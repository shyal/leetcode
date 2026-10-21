"""Fill mu/chrome with what is not checked in: the mulang package as one
file, session.py, the leet profile frozen to data (an unpacked extension
cannot read outside its folder, and Pyodide has no pydsa), and
ratings.json, slug -> [CLIST rating, zerotrac rating], 0 where a source
has none. `make mu-chrome` runs it and fetches Pyodide into mu/chrome/pyodide."""

import csv
import json
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).parent
ROOT = HERE.parent.parent
# the script's own folder holds the last build's mulang.py; import the live one
sys.path = [p for p in sys.path if Path(p or ".").resolve() != HERE.resolve()]
sys.path.insert(0, str(HERE.parent))
import leetmu  # noqa: E402, F401
import mulang  # noqa: E402

shutil.copy(mulang.__file__, HERE / "mulang.py")
shutil.copy(HERE.parent / "session.py", HERE / "session.py")
frozen = {
    name: [list(h.imports), list(h.deps), h.source, h.doc]
    for name, h in mulang.HELPERS.items()
    if name not in mulang.RUNTIME
}
(HERE / "leetmu.py").write_text(
    '"""The leet profile, frozen to data by mu/chrome/build.py: the helpers\n'
    'pydsa gives mu, as mulang.Helper rows."""\n\n'
    "import mulang\n\n"
    f"HELPERS = {json.dumps(frozen, indent=1)}\n\n"
    "for _name, _row in HELPERS.items():\n"
    "    mulang.HELPERS.setdefault(_name, mulang.Helper(*_row))\n"
)
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
print(
    f"mu/chrome: mulang.py, session.py and leetmu.py written, "
    f"{len(frozen)} helpers, {len(ratings)} problem ratings"
)
