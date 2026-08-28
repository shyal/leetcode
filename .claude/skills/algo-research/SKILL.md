---
name: algo-research
description: Look up how a technique or leetcode problem is actually explained before building drills, giving hints, or writing walkthroughs. Local cache first (research/), web fallbacks second. Use whenever the drill-building rule demands editorial/community research.
---

Research a leetcode problem or technique from real writeups, never from your
own head. This serves the "Building drills" rule in CLAUDE.md: read the
intuition sections, build from those.

## Local cache (check first, in this order)

All under `research/` (gitignored, ~92MB):

1. **Per-problem editorials** - `research/doocs-leetcode/solution/*/NNNN.*/README_EN.md`
   (4-digit zero-padded number, e.g. `*/0979.*/README_EN.md`). 4034 problems:
   statement, approach intuition, complexity, multi-language code.
   Find one with: `ls research/doocs-leetcode/solution/*/0543.*/`
2. **Technique canon** - `research/cp-algorithms/src/<category>/<topic>.md`
   (categories: algebra, combinatorics, data_structures, dynamic_programming,
   game_theory, geometry, graph, num_methods, others, schedules, sequences,
   string). The canonical treatment of named algorithms.
3. **Curated modules** - `research/usaco-guide/content/<1_General|2_Bronze|3_Silver|4_Gold|5_Plat|6_Advanced>/**/*.mdx`.
   Technique modules with worked intuition, ramped by level.
4. **Books** - `research/books/`, read with the Read tool's `pages` param:
   - `competitive-programmers-handbook.pdf` (Laaksonen, CPH) - short, chapter per technique
   - `principles-of-algorithmic-problem-solving.pdf` (Sannemo) - intuition-first
   - `algorithms-jeff-erickson.pdf` (Erickson) - deep treatments, recursion/DP/graphs

## Community solutions (the Solutions tab, usually better than editorials)

`utils/lc_solutions` hits leetcode's public graphql directly, no auth:

    utils/lc_solutions 543                 # top-voted solution titles
    utils/lc_solutions 543 --read 1-3      # full markdown of ranks 1 to 3
    utils/lc_solutions 543 --tag python3   # filter by tag
    utils/lc_solutions 543 --order HOT     # or MOST_RECENT

Every --read is saved under `research/lc-solutions/<num>.<slug>/<topicId>.md`,
so check there before refetching. Read a couple of top-voted writeups, not
just one. Keep usage per-problem and polite; do not bulk-crawl.

The operator's recipe: filter `--tag python --tag python3`, then hunt for the
CLEANEST solution in the list, not the most upvoted one. Benchmark author:
StefanPochmann (`--author StefanPochmann`, with or without a problem) - his
solutions are a different level of clean; note his pre-2019 classics were not
migrated into this API, only the per-problem top-voted list may carry them.

## Web fallbacks (when the cache misses or you need a second angle)

- `https://algo.monster/liteproblems/<num>` - free per-problem intuition writeups, WebFetch works
- `https://walkccc.me/LeetCode/problems/<num>/` - concise solutions, all problems
- LeetCode's own editorial + top Discuss posts for the carrier problem
- Codeforces blog entries - fetch via `https://web.archive.org/web/<url>` (direct fetch is blocked)
- neetcode.io - good content but JS-rendered; WebFetch usually fails, use search snippets instead

## Rules

- Read the INTUITION sections, not just code. A drill or hint built without
  them is worthless (CLAUDE.md, settled 2026-08-26).
- Multiple sources beat one: cross-check the approach across at least two
  writeups before treating it as canonical.
- Coaching rules still apply: research feeds drills, hints and walkthroughs;
  it is never an excuse to reveal answers unasked.
- Refresh the cache occasionally: `git -C research/doocs-leetcode pull`,
  same for `cp-algorithms` and `usaco-guide`.
