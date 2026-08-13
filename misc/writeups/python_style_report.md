# Style Genome

Python style report, solves only: the 2021 pythonical wiki against the 2025-2026 solve files, plus what the old wiki is still good for.

Corpus: all 77 solves from 2026; ~70 sampled of 556 solves from 2025 (greps ran over all 556); ~65 pages read of 200 in pythonical, all 200 inventoried.

Scope: solution code only. Tooling under `utils/`, `dsa/`, `graph/` was read only to map where pythonical could plug in. Two environment facts are excluded from style claims: missing imports come from sitecustomize, and the 2025 files are black-formatted.

## The short version

Your Python is **expression-first**. Given a choice between accumulating with statements and computing the answer as one expression, you pick the expression: a generator fed to `sum`/`any`/`all`, a `reduce`, a comprehension, an `accumulate`. When statements are unavoidable you compress the state change into one line of tuple assignment. That instinct is identical in 2021 and 2026; what changed is that the 2021 version showed off (boolean tuple indexing, `~i` evangelism, code golf) and the current version mostly just uses the vocabulary and moves on.

The second constant: you learn Python by **collecting named idioms on purpose**. Pythonical was a hand-built curriculum of them ("single bidirectional pass", "list index complement", "shifted zip"). The technique graph is the same instinct with scheduling and evidence bolted on. You have been building the same system for five years; the 2021 one just didn't have a forgetting curve.

## Tells that survive five years

Things that would identify your code blind, present in both eras.

**1. `[*...]` splat instead of `list()`**
2021: 35 occurrences — `[*zip(*reversed(m))]`, `[*map(str.lower, filter(str.isalnum, s))]`. 2025: 36 files — `prefix = [*accumulate(nums)] + [0]` (p209). 2026: still going — `self.sums = [*accumulate(nums)]` (p303), even redundantly: `[*sorted(...)]` (p409).

**2. Nested closure helpers, and zero `nonlocal` ever**
Not one `nonlocal` in 633 solve files or the wiki. Scalar state goes through `self.` attributes or a dict used as a mutable cell, and the dict-cell hack is verbatim across five years: `output = {"str": ""}` (2021, alien dictionary), `data = {'ways': -1}` (2021, decoding a string), `mem = {'max': float('-inf')}` (2026, p124 Max Path Sum). 2021's `nested functions.md` argues the closure preference explicitly ("It may seem like nit-picking, but it isn't").

**3. Functional one-liners for problems others would loop**
2021: `reduce(lambda a, b: (a, b)[knows(a, b)], range(1, n), 0)` solves Find the Celebrity in one line; a whole loving `reduce.md`. 2026: `return reduce(xor, nums)` (p136), `reduce(ixor, [ord(x) for x in s] or [0])` (p389), `sum(x == 1 for x in ...)` bool-summing everywhere.

**4. Provenance honesty, in lowercase**
2021: "Credit: Stefan Pochmann", "Official answer", diary lines like "Nailed it." and "Hard to believe i wrote this only two weeks ago". 2025: `# not my solution. Still learning.`, `# had to look up solution`, "So i just cheated by using copy.deepcopy" (p133). Lowercase i, British spellings, the occasional "naïve".

**5. Drawing to understand**
2021: 79 self-made animation videos on static.ioloop.io across 24 pages, mermaid trees, ASCII trace tables, 7 photos of hand-drawn diagrams. 2025: `draw_tree`/`draw_graphviz`/`draw_linked_list` calls sitting in 44 solve files, sometimes left live inside the algorithm. Same learner, different instruments.

**6. The naming register**
Terse single letters for machinery (`d`, `q`, `c`, `h`, `l`/`r`), capitals for lookup structures (`D` for dicts, `G` for graphs, `S` for sets, `Q` for queues), snake_case that turns descriptive exactly when logic gets subtle (`po_root_ind`, `in_left_subtree`, `has_fresh_oranges`). LeetCode's camelCase is kept in the signature, never written voluntarily; in 2021 you nested `two_sum` inside `threeSum`. Type hints are whatever LeetCode gave you (`List[int]`, `Optional[TreeNode]`, zero lowercase `list[int]`); own helpers never get hints.

## What changed, 2021 → 2026

### Upgrades

- **`deque` arrived.** The single biggest upgrade. 2021 has zero deques in 200 pages; BFS was `q.pop(0)` on lists. Now it's a reflex, including converting input wholesale: `nums = deque(nums)` then popping both ends (p2562).
- **`Counter` became the default frequency tool.** 4 files in 2021; 36 files in 2025, including Counter algebra: `return rc - mc == {}` (p383), `for n in c1 & c2` (p350).
- **`@cache` replaced hand memos.** 2021 memoized through dict cells; now `@cache` sits on inner DP functions (p72, p1143). One fossil remains: `def brute_force(n, memo={})` (p1025, 2026).
- **The itertools vocabulary grew.** `accumulate` was already a 2021 favourite; `pairwise`, `compress`, `groupby`, `chain`, `combinations` joined it (11 files for pairwise, 31 for combinations, 2025).
- **Multi-criteria sorts with list-valued keys:** `nums.sort(key=lambda x: [c[x], -x])` (p1636) — not in the 2021 repertoire.

