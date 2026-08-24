# Golden lockstep test: utils/kg_lib.py and utils/kg_mock_rs both implement
# node_status (the forgetting-curve mastery derivation), and kg_mock's
# PyRandom claims to reproduce CPython's random.Random bit-for-bit. Nothing
# enforced that until now — the "kept in lockstep" comments were the only
# guard. This runs both sides over the REAL graph/ data and diffs the outputs
# exactly, so any drift in either implementation fails `make test`.

import json
import os
import random
import subprocess
from datetime import date

import pytest

import kg_lib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUST_BIN = os.path.join(ROOT, "utils", "kg_mock_rs", "target", "release", "kg_mock")


@pytest.fixture(scope="session", autouse=True)
def build_rust():
    subprocess.run(
        ["cargo", "build", "--release", "--quiet",
         "--manifest-path", os.path.join(ROOT, "utils", "kg_mock_rs", "Cargo.toml")],
        check=True, capture_output=True, text=True,
    )


@pytest.fixture(scope="module")
def golden():
    proc = subprocess.run(
        [RUST_BIN, "--golden-json"], capture_output=True, text=True, cwd=ROOT,
        check=True,
    )
    assert proc.stderr == ""
    return json.loads(proc.stdout)


def test_node_status_lockstep(golden):
    # same today as the Rust run, so the test can't flake across midnight
    today = date.fromisoformat(golden["today"])
    evidence = kg_lib.load_evidence()
    mismatches = []
    for node, exp in golden["nodes"].items():
        status, last = kg_lib.node_status(node, evidence, today)
        got = {"status": status, "last": last.isoformat() if last else None}
        if got != exp:
            mismatches.append(f"{node}: python={got} rust={exp}")
    assert not mismatches, "node_status drift:\n" + "\n".join(mismatches)
    # guard against a vacuous pass (empty evidence would make everything agree
    # on MISSING without exercising the curve math at all)
    statuses = {v["status"] for v in golden["nodes"].values()}
    assert statuses - {"MISSING"}, "no evidenced nodes — curve math untested"


def test_pyrandom_random_bit_for_bit(golden):
    rng = random.Random(42)
    assert [rng.random() for _ in range(20)] == golden["random"]


def test_pyrandom_randint_bit_for_bit(golden):
    rng = random.Random(42)
    assert [rng.randint(1, 1000) for _ in range(20)] == golden["randint"]
