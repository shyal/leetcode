"""Every TypeScript reference solution, graph/node_notes/<node>/dNNN_*.ts,
is spliced into its drill in place of the stub, with the commented-out
asserts turned on, and run the way `make` runs current.ts: tsc --strict,
then node. The TypeScript twin of test_reference_solutions.py. Needs node
22 and tsc on PATH (kg::lang)."""

import glob
import os
import re
import shutil
import subprocess

import pytest
from test_reference_solutions import ROOT, drill_for

REFERENCES = sorted(
    glob.glob(os.path.join(ROOT, "graph", "node_notes", "*", "d[0-9]*.ts"))
)
DECLARATIONS = os.path.join(ROOT, "utils", "harness", "ts", "node.d.ts")
# the first top-level declaration opens the stub; the demo or the first
# commented assert closes it
STUB_OPENS = re.compile(r"^(?:type|interface|function|class|const|let) ", re.M)
SCRIPT_OPENS = re.compile(r"^(?:console\.|// (?:assert|const|let|[a-z]\w*\())", re.M)


def spliced(drill_src, reference_src):
    """The drill file with its stub replaced by the reference and every
    commented-out script line turned on."""
    head_end = STUB_OPENS.search(drill_src)
    assert head_end, "drill has no declaration"
    script_at = SCRIPT_OPENS.search(drill_src, head_end.start())
    assert script_at, "drill has no demo or asserts"
    head, script = drill_src[: head_end.start()], drill_src[script_at.start() :]
    script = re.sub(r"^// (?=\S)", "", script, flags=re.M)
    return head + reference_src.rstrip("\n") + "\n\n" + script


@pytest.mark.skipif(shutil.which("node") is None, reason="node is not installed")
@pytest.mark.skipif(shutil.which("tsc") is None, reason="tsc is not installed")
@pytest.mark.parametrize("reference", REFERENCES, ids=os.path.basename)
def test_ts_reference_passes_its_drill(reference, tmp_path):
    drill = drill_for(reference)
    src = spliced(open(drill).read(), open(reference).read())
    assert "\nassert." in src, f"{drill} has no asserts"
    script = tmp_path / os.path.basename(drill)
    script.write_text(src)
    check = subprocess.run(
        ["tsc", "--noEmit", "--strict", "--target", "es2022", "--lib", "es2022,dom"]
        + ["--types", DECLARATIONS, str(script)],
        capture_output=True,
        text=True,
        cwd=ROOT,
        timeout=120,
    )
    assert check.returncode == 0, check.stdout + check.stderr
    run = subprocess.run(
        ["node", "--experimental-strip-types", "--no-warnings", str(script)],
        capture_output=True,
        text=True,
        cwd=ROOT,
        timeout=120,
    )
    assert run.returncode == 0, run.stdout[-2000:] + run.stderr[-2000:]