### Retirements

- **Boolean tuple indexing `(a, b)[cond]`** — the 2021 trademark, defended at length in `ternary conditionals.md` and used in real solves (`dfs((r, r+1)[c==8], (c+1,0)[c==8])`). Zero occurrences in 2025-26; real ternaries took over.
- **`~i` complement indexing** — evangelized in 2021 as "a sign of a mature and experienced developer", 9 files. Not seen once in the current samples.
- **namedtuple/dataclass for throwaway solves** — 2021 defined `Point`, `Interval`, `StackEntry` just to name fields; 2026 has one namedtuple (p994) and no dataclasses.
- **Abbreviated imports** (`defaultdict as ddict`, `heappush as hpush`) — gone.
- **Recursion on slices** mostly gave way to index recursion, though it resurfaces where it reads well (`DP(a[:-1], b[:-1])` under `@cache`, p72).

### New quirks that didn't exist in 2021

- `_max`/`_min`/`_sum` underscore-prefix to dodge builtins (26/11/13 files in 2025). The 2021 author happily shadowed `ascii`.
- `set([])` and `deque([])` empty initializers, and `set([...])` around list literals — 20 files, with zero set comprehensions all year.
- The `len(x) -1` spacing tic (space before the minus only), all over 2026: `j = len(numbers) -1` (p167), `return time -1` (p994). Often correct on the very next line.
- Both `res` and `ret` alive in one function (p17: `ret` is the path, `res` the answers).
- Assert walls comparing `== True` / `== False` explicitly (192 lines in 2025).
- Bare string literals as comments: `"it's a close"` as an expression statement inside a loop (p20).

### Never adopted, five years running

| Feature | Count across 633 solve files + wiki |
|---|---|
| walrus `:=` | 1 (p450, 2025) |
| `nonlocal` | 0 |
| `match` | 0 |
| set comprehensions | 0 in 2025-26 (2021 had a few) |
| f-strings inside solution logic | ~0 (harness only) |
| lowercase `list[int]` hints | 3 |

## How you explain things to yourself

The 2021 writeups show a stable explanation ritual: bullets of steps before code, code pasted in chunks with a paragraph after each, an ASCII trace table when a loop is confusing ("drawing these tables in ascii is probably the most effective and quickest method of all" — your words in `reduce.md`), a physical analogy when a concept is slippery (prefix sums as hopping in snow and landing on your own footprints; the merge-lists `current` pointer as an electrician rewiring), and a LaTeX complexity footer as a sign-off: `$$time = O(M \times N)$$`. The analogies are the part worth keeping: they are proven personal mnemonics, already tested on your own memory.

## What pythonical is good for now

Inventory: of 200 pages, ~125 are problem writeups (98 LeetCode, 22 Pramp, 5 EPI), ~32 are Python idiom notes, ~25 are CS theory notes, and the rest is stray (cubing, pyqt, blog). About 15 writeups are genuinely rich, nearly all with your own animation videos. Ranked by fit with the current system:

1. **Drill bank seeds.** The idiom pages are already drill-shaped and the drill bank has 3 entries for 63 nodes. `shifted zip.md`, `list index complement.md`, `dp array sum.md` (accumulate prefix sums), `max array from right.md`, the matrix rotation trio, and the complexity-drill pages (`n.md`, `sqrt(n).md`, ...) convert almost mechanically into `drills/<node-id>/` files with `DRILL:`/`TRAINS:` headers.
2. **`problems.json` note pointers.** The `note` field prints with the assignment. A one-line pointer like `see ~/dev/pythonical/subarray sum equals k.md` on the ~15 rich writeups puts your own 2021 explanation (snow-hops and all) in front of you exactly when the problem comes back around. Direct hits already in the graph: 560, 1, 200, 121, 2, 42.
3. **Pramp problems as fresh carriers.** `problems.json` accepts `misc/<name>` keys. The 22 Pramp problems (budget cuts, drone flight planner, word count engine, getting a different number, ...) are not on LeetCode, so they can't be answered from number-recognition — useful as honest checks that a technique transferred.
4. **Palace material.** The 79 videos and the physical analogies are ready-made drawer content for the Technique Palace: each analogy is a hook you already know works on you.
5. **Node audit.** You named your own patterns in 2021: "single bidirectional pass", "list index complement", "string contains all chars ordered". Worth diffing that list against `nodes.json` — any 2021 pattern with no node today is either missing from the graph or genuinely retired.

Not useful as evidence: `evidence.json` is append-only, keyed to solve files, and five-year-old reps would be long past STALE anyway. The wiki is reference and mnemonic material, not proof of current skill.

## Method

Four parallel readers: all 77 files matching 2026 in `solved/`; a systematic every-8th sample of the 556 files matching 2025, with grep counts run over all 556; ~65 pythonical pages weighted toward solves and idiom notes; and a full 200-page inventory plus a read of `graph/README.md` and the makefile to map plug-in points. Every claim above traces to a named file; counts are exact where a grep is cited and approximate where a sample is.
