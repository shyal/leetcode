# Every reference solution under graph/node_notes/<node>/dNNN_*.py is run
# against its drill's own asserts (drills/<node>/dNNN_*.py, with the
# commented-out asserts turned on). A reference that no longer passes its
# drill, or a reference whose drill is gone, fails here.
import glob
import os
import re
import subprocess
import sys

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
VENV_PY = os.path.join(ROOT, ".venv", "bin", "python3")
PY = VENV_PY if os.path.exists(VENV_PY) else sys.executable

REFERENCES = sorted(
    glob.glob(os.path.join(ROOT, "graph", "node_notes", "*", "d[0-9]*.py"))
)


def drill_for(reference):
    node = os.path.basename(os.path.dirname(reference))
    did = os.path.basename(reference).split("_")[0]
    hits = glob.glob(os.path.join(ROOT, "drills", node, f"{did}_*.py"))
    assert (
        len(hits) == 1
    ), f"{reference}: expected one drill drills/{node}/{did}_*.py, got {hits}"
    return hits[0]


# a line the asserts need: an assert, `name = ...` or `name += ...`, or a
# `sol.method(...)` call
SETUP = r"(?:assert |[\w.\[\]]+ (?:[-+*/]|//)?= |sol\.\w+\()"


def spliced(drill_src, reference_src):
    """The drill file with its Solution stub replaced by the reference and
    every commented-out assert (and any setup line an assert needs) turned
    on. The class may extend a dsa/ class, the constructor may take
    arguments, and the instance may have any name (`p = Solution(S)`)."""
    cls = re.search(r"^class Solution(\([^)]*\))?:", drill_src, flags=re.M)
    assert cls, "drill has no `class Solution` line"
    head, rest = drill_src[: cls.start()], drill_src[cls.end() :]
    after = re.search(r"^\S", rest, flags=re.M)
    assert after, "drill has nothing after the Solution class"
    tail = rest[after.start() :]
    assert re.search(r"= Solution\(", tail), "drill never builds a Solution"
    body = re.sub(rf"^# ({SETUP}.*)$", r"\1", tail, flags=re.M)
    return head + reference_src + "\n\n\n" + continued(body)


def continued(body):
    """Turn on the commented lines that continue an assert left open, as in
    `assert f(x) == [` followed by `#     [1, 2],` and `# ]`."""
    out, depth = [], 0
    for line in body.split("\n"):
        if depth > 0 and line.startswith("#"):
            line = line[2:] if line.startswith("# ") else line[1:]
        elif not re.match(SETUP, line):
            out.append(line)
            continue
        depth = max(0, depth + brackets(line))
        out.append(line)
    return "\n".join(out)


def brackets(line):
    """Opened minus closed brackets on a line, outside string literals."""
    code = re.sub(r"'[^']*'|\"[^\"]*\"", "", line.split("  #")[0])
    return sum(code.count(c) for c in "([{") - sum(code.count(c) for c in ")]}")


@pytest.mark.parametrize("reference", REFERENCES, ids=os.path.basename)
def test_reference_passes_its_drill(reference, tmp_path):
    drill = drill_for(reference)
    src = spliced(open(drill).read(), open(reference).read())
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
