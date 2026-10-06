"""Every Rust reference solution, graph/node_notes/<node>/dNNN_*.rs, is
spliced into its drill above `fn main`, in place of whatever stub the drill
holds there, with the commented-out asserts turned on, and run the way
`make` runs current.rs: rustc --edition 2021, then the binary. The Rust
twin of test_reference_solutions.py. Needs rustc on PATH (kg::lang)."""

import glob
import os
import re
import shutil
import subprocess

import pytest
from test_reference_solutions import ROOT, drill_for

REFERENCES = sorted(
    glob.glob(os.path.join(ROOT, "graph", "node_notes", "*", "d[0-9]*.rs"))
)
MAIN = re.compile(r"^fn main\(\)", re.M)


def spliced(drill_src, reference_src):
    """The drill file with everything between its statement block and
    `fn main` replaced by the reference, and every commented-out line of
    main turned on."""
    main_at = MAIN.search(drill_src)
    assert main_at, "drill has no fn main"
    head_lines = []
    for line in drill_src.splitlines(keepends=True):
        if line.startswith("//") or not line.strip():
            head_lines.append(line)
        else:
            break
    head = "".join(head_lines)
    main = drill_src[main_at.start() :]
    main = re.sub(r"^(\s*)// (?=\S)", r"\1", main, flags=re.M)
    return head + reference_src.rstrip("\n") + "\n\n" + main


@pytest.mark.skipif(shutil.which("rustc") is None, reason="rustc is not installed")
@pytest.mark.parametrize("reference", REFERENCES, ids=os.path.basename)
def test_rs_reference_passes_its_drill(reference, tmp_path):
    drill = drill_for(reference)
    src = spliced(open(drill).read(), open(reference).read())
    assert "\n    assert" in src, f"{drill} has no asserts"
    script = tmp_path / os.path.basename(drill)
    script.write_text(src)
    binary = tmp_path / "current"
    build = subprocess.run(
        ["rustc", "--edition", "2021", "--crate-name", "current", "-o", str(binary)]
        + [str(script)],
        capture_output=True,
        text=True,
        cwd=ROOT,
        timeout=120,
    )
    assert build.returncode == 0, build.stdout + build.stderr
    run = subprocess.run(
        [str(binary)], capture_output=True, text=True, cwd=ROOT, timeout=60
    )
    assert run.returncode == 0, run.stdout + run.stderr
