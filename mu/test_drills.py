"""Every mu reference solution, graph/node_notes/<node>/dNNN_*.mu, is
transpiled and run against its drill's own asserts, the same way
utils/tests/test_reference_solutions.py runs the Python ones."""

import glob
import os
import subprocess
import sys

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path[:0] = [HERE, os.path.join(ROOT, "utils", "tests")]
from test_reference_solutions import PY, drill_for, spliced  # noqa: E402

from mu import VERSION, transpile  # noqa: E402
from session import solution  # noqa: E402

REFERENCES = sorted(
    glob.glob(os.path.join(ROOT, "graph", "node_notes", "*", "d[0-9]*.mu"))
)


@pytest.mark.parametrize("reference", REFERENCES, ids=os.path.basename)
def test_mu_reference_passes_its_drill(reference, tmp_path):
    drill = drill_for(reference)
    mu_src = open(reference).read()
    quoted = "\n".join(f"# {ln}".rstrip() for ln in solution(mu_src).splitlines())
    src = spliced(open(drill).read(), f"# mu {VERSION}\n{quoted}\n\n" + transpile(mu_src))
    assert "assert " in src, f"{drill} has no asserts"
    script = tmp_path / os.path.basename(drill)
    script.write_text(src)
    env = dict(
        os.environ,
        PYTHONPATH=os.pathsep.join(
            [ROOT, os.path.join(ROOT, "utils"), os.path.join(ROOT, "utils", "harness")]
        ),
    )
    run = subprocess.run(
        [PY, str(script)],
        capture_output=True,
        text=True,
        env=env,
        cwd=ROOT,
        timeout=120,
    )
    assert run.returncode == 0, run.stdout[-2000:] + run.stderr[-2000:]
