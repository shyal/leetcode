import os
import sys

# utils/ is the import root for the tooling packages (kg, history, readme) and
# utils/harness is the flat LeetCode-style namespace (Types, tree_utils, ...).
# The makefile passes both via PYTHONPATH; a bare `pytest` gets them here.
_ROOT = os.path.dirname(os.path.abspath(__file__))
for _p in (os.path.join(_ROOT, "utils", "harness"), os.path.join(_ROOT, "utils")):
    if _p not in sys.path:
        sys.path.insert(0, _p)


def pytest_configure():
    """Keep the operator's .envrc out of the suite.

    kg.kg_lib reads the repo's .envrc into os.environ at import, so the
    knobs set there (DRILL_SCHEDULER=anki, KG_GROUP_CAP, MAX_NEW_DRILLS,
    SPOT_EVERY, ...) answer for the defaults the tests assert: with the
    anki clock in the environment, eleven tests in test_kg_next went red
    here while CI, which has no .envrc, was green. Every name .envrc sets
    is dropped before collection, whether it arrived from the file or from
    a shell that loaded it earlier. A test that wants a knob sets it itself
    with monkeypatch.
    """
    from kg import kg_lib
    for name in kg_lib.load_envrc(environ={}):
        os.environ.pop(name, None)
