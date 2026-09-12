# Smoke tests for the Rust binaries that replaced Python scripts outright
# (kg_rep, is_session_start, kg_chat, kg_status, kg_dependents; utils/rs).
# Each was diffed against
# its Python original over the real graph/ data before the Python was
# deleted (2026-09-12); these guard the shape of what they print, and make
# sure CI builds them.
import json
import os
import subprocess

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RS_BIN = os.path.join(ROOT, "utils", "rs", "target", "release")


@pytest.fixture(scope="session", autouse=True)
def build_rust():
    subprocess.run(
        [
            "cargo",
            "build",
            "--release",
            "--quiet",
            "--manifest-path",
            os.path.join(ROOT, "utils", "rs", "Cargo.toml"),
        ],
        check=True,
        capture_output=True,
        text=True,
    )


def run(name, *args, stdin=None):
    return subprocess.run(
        [os.path.join(RS_BIN, name), *args],
        capture_output=True,
        text=True,
        input=stdin,
        cwd=ROOT,
    )


def _first_evidenced_problem():
    ev = json.load(open(os.path.join(ROOT, "graph", "evidence.json")))["evidence"]
    return next(str(r["problem"]) for r in ev.values() if r.get("problem"))


def test_kg_rep_problem_report():
    pnum = _first_evidenced_problem()
    p = run("kg_rep", pnum)
    assert p.returncode == 0, p.stderr
    lines = p.stdout.splitlines()
    assert lines[0].startswith(f"problem: {pnum}. ")
    assert any(l.startswith("rep ") and "not first exposure" in l for l in lines)
    assert any(l.startswith("  rep 1  ") for l in lines)


def test_kg_rep_unknown_reference():
    p = run("kg_rep", "no-such-thing-xyz")
    assert p.returncode == 1
    assert p.stdout.strip() == "nothing known for 'no-such-thing-xyz'"


def test_kg_rep_line_is_silent_on_unknown():
    p = run("kg_rep", "--line", "no-such-thing-xyz")
    assert p.returncode == 0 and p.stdout == ""


def test_is_session_start_prints_a_predicate():
    p = run("is_session_start")
    assert p.stdout.strip() in ("true", "false")
    assert p.returncode == (0 if p.stdout.strip() == "true" else 1)


def test_kg_chat_check_is_quiet_for_a_foreign_session_on_master():
    branch = subprocess.run(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
        capture_output=True,
        text=True,
        cwd=ROOT,
    ).stdout.strip()
    p = run("kg_chat", "--check", stdin=json.dumps({"session_id": "not-a-real-id"}))
    assert p.returncode == 0
    if branch in ("master", "HEAD"):
        assert p.stdout == ""
    else:
        assert p.stdout.startswith(f"[this is not branch {branch}'s conversation")


# --- kg_rs, the extension kg_lib imports -----------------------------------


def test_kg_rs_drill_key():
    import kg_rs

    assert kg_rs.drill_key("solved/d_paid_orders_2026_09_03t10.py") == "d_paid_orders"
    assert kg_rs.drill_key("solved/D_Two_Sum_x.py") == "d_two_sum"
    assert kg_rs.drill_key("solved/p1004_2026_09_03t10.py") is None


def test_kg_rs_degree_color_ends_of_the_ramp():
    import kg_rs

    assert kg_rs.degree_color(0.0) == "#da3633"
    assert kg_rs.degree_color(1.0) == "#3fb950"
    assert kg_rs.degree_color(-3) == "#da3633"
    assert kg_rs.degree_color(0.5).startswith("#") and len(kg_rs.degree_color(0.5)) == 7


# --- kg_status, kg_dependents ------------------------------------------------


def test_kg_status_summary_shape():
    p = run("kg_status", "--summary")
    assert p.returncode == 0, p.stderr
    lines = p.stdout.splitlines()
    assert lines[1].startswith("Technique graph · ")
    assert [l.split()[1] for l in lines[2:6]] == [
        "SOLID",
        "STALE",
        "FRAGILE",
        "MISSING",
    ]
    assert any(l.startswith("ownership: mean ") for l in lines)
    assert "by group" not in p.stdout
    assert "by group" in run("kg_status").stdout


def test_kg_dependents_unknown_and_usage():
    p = run("kg_dependents", "no-such-id")
    assert (
        p.returncode == 1
        and p.stdout.strip() == "nothing in the graph is called no-such-id"
    )
    assert run("kg_dependents").returncode == 2


def test_kg_dependents_lists_a_gated_problem():
    problems = json.load(open(os.path.join(ROOT, "graph", "problems.json")))["problems"]
    gate, held = next(
        (str(p["after"][0]), pnum) for pnum, p in problems.items() if p.get("after")
    )
    p = run("kg_dependents", gate)
    assert p.returncode == 0, p.stderr
    assert p.stdout.splitlines()[0].startswith(gate)
    assert any(l.split()[:1] == [held] for l in p.stdout.splitlines())
