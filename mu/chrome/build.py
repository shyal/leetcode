"""Fill mu/chrome with what is not checked in: copies of mu.py and
session.py (an unpacked extension cannot read outside its folder) and ratings.json,
slug -> [CLIST rating, zerotrac rating], 0 where a source has none.
`make mu-chrome` runs it and fetches Pyodide into mu/chrome/pyodide."""

import csv
import json
import shutil
from pathlib import Path

HERE = Path(__file__).parent
ROOT = HERE.parent.parent

for f in ("mu.py", "session.py"):
    shutil.copy(HERE.parent / f, HERE / f)
# Chrome refuses to load a folder holding a name that starts with "_"
shutil.rmtree(HERE / "__pycache__", ignore_errors=True)
ratings: dict[str, list[int]] = {}
for row in json.loads((ROOT / "data/clist_problems.json").read_text()):
    if row.get("rating"):
        ratings[row["slug"]] = [round(row["rating"]), 0]
with open(ROOT / "data/leetcode_ratings.tsv") as f:
    for row in csv.DictReader(f, delimiter="\t"):
        ratings.setdefault(row["slug"], [0, 0])[1] = round(float(row["rating"]))
(HERE / "ratings.json").write_text(json.dumps(ratings, separators=(",", ":")))
print(f"mu/chrome: mu.py and session.py copied, {len(ratings)} problem ratings written")
