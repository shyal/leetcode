"""Extra asserts for a prepared problem, computed by running the reference.

The prepare pipeline's edge-case stage proposes single-call expressions, which
a design problem cannot express - a class is driven by a SEQUENCE of calls, so
2349 shipped with nothing but its two official asserts, and a solve whose
find() popped the heap passed both.

Every assert here is one self-contained line: a class is built inline with the
walrus operator, so no line depends on any other and the block can be
uncommented whole or a line at a time. The expected values are frozen by
executing the validated reference solution from the prepare cache, so none is
ever guessed, and each line carries the case it covers as a trailing comment.

Run it again on the same problem and the block grows: the cases already
covered are handed to the model as labels it must look past, and the new lines
are appended under them.
"""

import ast
import re

MARK = "# edge cases: one line each, the values are the reference solution's."

# A line the solve file has to stay readable with. Anything longer is a
# workload, not a case, and gets dropped.
MAX_LINE = 240

PROMPT = """\
The file below contains a correct, validated solution to a LeetCode problem.

Propose test expressions for its edge cases: ONE line each, formatted as

    <expression>  # <label>

Rules for the expression:

- it evaluates to a plain comparable value (int, string, tuple, list of them).
  Wrap structure results with helpers like get_level_order / get_list_values,
  as the existing asserts do.
- it is entirely self-contained - no line may depend on another having run,
  and none may use `sol` or any other object the file already built. A problem
  driven by a class is built inline with the walrus operator and the query
  taken last, like this:

    [(nc := NumberContainers()), nc.change(5, 7), nc.change(5, 8), nc.find(7)][-1]

- it stays under 200 characters, and it defines no function

Rules for the label:

- it describes what the INPUT does, in the problem's own words, and never how
  a solution copes with it: "index_reassigned_then_queried", not
  "stale_heap_entry_skipped". The file is read by someone about to solve the
  problem; a label naming heaps, caches, memoization or two pointers hands
  them the answer.

Cover the boundaries that actually bite this problem: the smallest legal
input, an empty or absent lookup, a value replaced by itself, duplicates,
negatives, a query before anything exists, the extremes the constraints allow,
and a longer mixed sequence or two.

At most 12 lines. Output ONLY those lines - no asserts, no expected values, no
blank lines, no prose.
{more}
{code}
"""

MORE = """
These cases are already covered:

{labels}

Propose ones they miss. A repeat of a case above is wasted: the point of this
pass is what the existing labels do not name.
"""


def _strip_fences(out):
    if out.startswith("```"):
        lines = out.splitlines()[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        out = "\n".join(lines).strip()
    return out


def _proposals(text):
    """(expression, label) for each usable line the model proposed."""
    out = []
    for line in text.splitlines():
        line = line.strip().rstrip(",")
        if not line or line.startswith(("#", "```", "assert ")):
            continue
        expr, _, label = line.partition("#")
        expr, label = expr.strip(), label.strip()
        if not expr or not label:
            continue
        try:
            tree = ast.parse(expr, mode="eval")
        except SyntaxError:
            continue
        if any(isinstance(n, (ast.Lambda, ast.FunctionDef)) for n in ast.walk(tree)):
            continue
        out.append((expr, re.sub(r"\W+", "_", label).strip("_")))
    return out


def covered(code):
    """The labels a file's one-line asserts already carry."""
    return [m.group(1) for m in
            re.finditer(r"^assert .*#\s*(\S+)\s*$", code, re.M)]


def _freeze(run, code, proposals):
    """Run every proposal against the reference and keep the ones that come
    back as a literal. A proposal that raises, hangs on a helper the file does
    not have, or answers with a repr like <TreeNode object> is dropped."""
    harness = [code, ""]
    for i, (expr, _) in enumerate(proposals):
        harness.append(
            f"try:\n"
            f"    print('@@', {i}, repr(({expr})))\n"
            f"except Exception:\n"
            f"    pass"
        )
    ok, output = run("\n".join(harness))
    if not ok:
        return []
    frozen = {}
    for line in output.splitlines():
        if not line.startswith("@@ "):
            continue
        _, idx, rep = line.split(" ", 2)
        try:
            ast.literal_eval(rep)
        except (ValueError, SyntaxError):
            continue
        frozen[int(idx)] = rep
    return [(proposals[i][0], proposals[i][1], frozen[i]) for i in sorted(frozen)]


def extra_asserts(code, llm, run):
    """`code` with one assert line appended per new edge case it survives."""
    already = covered(code)
    more = MORE.format(labels="\n".join("- " + l for l in already)) if already else ""
    proposals = _proposals(_strip_fences(llm(PROMPT.format(code=code, more=more))))
    proposals = [(e, l) for e, l in proposals if l not in already]
    if not proposals:
        return code

    lines = []
    seen = set(already)
    for expr, label, rep in _freeze(run, code, proposals):
        line = f"assert {expr} == {rep}  # {label}"
        if label in seen or len(line) > MAX_LINE:
            continue
        seen.add(label)
        lines.append(line)
    if not lines:
        return code

    head = [] if MARK in code else ["", "", MARK]
    merged = code.rstrip() + "\n" + "\n".join(head + lines) + "\n"
    # one line that fails against the reference itself poisons the block, so
    # the whole pass is dropped rather than a guess being cached
    return merged if run(merged)[0] else code


def has_extra(code):
    return MARK in code
