# Smoke tests for the Rust binaries that replaced Python scripts outright
# (kg_rep, is_session_start, kg_chat, kg_status, kg_dependents, kg_gaps,
# kg_viz, estimate, kg_residuals, kg_predict, kg_sleep, kg_mirror, kg_drill,
# kg_solved, drill, kg_force, timer, kg_curve, kg_solvecost; utils/rs).
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


# --- kg_gaps, kg_viz, estimate ----------------------------------------------


def test_kg_gaps_table_shape():
    p = run("kg_gaps")
    assert p.returncode == 0, p.stderr
    lines = p.stdout.splitlines()
    assert lines[0].split() == ["suggested", "move", "unlocks", "mentions", "examples"]
    assert len(lines) <= 28  # header, up to 25 rows, blank, total
    assert "distinct suggestions" in lines[-1]
    assert len(run("kg_gaps", "--all").stdout.splitlines()) >= len(lines)


def test_kg_viz_source_is_dot_with_clusters_and_legend():
    p = run("kg_viz", "--source")
    assert p.returncode == 0, p.stderr
    assert p.stdout.startswith('digraph "technique-graph" {')
    assert 'subgraph "cluster_legend"' in p.stdout
    assert p.stdout.count('subgraph "cluster_') >= 3
    assert p.stdout.rstrip().endswith("}")


def test_estimate_rows():
    p = run("estimate")
    assert p.returncode == 0, p.stderr
    heads = [
        l.split("  ")[1].strip()
        for l in p.stdout.splitlines()
        if l.startswith("  ") and not l.startswith("   ")
    ]
    assert heads[:2] == ["Run date", "Node statuses"]
    assert any(h.startswith("Onsite (mock P(onsite)>=") for h in heads)


# --- kg_residuals, kg_predict -------------------------------------------------


def test_kg_residuals_table():
    p = run("kg_residuals")
    assert p.returncode == 0, p.stderr
    lines = p.stdout.splitlines()
    assert lines[0].endswith(" trials against curve.json")
    assert lines[2].split() == ["wing", "bucket", "n", "obs", "model", "z"]
    assert any("(<=21d)" in l or "(>21d)" in l for l in lines[3:])


def test_kg_predict_modes_agree():
    text = run("kg_predict", "1.5")
    assert text.returncode == 0, text.stderr
    assert text.stdout.startswith("at 1.5h/day, every day:")
    j = json.loads(run("kg_predict", "1.5", "--json").stdout)
    assert j["hours"] == 1.5 and j["days"] >= 35
    assert f"({j['days']} days)" in text.stdout
    hist = json.loads(run("kg_predict", "--history-json").stdout)
    assert hist and hist[-1]["run_date"] == j["run_date"] and hist[-1]["hours"] == 2.0


# --- kg_sleep, kg_mirror, kg_drill -------------------------------------------


def test_kg_sleep_list_shape():
    p = run("kg_sleep", "--list")
    assert p.returncode == 0, p.stderr
    lines = p.stdout.splitlines()
    assert lines == ["nothing parked"] or all(
        " - asleep (" in l and l.endswith(" when you choose") for l in lines
    )


def test_kg_mirror_rebuilds_the_db():
    import sqlite3

    p = run("kg_mirror")
    assert p.returncode == 0, p.stderr
    assert p.stdout.splitlines()[1] == "sqlite3 graph/leet.db"
    con = sqlite3.connect(os.path.join(ROOT, "graph", "leet.db"))
    nodes = con.execute("select count(*) from nodes").fetchone()[0]
    solves = con.execute("select count(*) from solves").fetchone()[0]
    con.close()
    assert f"{nodes} nodes" in p.stdout and f"{solves} solves" in p.stdout
    ev = json.load(open(os.path.join(ROOT, "graph", "evidence.json")))["evidence"]
    assert solves == len(ev)


