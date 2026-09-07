"""Extra asserts for a prepared problem, computed by running the reference.

The prepare pipeline's edge-case stage proposes single-call expressions, which
a design problem cannot express - a class is driven by a SEQUENCE of calls, so
2349 shipped with nothing but its two official asserts, and a solve whose
find() popped the heap passed both.

Two stages here, both written against the validated reference solution in the
prepare cache and both frozen by executing it, so no expected value is ever
guessed:

  _stress(n) replays a seeded random workload of n operations,
  _edges() walks the boundary cases by hand, each one labelled.
"""

import ast
import re

# The asserts have to stay readable in the solve file, so a workload whose
# answer does not fit on a few lines shrinks until it does.
SIZES = (40, 25, 10)
MAX_REPR = 400

DRIVER_PROMPT = """\
The file below contains a correct, validated solution to a LeetCode problem.

Write ONE function `_stress(n)` that exercises it under a random workload:

- its first statement is `random.seed(n)`, so each size is a different
  workload (random is already a builtin here)
- it builds a workload of about n operations or n elements, strictly inside
  the problem's constraints, and works for any n from 10 to 100
- it drives the solution the way the problem does: construct the class and
  call its methods in a random order, or call the Solution method on random
  inputs
- it returns a list of the plain comparable values observed (ints, strings,
  tuples) - one per query. Wrap structure results with helpers like
  get_level_order / get_list_values, as the existing asserts do.
- when a single answer can be large (every subset, every permutation, a whole
  grid), append a fingerprint of it - its length with its smallest and largest
  element, say - rather than the answer itself
- it prints nothing, asserts nothing, and reads no global state

Output ONLY the function source.

{code}
"""

EDGE_MORE = """\

These cases are already covered, by these labels:

{labels}

Keep EVERY one of them, with its label spelled exactly as it is above, and add
at least six cases they miss. The point of this pass is the new ones: look for
the situations the existing labels do not name.
"""

EDGE_PROMPT = """\
The file below contains a correct, validated solution to a LeetCode problem.

Write ONE function `_edges()` that walks its edge cases:

- it returns a list of `(label, value)` pairs, where label is a short string
  naming the case and value is what the solution answered
- a label describes what the INPUT does, in the problem's own words, and never
  how a solution copes with it: "index_reassigned_then_queried", not
  "stale_heap_entry_skipped". The file is read by someone about to solve the
  problem; a label that names heaps, caches, memoization, two pointers or any
  other mechanism hands them the answer.
- cover the boundaries that actually bite this problem: the smallest legal
  input, an empty or absent lookup, a value replaced by itself, duplicates,
  negatives, a query before anything exists, the extremes the constraints
  allow
- construct a fresh solution object for each independent case
- every value a plain comparable one
- it prints nothing, asserts nothing, and reads no global state
{more}
Output ONLY the function source.

{code}
"""


