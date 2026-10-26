"""graph/drills.json is the one place a drill is named: each entry's "file"
is a bank file under drills/, each bank file is the "file" of exactly one
entry, and no bank file carries a DRILL or TRAINS line (2026-10-24: a
title rename had to touch 15 files and broke the link to the reps)."""

import glob
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DRILLS = os.path.join(ROOT, "drills")
REGISTRY = json.load(open(os.path.join(ROOT, "graph", "drills.json")))["drills"]
BANK = sorted(
    os.path.relpath(p, DRILLS)
    for p in glob.glob(os.path.join(DRILLS, "*", "*"))
    if os.path.isfile(p)
)


def test_every_entry_names_a_bank_file_and_trains_a_node():
    for did, d in REGISTRY.items():
        assert d.get("title"), did
        assert d.get("file") in BANK, f"{did}: no bank file {d.get('file')}"
        assert d.get("trains"), f"{did}: no trains"


def test_every_bank_file_has_one_entry():
    owners: dict[str, list[str]] = {}
    for did, d in REGISTRY.items():
        owners.setdefault(d["file"], []).append(did)
    for f in BANK:
        assert len(owners.get(f, [])) == 1, f"{f}: entries {owners.get(f)}"


def test_no_bank_file_carries_a_header():
    head = re.compile(r"^\s*(?://|#|--)?\s*\**(DRILL|TRAINS):", re.M)
    hits = [f for f in BANK if head.search(open(os.path.join(DRILLS, f)).read())]
    assert not hits, hits


def test_titles_are_unique():
    titles = [d["title"] for d in REGISTRY.values()]
    assert len(titles) == len(set(titles))
