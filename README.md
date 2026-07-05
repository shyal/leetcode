[![Run Tests](https://github.com/shyal/leetcode/actions/workflows/run-tests.yml/badge.svg)](https://github.com/shyal/leetcode/actions/workflows/run-tests.yml)

# Leetcode grind

This repo contains a log of my >= 2025 leetcode solves. I was clobbering together the helper scripts for this repo between my solves, so solve times don't go all the way back. Likewise for readiness and topic estimates, they don't go all the way back, however enough data should get collected for progress charts to get increasingly interesting as time goes on.

Originally i prompted Grok with my entire solve history for recommendations, which established a feedback loop: it recommended what to work on, then saw how i did. That architecture has since been replaced by a technique knowledge graph (`graph/`): every solve is distilled (by Claude, once, at ingest) into evidence about which atomic *moves* the code actually exercised — `streaming-ask-then-record`, `monotonic-stack`, etc. A problem is a walk through the graph of moves; mastery is derived at query time from evidence dates, so skills go stale if i don't revisit them, exactly like real memory.

Claude coaches on top of this: `make next` deterministically picks the next problem (consolidate fragile moves first, spaced re-solves second, one new move at a time), preflight-gates it so a problem never requires more than one untrained move, prescribes warm-up drills from a growing self-authored drill bank (`drills/`), and draws the problem's full dependency tree of techniques. The LLM judges code; the graph remembers; arithmetic decides what's next.

I am thrilled with the use of LLMs as learning assistants. The recommendations are of extremely high quality, and the reasoning as to why i should work on what is extremely coherent.

I also could not be happier with the use of Git + Python + LLMs, and believe this workflow (for developers) is not only incredibly versatile, but also extremely powerful.

This approach can be applied to learning any topic.

Here are some little charts, generated from the git log.

![Problem Grid Animation](https://shyal.s3.amazonaws.com/problem_grid_20260705093530.gif)

## Solve rate

This is the daily solve rate.

![Solves Per Day (Full Repo History)](https://shyal.s3.amazonaws.com/solves_per_day_20260705093530.png)

## Unique solve rate

This is the daily unique solve rate. This is because as complexity ramps up, questions will need to be revisited.

![Unique Problems Solved Daily (Full Repo History)](https://shyal.s3.amazonaws.com/uniques_per_day_20260705093530.png)

## Contest progress

The progress bar is derived from the technique graph: every move scores solid = 1.0, stale = 0.5, fragile = 0.25, missing = 0, averaged. Staleness (i.e. how much i forget over time) is baked in — the bar only moves when i actually re-earn moves, not when time passes. The projected date comes from a small Claude call fed the graph summary.

![Contest Readiness Progress (Ready by 2026-08-16)](https://shyal.s3.amazonaws.com/contest_progress_20260705093530.png)

Update: 05-Jul-2026

Rebuilt the readiness layer on the technique graph. The old bars measured elapsed time against a predicted date, which meant they filled up by me merely existing (lapses included) — they read 90% after a 10-week break. The new bars measure current skill with decay, and dropped honestly to ~55% contest / ~19% FAANG. The old history below still stands as a record of the LLM-guess era.

Update: 20-Oct-2025

Initially i was quite stunned by the estimator's tendency to output the exact same dates (without prior knowledge of its previous estimates). Then estimate dates started increasing dramatically. I investigated, and it appears that the estimator heavily weighs recent solves. Initially i was mixing easy and medium questions. The estimates started jumping because i stumbled on quite a few mediums in a row, then focussed on easy questions due to scheduling, and the model assumed this was a sign that my progress on mediums had completely plateaued.

I opted to tackle some of the 'learning' mediums in my history, and this appears to have had a dramatic effect in terms of clawing back those estimate dates.

In other words, these estimate variance charts are excellent indicators for complacency; if i start slacking by doing too many easies, or not tackling my 'learning' queue, estimates go up which is the clearest signal i could hope for.

## FAANG progress

Held to a stricter standard than contests: the bar is the fraction of technique moves that are fully SOLID (fresh evidence only — interviews demand instant recall, so stale doesn't count). Currently the focus of this repo is just fun, but this is an interesting metric regardless.

![FAANG Interview Readiness Progress (Ready by 2026-10-18)](https://shyal.s3.amazonaws.com/faang_progress_20260705093530.png)

## Estimate dates variance charts

I'm curious to see the amount of variance in the estimates, i.e whether they're stable over time.

![Contest Readiness Projection Over Time](https://shyal.s3.amazonaws.com/contest_variance_20260705093530.png)

![FAANG Interview Readiness Projection Over Time](https://shyal.s3.amazonaws.com/faang_variance_20260705093530.png)

## Topic readiness chart

Per-family readiness derived from the technique graph (same solid/stale/fragile weighting, averaged per node group), sorted strongest first.

![Topic Readiness](https://shyal.s3.amazonaws.com/contest_topics_readiness_20260705093530.png)

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