def _strip_fences(out):
    if out.startswith("```"):
        lines = out.splitlines()[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        out = "\n".join(lines).strip()
    return out


def _is_function(src, name, argc):
    """Usable only as exactly one function of the expected shape."""
    try:
        tree = ast.parse(src)
    except SyntaxError:
        return False
    return (
        len(tree.body) == 1
        and isinstance(tree.body[0], ast.FunctionDef)
        and tree.body[0].name == name
        and len(tree.body[0].args.args) == argc
    )


def _evaluate(run, code, helper, expr):
    """The repr of `expr` under solution+helper, or None if it did not run or
    did not come back as a literal. A repr like <TreeNode object> cannot be
    asserted against, and neither can a value that took an exception."""
    harness = f"{code}\n\n{helper}\n\nprint('@@', repr({expr}))\n"
    ok, output = run(harness)
    if not ok:
        return None
    rep = next((l[3:] for l in output.splitlines() if l.startswith("@@ ")), None)
    if rep is None:
        return None
    try:
        ast.literal_eval(rep)
    except (ValueError, SyntaxError):
        return None
    return rep


def workload_block(code, llm, run):
    """A seeded random workload, replayed at every size whose answer fits."""
    driver = _strip_fences(llm(DRIVER_PROMPT.format(code=code)))
    if not _is_function(driver, "_stress", 1):
        return None
    asserts = []
    for size in SIZES:
        rep = _evaluate(run, code, driver, f"_stress({size})")
        if rep is not None and len(rep) <= MAX_REPR:
            asserts.append(f"assert _stress({size}) == {rep}")
    if not asserts:
        return None
    return "\n".join(
        ["", "", "# stress: seeded random workloads, replayed against the "
         "reference solution.", driver.rstrip(), "", ""] + asserts
    ) + "\n"


def edge_labels(code):
    """The labels a file's frozen `assert _edges() == [...]` already covers."""
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Assert) or not isinstance(node.test, ast.Compare):
            continue
        left = node.test.left
        if not (isinstance(left, ast.Call) and isinstance(left.func, ast.Name)
                and left.func.id == "_edges"):
            continue
        try:
            pairs = ast.literal_eval(node.test.comparators[0])
        except (ValueError, SyntaxError):
            return []
        return [p[0] for p in pairs if isinstance(p, tuple) and p]
    return []


def strip_edges(code):
    """`code` without its edge block - the function, its assert, and the
    comment above it. A grown block replaces the old one rather than sitting
    beside it under a second name."""
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return code
    cut = set()
    for node in tree.body:
        is_def = isinstance(node, ast.FunctionDef) and node.name == "_edges"
        is_assert = (
            isinstance(node, ast.Assert)
            and isinstance(node.test, ast.Compare)
            and isinstance(node.test.left, ast.Call)
            and isinstance(node.test.left.func, ast.Name)
            and node.test.left.func.id == "_edges"
        )
        if is_def or is_assert:
            cut.update(range(node.lineno, node.end_lineno + 1))
    if not cut:
        return code
    src = code.splitlines()
    kept = [l for i, l in enumerate(src, 1)
            if i not in cut and not (i + 1 in cut and l.lstrip().startswith("#"))]
    return "\n".join(kept).rstrip() + "\n"


def edge_block(code, llm, run):
    """The boundary cases, each one labelled by the case it covers. On a
    problem that already has some, the model keeps them and hunts for more,
    and the whole block is re-frozen against the reference."""
    covered = edge_labels(code)
    more = EDGE_MORE.format(labels="\n".join("- " + l for l in covered)) \
        if covered else "- at most 12 pairs\n"
    base = strip_edges(code)
    edges = _strip_fences(llm(EDGE_PROMPT.format(code=base, more=more)))
    if not _is_function(edges, "_edges", 0):
        return None
    rep = _evaluate(run, base, edges, "_edges()")
    if rep is None:
        return None
    # a pass that dropped cases is a pass that lost coverage: keep what is
    # already frozen instead
    grown = [p[0] for p in ast.literal_eval(rep) if isinstance(p, tuple) and p]
    if not set(covered) <= set(grown) or len(grown) <= len(covered):
        return None
    return base.rstrip() + "\n" + "\n".join(
        ["", "", "# edge cases, labelled; the values are the reference "
         "solution's.", edges.rstrip(), "", "", f"assert _edges() == {rep}"]
    ) + "\n"


def extra_asserts(code, llm, run):
    """The file with both blocks, each kept only if it still runs green.

    The workload is generated once; the edge cases grow on every pass.
    """
    if not has_workload(code):
        try:
            extra = workload_block(code, llm, run)
        except Exception:
            extra = None
        if extra:
            merged = code.rstrip() + "\n" + extra
            if run(merged)[0]:
                code = merged
    try:
        merged = edge_block(code, llm, run)
    except Exception:
        merged = None
    if merged and run(merged)[0]:
        code = merged
    return code


def has_workload(code):
    return re.search(r"^def _stress\(", code, re.M) is not None


def has_stress(code):
    return re.search(r"^def (_stress|_edges)\(", code, re.M) is not None
