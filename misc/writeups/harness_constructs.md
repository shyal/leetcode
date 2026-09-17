# Harness constructs: what the corpus asks for

2026-09-17. Corpus: 1210 files in `solved/`, 14204 lines of solution code
(class and def bodies only; no docstrings, no asserts).

Method: normalise every statement (names to N, constants to C), rank the
statement shapes and consecutive pairs, then write AST matchers for the
recurring multi-line idioms and measure lines before and after a one-line
construct. Nine real solutions were rewritten with prototype helpers and
run against their own asserts; all pass. Files in `harness_constructs/`:

- `mine_idioms.py`: the matchers; run from the repo root, prints the table.
- `proto.py`: the candidate helpers.
- `rewrites.py`: the nine rewrites with asserts.

## What the corpus says

| idiom | problems | instances (prob/drill) | lines now | after | saved |
|---|---|---|---|---|---|
| binary search loop, on an answer | 21 | 31 / 4 | 382 | 70 | 312 |
| binary search loop, on an index | 14 | 30 / 7 | 386 | 74 | 312 |
| nested def appending to an outer `res` | 26 | 20 / 26 | 138 | 46 | 92 |
| void tree dfs (traversal only) | 20 | 22 / 0 | 110 | 22 | 88 |
| digit peel `n % 10`, `n //= 10` | 18 | 24 / 0 | 96 | 24 | 72 |
| graph bfs with a `seen` set | 2 | 3 / 0 | 65 | 3 | 62 |
| `res = []` / `append` / `return res` | 9 | 9 / 3 | 56 | 12 | 44 |
| `count = 0` / `count += 1` / `return count` | 13 | 12 / 1 | 56 | 13 | 43 |
| Kahn | 2 | 4 / 0 | 48 | 8 | 40 |
| `for i: for j in range(i+1, n)` | 14 | 15 / 23 | 76 | 38 | 38 |
| `if n.left: push` / `if n.right: push` | 4 | 9 / 0 | 36 | 9 | 27 |
| `it = head; while it: ... it = it.next` | 9 | 11 / 0 | 33 | 11 | 22 |
| adjacency build loop | 6 | 9 / 0 | 28 | 9 | 19 |

Total: about 1300 lines, 9% of the corpus. Binary search alone is 624
lines, 4.4%, in 35 distinct problems. Nothing else comes close.

Precedent: the grid helpers landed on 2026-09-13; since then 25 of 40 grid
solves use them.

## Proposals, ranked

### 1. `first_true(lo, hi, ok)` and `last_true(lo, hi, ok)`

The smallest x in [lo, hi] with ok(x), assuming ok is False then True;
hi + 1 if none. `last_true` is the mirror; lo - 1 if none. Same names as
the drills d_First_True and d_Last_True. One line on Python 3.10:

    lo + bisect_left(range(lo, hi + 1), True, key=ok)

    # 1760. Minimum Limit of Balls in a Bag: 11 lines -> 2
    ops = lambda cap: sum(ceil_div(n, cap) - 1 for n in nums)
    return first_true(1, max(nums), lambda cap: ops(cap) <= maxOperations)

    # 1539. Kth Missing Positive Number: 9 lines -> 1
    return first_true(0, len(arr) - 1, lambda i: arr[i] - i - 1 >= k) + k

Every problem in the "answer" row and most in the "index" row collapse to
the predicate plus this call. The predicate is the problem; the loop never
was.

### 2. Tree iterators: `preorder`, `inorder`, `postorder`, `levels`, `children`

Generators over nodes. `levels(root)` yields the list of nodes per level.
`children(node)` is the non-None children, left before right. Of the 20
void dfs problems, 13 are pure traversals (94, 144, 145, 102, 199, 1161,
1302, 226, 114, 783, 872, 897, 297 serialize); the rest carry a path or
mutate a BST and stay as they are. Tree DP (a dfs that returns a value,
24 problems) is untouched by design.

    # 102. Binary Tree Level Order Traversal: 11 lines -> 1
    return [[n.val for n in level] for level in levels(root)]

### 3. `nodes(head)`

Yields each node of a linked list. It reads `.next` before yielding, so
deleting the current node inside the loop is safe. 3 lines to 1 per walk,
9 problems.

### 4. `adjacency(edges, n=None, directed=False)`, `bfs(adj, *sources)`, `toposort(adj)`

`bfs` yields (node, dist) nearest first. Low frequency (6, 2, 2 problems)
but 10 to 30 lines each. 210. Course Schedule II went from 30 lines to 3.
Second tier.

### 5. Digits: no helper

All 18 problems are base 10, so `map(int, str(n))` already does it in one
expression. `digits` is taken anyway: sitecustomize preloads
`string.digits` ('0123456789').

## Already in the language

Three rows are a habit, not a missing construct: `count` loops are
`sum(cond for ...)`, `res`/`append`/`return` loops are a comprehension, and
a nested def that appends to an outer list is `@as_list` plus `yield`
(landed 2026-09-16, 2 files use it, 26 problems could). Triangular double
loops are `pairs(n)` (15 problem instances still hand-roll it). These are
220 lines with zero new code; a snippet or a note is the fix.

## Not proposing

- `path.append(x); rec(); path.pop()`: 13 problems, 66 drill reps. A
  `with` block saves one line and it is the technique the drill trains.
- `best = max(best, e)`: 42 problems, 102 hits. Python has no `max=`; an
  accumulator object would be a coined thing. Leave it.
- Interval merge, Dijkstra: 2 problems each. Not worth a name yet.

## Names checked

None of `first_true`, `last_true`, `nodes`, `children`, `preorder`,
`inorder`, `postorder`, `levels`, `adjacency`, `bfs`, `toposort` is a
builtin today. `nodes` (138 files) and `children` (25) are common local
names in `solved/`; a local shadows a builtin harmlessly, and ruff does not
lint `solved/`.
