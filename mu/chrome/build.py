"""Fill mu/chrome with what is not checked in: the mulang package as one
file, session.py, the leet profile frozen to data (an unpacked extension
cannot read outside its folder, and Pyodide has no pydsa), and
ratings.json, slug -> the problem's rating, rounded. The rating is the one
the repo shows everywhere (kg::model::combined_ratings through kg_rs:
zerotrac's where it rates, else CLIST's on zerotrac's scale), so the
number on a LeetCode page is the number on make next. `make mu-chrome`
runs it and fetches Pyodide into mu/chrome/pyodide."""

import json
import shutil
import sys
from pathlib import Path

import kg_rs

HERE = Path(__file__).parent
ROOT = HERE.parent.parent
# the script's own folder holds the last build's mulang.py; import the live one
sys.path = [p for p in sys.path if Path(p or ".").resolve() != HERE.resolve()]
sys.path.insert(0, str(HERE.parent))
import leetmu  # noqa: E402, F401
import mulang  # noqa: E402


def problem_ratings(root):
    """slug -> rounded rating for every problem the repo rates: kg_rs rates
    by problem number, data/problems_metadata.json gives each number its
    slug. A number without a slug there has no page to label."""
    meta = json.loads((root / "data/problems_metadata.json").read_text())
    out = {}
    for num, rating in kg_rs.solve_ratings(str(root)).items():
        slug = meta.get(num, {}).get("slug")
        if slug:
            out[slug] = round(rating)
    return dict(sorted(out.items()))


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
ratings = problem_ratings(ROOT)
(HERE / "ratings.json").write_text(json.dumps(ratings, separators=(",", ":")))
print(
    f"mu/chrome: mulang.py, session.py and leetmu.py written, "
    f"{len(frozen)} helpers, {len(ratings)} problem ratings"
)
