[![Run Tests](https://github.com/shyal/leetcode/actions/workflows/run-tests.yml/badge.svg)](https://github.com/shyal/leetcode/actions/workflows/run-tests.yml)

# Cracking Leetcode

I've recently come to the realization that leetcode was never about solving the problems, as i was trying to do in the past, but was always about cracking leetcode itself. Leetcoders often complain about only being able to remember a fixed number of solves and techniques, and their memory essentially functioning as an LRU cache.

My solution to this problem, in the past, was the use of Anki, and while Anki helped a lot, it created a problem of its own: it meant keeping a separate asset, and constantly having to work with both Anki and the actual learning + solving. This approach felt heavy. In November 2025, i started dumping my solve history in an LLM's context, and asking for what to work on next. This was a leaner approach, however in retrospect, although the scheduling felt good, it wasn't.

So, here's my new approach: i decided on a new thesis: to focus on the core techniques behind each solve, and treat those like the key asset that needs to be kept solid, via spaced repetition. With the repo's tooling, i can now run `make next` which scans my solve graph and evidence, finds fragile or stale nodes, and recommends what to work on next.

<!-- KG_MOVIE -->

![Technique graph growing solve by solve](https://shyal.s3.amazonaws.com/kg_movie_20260826030136.svg)

<!-- /KG_MOVIE -->

All the solves before the blue section of the timeline were done with poor scheduling. The inefficiency is evidenced by the nodes turning stale (orange) and fragile (red) like a Christmas tree. Then, once we enter the blue section of the timeline, they all turn green within a matter of a week.

## It seems to be working

Looking at my last leetcode grind, roughly October and November 2025, i plateaued quickly, because i was doing high volume, and picking what to work on poorly. Now, since my latest resumption (August 2026), my volume is much smaller, yet i appear to have already broken my plateau. These are still early days, but it seems to be working.

<!-- PASS_PROB_CHART -->

![P(pass a mock) over time](https://shyal.s3.amazonaws.com/pass_probability_20260826030136.svg)

<!-- /PASS_PROB_CHART -->

The same story with effort as the x axis. A plateau is a long flat slog: hundreds of new problems that buy nothing, because they only exercise ground i already hold. A consolidation is a short, nearly vertical climb: far fewer solves, mostly re-solves, repairing stale ground.

<!-- YIELD_CHART -->

![What a solve buys](https://shyal.s3.amazonaws.com/yield_20260826030136.svg)

<!-- /YIELD_CHART -->

The green bars in the chart below show **consolidation** periods: times when P is either flat, wobbly, or sloping downwards, with many resolves, as well as drills being either added or reviewed. These are periods spent building the foundations rather than trying to cover new solving ground. These periods, IFF sustained with optimal scheduling, should precede P moving up violently.

<!-- YIELD_TIME_CHART -->

![Two kinds of sideways](https://shyal.s3.amazonaws.com/yield_time_20260826030136.svg)

<!-- /YIELD_TIME_CHART -->

<!-- MOCK_DIST_CHART -->

![Simulated mock outcomes over time](https://shyal.s3.amazonaws.com/mock_dist_20260826030136.svg)

<!-- /MOCK_DIST_CHART -->

<!-- MOCK_SWARM_CHART -->

![Individual simulated mocks over time](https://shyal.s3.amazonaws.com/mock_swarm_20260826030136.svg)

<!-- /MOCK_SWARM_CHART -->

<!-- MOCK_BLAME_CHART -->

![Why simulated mocks fail, over time](https://shyal.s3.amazonaws.com/mock_blame_20260826030136.svg)

<!-- /MOCK_BLAME_CHART -->

The scheduler really is fantastic. It has a constraint i really like: it only recommends a problem with a single fragile node in its (input) dependency graph. This is what Vygotsky called the "Zone of proximal development", while in language acquisition it is Krashen's "i+1" (comprehensible input one step beyond current level).

The condition is the same for each solve: a foundation of solid techniques, with one fragile or stale node. The problem exists only to reinforce the fragile or stale node.

## My forgetting curve

A memory decay curve is computed (Duolingo style). It's fitted (`make curve`) regularly.

The model is power-law forgetting with a slip rate, P(recall) = (1−slip)·(1 + Δ/s)^(−β), where stability s grows with every clean rep and shrinks every time i struggle.

<!-- POSITIONS_SVG -->

![Nodes sliding down their forgetting curves](https://shyal.s3.amazonaws.com/positions_20260826030136.svg)

<!-- /POSITIONS_SVG -->

The model also tracks its accuracy internally, by comparing its predictions with my actual performance.

<!-- CURVE_CALIBRATION_CHART -->

![Curve calibration](https://shyal.s3.amazonaws.com/curve_calibration_20260826030136.svg)

<!-- /CURVE_CALIBRATION_CHART -->

<!-- REVIEW_TIMING_CHART -->

![Was each review on time?](https://shyal.s3.amazonaws.com/review_timing_20260826030136.svg)

<!-- /REVIEW_TIMING_CHART -->

i had a hunch my solve times were bimodal: either the move fires and the problem falls out in minutes, or it grinds. The clock says no. Solve times come from the timing trailer in each solve commit (single-solve commits only; the day-one bulk import stamped 109 old files with one shared timestamp, so those are dropped), and the distribution is one smooth lognormal around 7 minutes. Whatever a grind feels like from inside, there are no clusters.

What the clock does see is two drivers, and they were my gut ranking before i ran the numbers: repetition, then connectivity. Meet the same problem again within a month and i run at 0.76x my previous attempt on it; after a month away the edge is mostly gone. Averages can't show this (the problems i clear fast never earn a second serving, only the ones that hurt come back), so each re-solve is paired against my own previous attempt at that problem. The second driver: problems built from widely shared moves run faster than same-rated problems built from rare ones, 4.6m vs 6.3m on easies, 11.7m vs 20.5m on mediums. A move that fifty problems keep exercising never gets a chance to go cold; the rare moves are the expensive ones. Position in the concept taxonomy does nothing (prereq degree came out at zero in the regression): what matters is how many problems rehearse the move, not how central it looks on paper.

<!-- SOLVETIME_CHART -->

![The two drivers of solve time](https://shyal.s3.amazonaws.com/solvetime_20260826030136.svg)
<!-- /SOLVETIME_CHART -->

The connectivity effect, zoomed in. Every timed solve as a dot, against how many problems in the bank share its moves. The scatter is honest about the size of the effect: the running medians sit flat until a walk's moves are shared by roughly thirty problems, then bend down. It isn't a smooth discount, it's a threshold: moves need a critical mass of carriers before the free rehearsal shows up in the clock.

<!-- CONNECTIVITY_CHART -->

![Move connectivity vs solve time](https://shyal.s3.amazonaws.com/connectivity_20260826030136.svg)
<!-- /CONNECTIVITY_CHART -->

The payoff metric is problems in reach: a problem is in reach when every move in its walk is currently solid. This replays today's walked problems against each day's historical node states, so the curve measures my skill moving under a fixed yardstick, not the catalog growing.

Two lines now. The blue one counts only evidenced walks: walks extracted from code i actually wrote. The purple one is the whole bank of 3092 free problems, using LLM-drafted walks for everything i haven't solved yet (drafts score precision 0.80 / recall 0.75 against 50 evidenced walks, so the purple line runs a little optimistic). Guesses never mix into the blue line. The dip in the middle is the point of the whole repo: reach isn't a ratchet, volume without defense bleeds out at catalog scale.

<!-- REACH_CHART -->

![Problems in reach](https://shyal.s3.amazonaws.com/reach_20260826030136.svg)

<!-- /REACH_CHART -->

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

![Solves Per Day (Full Repo History)](https://shyal.s3.amazonaws.com/solves_per_day_20260826030136.png)

<!-- /SOLVES_CHART -->

## Unique solve rate

This is the daily unique solve rate, tracked separately because as complexity ramps up, questions will need to be revisited.

<!-- UNIQUES_CHART -->

![Unique Problems Solved Daily (Full Repo History)](https://shyal.s3.amazonaws.com/uniques_per_day_20260826030136.png)

<!-- /UNIQUES_CHART -->

## Readiness

Everything here comes from the Monte Carlo behind the mock charts up top. Ready means a 50% central pass rate; each bar shows today's rate against that mark, and the date in the title is when the forward simulation crosses it. Nothing is stored: the projection chart replays every day since the repo started from the evidence visible on that day. The old LLM date guesses are retired - they were garbage - and their stored snapshots are gone with them (git history has the file if anyone cares).

Contest bar: today's central P(clear a single hard).

<!-- CONTEST_PROGRESS -->

![Contest Readiness Progress (Ready by 2026-11-28, in 94 days)](https://shyal.s3.amazonaws.com/contest_progress_20260826030136.png)

<!-- /CONTEST_PROGRESS -->

FAANG bar: today's central P(pass a full onsite: 2 easies + 2 mediums + at least one hard).

<!-- FAANG_PROGRESS -->

![FAANG Interview Readiness Progress (Ready by 2027-02-04 at 1.7h/day, in 162 days)](https://shyal.s3.amazonaws.com/faang_progress_20260826030136.png)

<!-- /FAANG_PROGRESS -->

Every projected date is recorded daily, so one chart tracks whether the projections are stable. A flat line means the model isn't fooled by what i did that week; drift upward means i'm slacking. The third line is `utils/kg_predict`, a day-by-day simulation of how the picker would spend the hours; its date answers "when is the work done" (graph fully solid + enough mediums banked + a polish block), not "when would i pass", which is why it lands much earlier.

<!-- READINESS_PROJECTION_CHART -->

![Projected ready dates over time](https://shyal.s3.amazonaws.com/readiness_projection_20260826030136.png)

<!-- /READINESS_PROJECTION_CHART -->

As you can see, these readiness projections are currently highly unreliable. The first issue is the inconsistency in practice (with a huge gap between September 2025 and August 2026), and secondly it's because the monte carlo simulation tries to guess my progress. It's rolling dice with an incomplete picture.

Getting a more accurate picture would mean generating solutions for all leetcode problems, and building the currently unbuilt portions of the graph for it, something that can be done, but would not be _my_ graph, so would be a rather pointless activity.

Towards the end of August, these prediction variance lines should flatten out, on average, but will continue to whiplash.

This is because the projections use two noisy inputs: the hours assumption is my mean pace in the last 28 days, extrapolated forever. Secondly, since my resumption in August the window is refilling with consistent days, so by the end of the month that input settles.

I find the predictions to be honest. At 2 hours of solving a day, a 50% pass rate for a FAANG mock at any company feels both correct and realistic. This is a much taller hill to climb than picking one company's mock exam, and cramming the solutions. This is a prediction for any 2 easy 2 medium and 1 hard mock exam, with questions picked at random.

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

Everything currently charted is measured or simulated; the retired LLM-guessed readiness dates only survive in git history.

Solves are all mine. When they're not, i.e. 'learning' commits etc., then credit to the author is given (which can include LLM generated solves, credit also given).
