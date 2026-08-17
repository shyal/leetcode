[![Run Tests](https://github.com/shyal/leetcode/actions/workflows/run-tests.yml/badge.svg)](https://github.com/shyal/leetcode/actions/workflows/run-tests.yml)

# Cracking Leetcode

I've recently come to the realization that leetcode was never about solving the problems, as i was trying to do in the past, but was always about cracking leetcode itself. Leetcoders often complain about only being able to remember a fixed number of solves and techniques, and their memory essentially functioning as an LRU cache.

My solution to this problem, in the past, was the use of Anki, and while Anki helped a lot, it created a problem of its own: it meant keeping a separate asset, and constantly having to work with both Anki and the actual learning + solving.

So, here's my new approach: i wondered, how about thinking of the core techniques behind each solve, and treating those like the key asset that needs to be kept solid, via spaced repetition. With the repo's tooling, can now run `make next` which scans my solve graph and evidence, finds fragile or stale nodes, and recommends what to work on next.

<!-- KG_MOVIE -->

![Technique graph growing solve by solve](https://shyal.s3.amazonaws.com/kg_movie_20260817021158.gif)

<!-- /KG_MOVIE -->

## It seems to be working

Looking at my last leetcode grind, roughly October and November 2025, i plateaued quickly, because i was doing high volume, and picking what to work on poorly. Now, since my latest resumption (August 2026) my volume is much smaller, yet i appear to have already broken my plateau. These are still early days, but it seems to be working.

<!-- PASS_PROB_CHART -->

![P(pass a mock) over time](https://shyal.s3.amazonaws.com/pass_probability_20260817021158.png)

<!-- /PASS_PROB_CHART -->

The scheduler really is fantastic. It has a constraint i really like: it only recommends a problem with a single fragile node in its (input) dependency graph. This is what Vygotsky calleds the "Zone of proximal development", while in language acquisition it is Krashen's "i+1" (comprehensible input one step beyond current level).

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

The condition is the same for each solve: a foundation of solid techniques, with one fragile or sale node. The problem exists only to reinforce the fragile or stale node.

## My forgetting curve

A memory decay curve is computed (duolingo style). It's fitted (`make curve`) regularly.

The model is power-law forgetting with a slip rate, P(recall) = (1−slip)·(1 + Δ/s)^(−β), where stability s grows with every clean rep and shrinks every time i struggle.

<!-- CURVE_CHART -->

![Fitted forgetting curve](https://shyal.s3.amazonaws.com/forgetting_curve_20260817021158.png)

<!-- /CURVE_CHART -->

<!-- POSITIONS_SVG -->
![Nodes sliding down their forgetting curves](https://shyal.s3.amazonaws.com/positions_20260817021158.svg)
<!-- /POSITIONS_SVG -->

The model also tracks its accuracy internally, by comparing its predictions with my actual performance.

<!-- CURVE_CALIBRATION_CHART -->

![Curve calibration](https://shyal.s3.amazonaws.com/curve_calibration_20260817021158.png)

<!-- /CURVE_CALIBRATION_CHART -->

## Solve rate

This is the daily solve rate.

<!-- SOLVES_CHART -->

![Solves Per Day (Full Repo History)](https://shyal.s3.amazonaws.com/solves_per_day_20260817021158.png)

<!-- /SOLVES_CHART -->

## Unique solve rate

This is the daily unique solve rate. This is because as complexity ramps up, questions will need to be revisited.

<!-- UNIQUES_CHART -->

![Unique Problems Solved Daily (Full Repo History)](https://shyal.s3.amazonaws.com/uniques_per_day_20260817021158.png)

<!-- /UNIQUES_CHART -->

## Contest progress

The progress bar is derived from the technique graph: every move scores solid = 1.0, stale = 0.5, fragile = 0.25, missing = 0, averaged. Staleness (i.e. how much i forget over time) is baked in — the bar only moves when i actually re-earn moves, not when time passes. The projected date comes from a small Claude call fed the graph summary.

<!-- CONTEST_PROGRESS -->

![Contest Readiness Progress (Ready by 2026-08-27)](https://shyal.s3.amazonaws.com/contest_progress_20260817021158.png)

<!-- /CONTEST_PROGRESS -->

Update: 05-Jul-2026

Rebuilt the readiness layer on the technique graph. The old bars measured elapsed time against a predicted date, which meant they filled up by me merely existing (lapses included) — they read 90% after a 10-week break. The new bars measure current skill with decay, and dropped honestly to ~55% contest / ~19% FAANG. The old history below still stands as a record of the LLM-guess era.

Update: 20-Oct-2025

Initially i was quite stunned by the estimator's tendency to output the exact same dates (without prior knowledge of its previous estimates). Then estimate dates started increasing dramatically. I investigated, and it appears that the estimator heavily weighs recent solves. Initially i was mixing easy and medium questions. The estimates started jumping because i stumbled on quite a few mediums in a row, then focussed on easy questions due to scheduling, and the model assumed this was a sign that my progress on mediums had completely plateaued.

I opted to tackle some of the 'learning' mediums in my history, and this appears to have had a dramatic effect in terms of clawing back those estimate dates.

In other words, these estimate variance charts are excellent indicators for complacency; if i start slacking by doing too many easies, or not tackling my 'learning' queue, estimates go up which is the clearest signal i could hope for.

## FAANG progress

Held to a stricter standard than contests: the bar is the fraction of technique moves that are fully SOLID (fresh evidence only — interviews demand instant recall, so stale doesn't count). Currently the focus of this repo is just fun, but this is an interesting metric regardless.

The projected date no longer comes from an LLM guess: `utils/kg_predict` runs a day-by-day simulation of how the picker would spend the hours — consolidate fragile moves, acquire missing ones, re-solve whatever the personal forgetting curve (`graph/curve.json`) says is about to go stale, then bank new mediums — with solve costs measured from my own git history. Ready = graph fully solid + enough distinct mediums banked + a polish block of timed sets and mocks.

<!-- FAANG_PROGRESS -->

![FAANG Interview Readiness Progress (Ready by 2026-10-10)](https://shyal.s3.amazonaws.com/faang_progress_20260817021158.png)

<!-- /FAANG_PROGRESS -->

## Estimate dates variance charts

I'm curious to see the amount of variance in the estimates, i.e whether they're stable over time.

<!-- CONTEST_VARIANCE_CHART -->

![Contest Readiness Projection Over Time](https://shyal.s3.amazonaws.com/contest_variance_20260817021158.png)

<!-- /CONTEST_VARIANCE_CHART -->

<!-- FAANG_VARIANCE_CHART -->

![FAANG Interview Readiness Projection Over Time](https://shyal.s3.amazonaws.com/faang_variance_20260817021158.png)

<!-- /FAANG_VARIANCE_CHART -->

The simulator's date gets its own series (recorded daily to `readiness.json` alongside the LLM's), so its stability can be compared against the LLM-guess era above:

<!-- FAANG_PREDICT_VARIANCE_CHART -->

![FAANG Readiness (Curve Simulator) Projection Over Time](https://shyal.s3.amazonaws.com/faang_predict_variance_20260817021158.png)

<!-- /FAANG_PREDICT_VARIANCE_CHART -->

## Topic readiness chart

Per-family readiness derived from the technique graph (same solid/stale/fragile weighting, averaged per node group), sorted strongest first.

<!-- CONTEST_TOPICS_CHART -->

![Topic Readiness](https://shyal.s3.amazonaws.com/contest_topics_readiness_20260817021158.png)

<!-- /CONTEST_TOPICS_CHART -->

# Leetcode flavoured environment

Leetcode's python environment is non-standard: it seems to have pretty much everyhing in modules like `itertools`, `functools`, `bisect`, `operator` etc. readily avialble without the need for imports.

This is really great as it makes writing solutions way faster, without the need to import anything.

This repo tries to reproduce this same environment with `utils/sitecustomize.py`. It also has a `stubs/builtins.pyi` for autocomplete to handle this custom import scheme, as well as all the utilities for trees, linked lists, pretty printing etc.

# Dependencies

```
python3 -m venv .venv
. .venv/bin/activate
cp utils/sitecustomize.py .venv/lib/python3.10/site-packages/
pip3 install requirements.txt
```

# Running

```
PYTHONPATH=./utils:${PYTHONPATH} python3 utils/runner.py
```

# Disclaimer

The utility scripts in this repo (for git log reports etc.), solve rate computations etc are LLM generated, so not production quality code (throw away scripts).

Some of the data generated i.e contest readiness dates, topics etc. is also LLM generated.

Solves are all mine. When they're not, i.e 'learning' commits etc. then credit to the author is given (which can include LLM generated solves, credit also given).