def test_kg_drill_refuses_without_writing():
    before = open(os.path.join(ROOT, "graph", "evidence.json")).read()
    assert run("kg_drill").returncode == 2
    assert run("kg_drill", "set-membership", "meh").returncode == 2
    p = run("kg_drill", "no-such-node-xyz", "clean")
    assert p.returncode == 1 and p.stdout.startswith(
        "Unknown node id: no-such-node-xyz"
    )
    assert open(os.path.join(ROOT, "graph", "evidence.json")).read() == before


# --- drill, kg_solved ----------------------------------------------------------


def test_drill_list_and_unknown_node():
    drills = json.load(open(os.path.join(ROOT, "graph", "drills.json")))["drills"]
    did = sorted(drills, key=lambda d: int(d[1:]))[0]
    p = run("drill", did, "--list")
    assert p.returncode == 0, p.stderr
    assert p.stdout.split()[0] == did and "last drilled:" in p.stdout
    p = run("drill", "no-such-node-xyz", "--list")
    assert p.returncode == 1 and p.stdout.startswith(
        "No drills found under drills/no-such-node-xyz/"
    )


def test_kg_solved_files_nothing_from_an_empty_stub(tmp_path):
    """Run in a scratch directory: the file phase reads current.py from the
    working directory, so the repo's own attempt is never touched here."""
    (tmp_path / "current.py").write_text("\n")
    p = subprocess.run(
        [os.path.join(RS_BIN, "kg_solved")],
        capture_output=True,
        text=True,
        cwd=tmp_path,
    )
    assert p.returncode == 0, p.stderr
    assert p.stdout.strip() == "current.py is empty — nothing to file."
    assert (
        not (tmp_path / ".solve_meta.json").exists()
        and not (tmp_path / "solved").exists()
    )
    p = subprocess.run(
        [os.path.join(RS_BIN, "kg_solved"), "--commit"],
        capture_output=True,
        text=True,
        cwd=tmp_path,
    )
    assert p.stdout.strip() == "nothing staged — no commit to make."


# --- kg_force, timer -----------------------------------------------------------


def test_kg_force_clear_and_usage_in_a_scratch_root(tmp_path):
    """KG_ROOT points the binary at an empty root, so the repo's own
    .force.json is never touched."""
    env = {**os.environ, "KG_ROOT": str(tmp_path)}
    p = subprocess.run(
        [os.path.join(RS_BIN, "kg_force"), "--clear"],
        capture_output=True,
        text=True,
        env=env,
    )
    assert p.returncode == 0 and p.stdout == ""
    (tmp_path / ".force.json").write_text('{"problem": "1", "moves": []}')
    p = subprocess.run(
        [os.path.join(RS_BIN, "kg_force"), "--clear"],
        capture_output=True,
        text=True,
        env=env,
    )
    assert p.stdout.strip() == "constraint dropped — freestyle solve."
    assert not (tmp_path / ".force.json").exists()
    assert run("kg_force").returncode == 2


def test_timer_figlet_matches_pyfiglet_and_renders_a_frame():
    art = run("timer", "--figlet", "big", "1:05").stdout
    assert art == (
        " __    ___  _____ \n/_ |_ / _ \\| ____|\n | (_) | | | |__  \n"
        " | | | | | |___ \\ \n | |_| |_| |___) |\n |_(_)\\___/|____/ \n"
        "                  \n                  \n"
    )
    frame = run("timer", "--once").stdout
    assert frame.startswith("╭") and frame.rstrip().endswith("╯")
    assert "\x1b[" not in frame  # no colour when piped


# --- kg_curve, kg_solvecost (read-only modes: a refit rewrites graph/ files) ----


def test_kg_curve_solve_rows_bridge():
    p = run("kg_curve", "--solve-rows-json")
    assert p.returncode == 0, p.stderr
    rows = json.loads(p.stdout)
    assert rows and set(rows[0][0]) == {
        "gap",
        "rating",
        "recall",
        "unseen",
        "experience",
        "mass",
        "length",
    }
    assert rows[0][1] in (0.0, 0.5, 1.0) and len(rows[0][2]) == 10


def test_fitters_print_usage():
    assert run("kg_curve", "--help").stdout.startswith("usage: kg_curve")
    assert run("kg_solvecost", "--help").stdout.startswith("usage: kg_solvecost")
