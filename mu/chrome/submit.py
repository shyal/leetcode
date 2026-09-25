"""The Python side of the extension, run in Pyodide.

submission(src): what goes in LeetCode's editor, `# mu <version>`, the mu
solution quoted as comments, then the Python it compiles to. lc_submit sends a filed
solve in the same shape.

starter(py): the mu to start from, LeetCode's Python3 starter code
through mu/session.py stub. The starter leaves each def's body empty,
which does not parse, so every empty def first gets a `pass`."""

import re

from session import stub

from mu import VERSION, transpile

DEF = re.compile(r"^(\s*)def .*:\s*$")


def submission(src):
    quoted = "\n".join(f"# {ln}".rstrip() for ln in src.strip("\n").splitlines())
    return f"# mu {VERSION}\n{quoted}\n\n{transpile(src)}"


def indent(line):
    return len(line) - len(line.lstrip())


def starter(py):
    lines = py.rstrip().split("\n")
    out = []
    for k, line in enumerate(lines):
        out.append(line)
        m = DEF.match(line)
        rest = [ln for ln in lines[k + 1 :] if ln.strip()]
        if m and (not rest or indent(rest[0]) <= indent(line)):
            out.append(m.group(1) + "    pass")
    return stub("\n".join(out) + "\n") or ""
