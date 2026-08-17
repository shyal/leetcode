[![Run Tests](https://github.com/shyal/leetcode/actions/workflows/run-tests.yml/badge.svg)](https://github.com/shyal/leetcode/actions/workflows/run-tests.yml)

# Cracking Leetcode

I've recently come to the realization that leetcode was never about solving the problems, as i was trying to do in the past, but was always about cracking leetcode itself. Leetcoders often complain about only being able to remember a fixed number of solves and techniques, and their memory essentially functioning as an LRU cache.

My solution to this problem, in the past, was the use of Anki, and while Anki helped a lot, it created a problem of its own: it meant keeping a separate asset, and constantly having to work with both Anki and the actual learning + solving. This approach felt heavy. In November 2025, i started dumping my solve history in an LLM's context, and asking for what to work on next. This was a leaner approach, however in retrospect, although the scheduling felt good, it wasn't.

So, here's my new approach: i decided on a new thesis: to focus on the core techniques behind each solve, and treat those like the key asset that needs to be kept solid, via spaced repetition. With the repo's tooling, i can now run `make next` which scans my solve graph and evidence, finds fragile or stale nodes, and recommends what to work on next.

<!-- KG_MOVIE -->

![Technique graph growing solve by solve](https://shyal.s3.amazonaws.com/kg_movie_20260817130754.svg)

<!-- /KG_MOVIE -->

All the solves before the blue section of the timeline were done with poor scheduling. The inefficiency is evidenced by the nodes turning stale (orange) and fragile (red) like a Christmas tree. Then, once we enter the blue section of the timeline, they all turn green within a matter of a week.

## It seems to be working

Looking at my last leetcode grind, roughly October and November 2025, i plateaued quickly, because i was doing high volume, and picking what to work on poorly. Now, since my latest resumption (August 2026), my volume is much smaller, yet i appear to have already broken my plateau. These are still early days, but it seems to be working.

<!-- PASS_PROB_CHART -->

![P(pass a mock) over time](https://shyal.s3.amazonaws.com/pass_probability_20260817130754.svg)

<!-- /PASS_PROB_CHART -->

<!-- MOCK_DIST_CHART -->

![Simulated mock outcomes over time](https://shyal.s3.amazonaws.com/mock_dist_20260817130754.svg)

<!-- /MOCK_DIST_CHART -->

<!-- MOCK_SWARM_CHART -->

![Individual simulated mocks over time](https://shyal.s3.amazonaws.com/mock_swarm_20260817130754.svg)

<!-- /MOCK_SWARM_CHART -->

<!-- MOCK_BLAME_CHART -->

![Why simulated mocks fail, over time](https://shyal.s3.amazonaws.com/mock_blame_20260817130754.svg)

<!-- /MOCK_BLAME_CHART -->

The scheduler really is fantastic. It has a constraint i really like: it only recommends a problem with a single fragile node in its (input) dependency graph. This is what Vygotsky called the "Zone of proximal development", while in language acquisition it is Krashen's "i+1" (comprehensible input one step beyond current level).

The condition is the same for each solve: a foundation of solid techniques, with one fragile or stale node. The problem exists only to reinforce the fragile or stale node.

## My forgetting curve

A memory decay curve is computed (Duolingo style). It's fitted (`make curve`) regularly.

The model is power-law forgetting with a slip rate, P(recall) = (1−slip)·(1 + Δ/s)^(−β), where stability s grows with every clean rep and shrinks every time i struggle.

<!-- POSITIONS_SVG -->

![Nodes sliding down their forgetting curves](https://shyal.s3.amazonaws.com/positions_20260817130754.svg)

<!-- /POSITIONS_SVG -->

The model also tracks its accuracy internally, by comparing its predictions with my actual performance.

<!-- CURVE_CALIBRATION_CHART -->

![Curve calibration](https://shyal.s3.amazonaws.com/curve_calibration_20260817130754.svg)

<!-- /CURVE_CALIBRATION_CHART -->

<!-- REVIEW_TIMING_CHART -->

![Was each review on time?](https://shyal.s3.amazonaws.com/review_timing_20260817130754.svg)

<!-- /REVIEW_TIMING_CHART -->

## The zone of proximal development

It can be visualized in a single image, in the graph. Running `make next` shows me something like this in my terminal:

```
make next

560. Subarray Sum Equals K
https://leetcode.com/problems/subarray-sum-equals-k/
  Move                          Status    Last evidence
  prefix-sums                   SOLID     2026-08-07
  streaming-ask-then-record     SOLID     2026-08-09
  derived-key-lookup            SOLID     2026-08-08
  streaming-accumulate-pairs    SOLID     2026-07-05
  prefix-sum-hashmap            STALE     2025-10-23

```

![560 input tree, one stale node](https://shyal.s3.amazonaws.com/zpd_560_input_tree.png)

## Solve rate

This is the daily solve rate.

<!-- SOLVES_CHART -->

![Solves Per Day (Full Repo History)](https://shyal.s3.amazonaws.com/solves_per_day_20260817130754.png)

<!-- /SOLVES_CHART -->

## Unique solve rate

This is the daily unique solve rate, tracked separately because as complexity ramps up, questions will need to be revisited.

<!-- UNIQUES_CHART -->

![Unique Problems Solved Daily (Full Repo History)](https://shyal.s3.amazonaws.com/uniques_per_day_20260817130754.png)

<!-- /UNIQUES_CHART -->

## Readiness

Everything here comes from the Monte Carlo behind the mock charts up top. Ready means a 50% central pass rate; each bar shows today's rate against that mark, and the date in the title is when the forward simulation crosses it. The old LLM date guesses are retired - they were garbage - though their history stays in `data/readiness.json`.

Contest bar: today's central P(clear a single hard).

<!-- CONTEST_PROGRESS -->

![Contest Readiness Progress (Ready by 2027-01-14)](https://shyal.s3.amazonaws.com/contest_progress_20260817130754.png)

<!-- /CONTEST_PROGRESS -->

FAANG bar: today's central P(pass a full onsite: 2 easies + 2 mediums + at least one hard).

<!-- FAANG_PROGRESS -->

![FAANG Interview Readiness Progress (Ready by 2027-09-11 at 1.7h/day)](https://shyal.s3.amazonaws.com/faang_progress_20260817130754.png)

<!-- /FAANG_PROGRESS -->

Every projected date is recorded daily, so one chart tracks whether the projections are stable. A flat line means the model isn't fooled by what i did that week; drift upward means i'm slacking. The third line is `utils/kg_predict`, a day-by-day simulation of how the picker would spend the hours; its date answers "when is the work done" (graph fully solid + enough mediums banked + a polish block), not "when would i pass", which is why it lands much earlier.

<!-- READINESS_PROJECTION_CHART -->

![Projected ready dates over time](https://shyal.s3.amazonaws.com/readiness_projection_20260817130754.png)

<!-- /READINESS_PROJECTION_CHART -->

# Leetcode flavoured environment

Leetcode's python environment is non-standard: it seems to have pretty much everything in modules like `itertools`, `functools`, `bisect`, `operator` etc. readily available without the need for imports.

This is really great as it makes writing solutions way faster, without the need to import anything.

This repo tries to reproduce this same environment with `utils/sitecustomize.py`. It also has a `stubs/builtins.pyi` for autocomplete to handle this custom import scheme, as well as all the utilities for trees, linked lists, pretty printing etc.

# Dependencies

```
python3 -m venv .venv
. .venv/bin/activate
cp utils/sitecustomize.py .venv/lib/python3.10/site-packages/
pip3 install -r requirements.txt
```

# Running

```
PYTHONPATH=./utils:${PYTHONPATH} python3 utils/runner.py
```

# Disclaimer

The utility scripts in this repo (for git log reports etc.), solve rate computations etc. are LLM generated, so not production quality code (throw away scripts).

Some of the historical data in `data/readiness.json` (the retired readiness-date series) was LLM generated; everything currently charted is measured or simulated.

Solves are all mine. When they're not, i.e. 'learning' commits etc., then credit to the author is given (which can include LLM generated solves, credit also given).
