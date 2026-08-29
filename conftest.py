import os
import sys

collect_ignore = ["stubs.py"]

# utils/ is the import root for the tooling packages (kg, history, readme) and
# utils/harness is the flat LeetCode-style namespace (Types, tree_utils, ...).
# The makefile passes both via PYTHONPATH; a bare `pytest` gets them here.
_ROOT = os.path.dirname(os.path.abspath(__file__))
for _p in (os.path.join(_ROOT, "utils", "harness"), os.path.join(_ROOT, "utils")):
    if _p not in sys.path:
        sys.path.insert(0, _p)
