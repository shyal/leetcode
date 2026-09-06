[![Run Tests](https://github.com/shyal/leetcode/actions/workflows/run-tests.yml/badge.svg)](https://github.com/shyal/leetcode/actions/workflows/run-tests.yml) <!-- ELO_BADGE -->![Elo](https://shyal.s3.amazonaws.com/elo_badge_20260906043458.svg)<!-- /ELO_BADGE --> <!-- STREAK_BADGE -->![Streak](https://shyal.s3.amazonaws.com/streak_badge_20260906043458.svg)<!-- /STREAK_BADGE -->

# Cracking Leetcode

I've recently come to the realization that leetcode was never about solving the problems, as i was trying to do in the past, but was always about cracking leetcode itself. Leetcoders often complain about only being able to remember a fixed number of solves and techniques, and their memory essentially functioning as an LRU cache [[1]](https://leetcode.com/discuss/study-guide/3000556/Forget-the-logic-and-structure-of-a-problem-that-I-solved-before.) [[2]](https://leetcode.com/discuss/study-guide/3000556/Forget-the-logic-and-structure-of-a-problem-that-I-solved-before.) [[3]](https://leetcode.com/discuss/general-discussion/1592466/tips-on-how-to-not-forgetting-solutionsapproaches/) [[4]](https://leetcode.com/discuss/general-discussion/1099326/how-you-guys-remember-leetcode-questions-during-the-interview-any-tips/) [[5]](https://leetcode.com/discuss/general-discussion/451042/suggest-best-way-to-remember-a-solution) [[6]](https://leetcode.com/discuss/post/8345508/) [[7]](https://leetcode.com/discuss/post/8351692/) [[8]](https://www.quora.com/Even-if-I-solve-200-algorithm-questions-on-LeetCode-and-think-that-I-understood-solutions-after-2-months-without-solving-any-question-when-I-try-to-solve-them-again-I-cant-remember-some-of-the-solutions-What-should) [[9]](https://news.ycombinator.com/item?id=46203581) [[10]](https://dev.to/anjandutta/i-failed-5-coding-interviews-despite-solving-200-leetcode-problems-heres-what-fixed-it-4f5c) [[11]](https://dev.to/neelbansal/the-leetcode-amnesia-problem-and-how-i-fixed-it-4i7n) [[12]](https://dev.to/alex_hunter_44f4c9ed6671e/system-design-for-your-brain-architecting-a-scalable-leetcode-retention-strategy-3aah).

My solution to this problem, in the past, was the use of Anki, and while Anki helped a lot, it created a problem of its own: it meant keeping a separate asset, and constantly having to work with both Anki and the actual learning + solving. This approach felt heavy. In November 2025, i started dumping my solve history in an LLM's context, and asking for what to work on next. This was a leaner approach, however in retrospect, although the scheduling felt good, it wasn't.

So, here's my new approach: i decided on a new thesis: to focus on the core techniques behind each solve, and treat those like the key asset that needs to be kept solid, via spaced repetition. Of course classifying thousands of solves into a personal knowledge graph was always the answer to pick the signal from the noise. It's just that up until now, it wasn't feasible without significant resources. Well, now it is feasible, for a douzen dollars (i'll write up on the extraction process soon). So with the repo's tooling, i can now run `make next` which scans my solve graph and evidence, finds fragile or stale nodes, and recommends what to work on next. If nothing needs reviewing, then `make next` goes into exploration mode with the goal of maximizing problem rechability.

<!-- KG_3D -->

![The technique graph in three dimensions, turning while the history replays](https://shyal.s3.amazonaws.com/kg_3d_20260906043458.svg)

<!-- /KG_3D -->

I like to think of this process as a compression algorithm. Lots of leetcode problems are just variations of one another, or variations around core themes that don't emerge easily by simply trying to solve. This readme is changing a lot as the tooling is in active development. But at the time of writing, <!-- N_NODES -->99<!-- /N_NODES --> nodes are enough to describe the whole bank of <!-- N_BANK -->3091<!-- /N_BANK --> free problems (the drafted walks score precision 0.80 / recall 0.75 against my evidenced ones), and the model expects <!-- N_REACH_TODAY -->~2400<!-- /N_REACH_TODAY --> of them to be solvable today. i'm hoping to demonstrate that the compression + optimizer works.

It is worth noting that the topology of the graph changes continually: each new node is a mental model i was missing, and the graph grows as those gaps turn up. To continue with the compression analogy, the compression is lossy. Compression artifacts are detected via residuals, and resolution is increased for those nodes only via node splits.

<!-- KG_COMPRESSION -->

![One tile per node, one cell per problem or drill; tiles split as nodes are added, cells light as they are solved](https://shyal.s3.amazonaws.com/kg_compression_20260906043458.svg)

<!-- /KG_COMPRESSION -->

It is also worth noting that everything connects to everything, and everything can depend on anything. The first class citizens in the graph are:

- Leetcode problems.
- Drills (tiny problems i create myself, each training one atomic technique).
- Nodes (single technique class, like prefix-sums or floyd-cycle).
- Groups (like sql or trees).

A problem's solution is a combination of several nodes, in a directed dependency graph. Problems can depend on an input dependency graph of nodes, on other problems and on drills. Nodes themselves can also depend on a dependency graph of drills. Problems that are solved in unpredicted ways are recorded as alternate walks.

<!-- KG_FULL -->

![Every node, problem and drill with every edge, each solve blinking its vertex](https://shyal.s3.amazonaws.com/kg_full_20260906043458.svg)

<!-- /KG_FULL -->

After each solve a judge runs, reads my submitted code + notes, and records the walk i took. Per node it records:

- a verdict: clean or struggled
- an assist level, from my notes only: none, hint, walkthrough or learning

This means that failures are granular, and only affect the pertinent nodes, not the whole input dependency tree.

<!-- KG_MOVIE -->

![Technique graph growing solve by solve](https://shyal.s3.amazonaws.com/kg_movie_20260906043458.svg)

<!-- /KG_MOVIE -->

All the solves before the blue section of the timeline were done with poor scheduling. The inefficiency is evidenced by the nodes turning stale (orange) and fragile (red) like a Christmas tree. Then, once we enter the blue section of the timeline, the nodes start turning green rapidly (quick disclaimer, the scheduler has been starved throughout August 2026 due to deadlocks. This how now been fixed, so i'm expecting a lot of green September onwards).

## It seems to be working

Looking at my last leetcode grind, roughly October and November 2025, i plateaued quickly, because i was doing high volume, and picking what to work on poorly. Now, since my latest resumption (August 2026), my volume is much smaller, yet i appear to have already broken my plateau. These are still early days, but it seems to be working.

<!-- PASS_PROB_CHART -->

![P(pass a mock) over time](https://shyal.s3.amazonaws.com/pass_probability_20260906043458.svg)

<!-- /PASS_PROB_CHART -->

<!-- MOCK_SWARM_CHART -->

![Individual simulated mocks over time](https://shyal.s3.amazonaws.com/mock_swarm_20260906043458.svg)

<!-- /MOCK_SWARM_CHART -->

<!-- MOCK_BLAME_CHART -->

![Share of simulated problems failed, by group](https://shyal.s3.amazonaws.com/mock_blame_20260906043458.svg)

<!-- /MOCK_BLAME_CHART -->

The scheduler really is fantastic. It has a constraint i really like: it only recommends a problem with a single fragile node in its (input) dependency graph. This is what Vygotsky called the "Zone of proximal development", while in language acquisition it is Krashen's "i+1" (comprehensible input one step beyond current level).

The condition is the same for each solve: a foundation of solid techniques, with one fragile or stale node. The problem exists only to reinforce the fragile or stale node.

## My forgetting curve

A memory decay curve is computed (Duolingo style). It's fitted (`make curve`) regularly.

The model is power-law forgetting with a slip rate, P(recall) = (1−slip)·(1 + Δ/s)^(−β), where stability s grows with every clean rep and shrinks every time i struggle.

<!-- POSITIONS_SVG -->

![Nodes sliding down their forgetting curves](https://shyal.s3.amazonaws.com/positions_20260906043458.svg)

<!-- /POSITIONS_SVG -->

The model also tracks its accuracy internally, by comparing its predictions with my actual performance.

<!-- CURVE_CALIBRATION_CHART -->

![Curve calibration](https://shyal.s3.amazonaws.com/curve_calibration_20260906043458.svg)

<!-- /CURVE_CALIBRATION_CHART -->

The lines below are 'residuals': groups of nodes moving up and down based on whether i perform better than the model predicts. The fact they roughly remain in the -2 to +2 band means the problem compression, combined with the derived forgetting curves is working as expected (the curves drop quite a bit in August 2026, because the scheduler was getting starved due to deadlocks etc. This has now been fixed).

Groups that fall off the chart (below -2) for a portion of time likely need looking into. The process is usually finding the problematic node, then the drills or problems inside it, then node splitting the node: creating a new node for those problems, and possibly some drills. To continue with the compression analogy: those are compression artifacts, and the node splitting boosts the resolution for that section of the graph.

<!-- RESIDUALS_CHART -->

![Residuals per group over time](https://shyal.s3.amazonaws.com/residuals_20260906043458.svg)

<!-- /RESIDUALS_CHART -->

<!-- REVIEW_TIMING_CHART -->

![Review timing](https://shyal.s3.amazonaws.com/review_timing_20260906043458.svg)

<!-- /REVIEW_TIMING_CHART -->

<!-- SOLVETIME_CHART -->

![How solve time changes with repetition and shared moves](https://shyal.s3.amazonaws.com/solvetime_20260906043458.svg)

<!-- /SOLVETIME_CHART -->

The connectivity effect, zoomed in. Every timed solve as a dot, against how many problems in the bank share its moves. The scatter is honest about the size of the effect: the running medians sit flat until a walk's moves are shared by roughly thirty problems, then bend down. It isn't a smooth discount, it's a threshold: moves need a critical mass of carriers before the free rehearsal shows up in the clock.

<!-- CONNECTIVITY_CHART -->

![Move connectivity vs solve time](https://shyal.s3.amazonaws.com/connectivity_20260906043458.svg)

<!-- /CONNECTIVITY_CHART -->

The payoff metric is problems in reach: a problem is in reach when every move in its walk is currently solid. This replays today's walked problems against each day's historical node states, so the curve measures my skill moving under a fixed yardstick, not the catalog growing.

Two lines now. The blue one counts only evidenced walks: walks extracted from code i actually wrote. The purple one is the whole bank of <!-- N_BANK -->3091<!-- /N_BANK --> free problems, using LLM-drafted walks for everything i haven't solved yet (drafts score precision 0.80 / recall 0.75 against 50 evidenced walks, so the purple line runs a little optimistic). Guesses never mix into the blue line. The dip in the middle is the point of the whole repo: reach isn't a ratchet, volume without defense bleeds out at catalog scale.

<!-- REACH_CHART -->

![Problems in reach](https://shyal.s3.amazonaws.com/reach_20260906043458.svg)

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

<!-- ZPD_SVG -->

![The input tree of each of my last 50 solves, one per second](https://shyal.s3.amazonaws.com/zpd_20260906043458.svg)

<!-- /ZPD_SVG -->

## Rating

<!-- ELO_CHART -->

![Elo on a contest clock](https://shyal.s3.amazonaws.com/elo_20260906043458.svg)

<!-- /ELO_CHART -->

## Solve rate

Solves and drills per day, then the unique ones. Uniques are tracked separately because as complexity ramps up, questions and drill rungs get revisited, and the unique line is the part that is new ground. Drills only exist since August 2026, when the drill bank became the real bank and leetcode problems became the tests.

<!-- SOLVES_CHART -->

![Solves and drills per day](https://shyal.s3.amazonaws.com/rates_20260906043458.svg)

<!-- /SOLVES_CHART -->

## Tooling versus solves

Cumulative commits of each kind. A solve commit adds a file to `solved/`, problem or drill, fails excluded. A tooling commit is any other commit that touches code: the picker, the graph scripts, the drill bank, the makefile. Commits that only regenerate the README or hand-edit graph json are neither and are left out.

<!-- COMMITS_CHART -->

![Tooling commits versus solves](https://shyal.s3.amazonaws.com/commits_20260906043458.svg)

<!-- /COMMITS_CHART -->

## Readiness

Everything here comes from the Monte Carlo behind the mock charts up top. Ready means a 50% central pass rate; each bar shows today's rate against that mark, and the date in the title is when the forward simulation crosses it. Nothing is stored: the projection chart replays every day since the repo started from the evidence visible on that day. The old LLM date guesses are retired - they were garbage - and their stored snapshots are gone with them (git history has the file if anyone cares).

Contest bar: today's central P(clear a single hard).

<!-- CONTEST_PROGRESS -->

![Contest Readiness Progress (Ready by 2026-11-02, in 57 days)](https://shyal.s3.amazonaws.com/contest_progress_20260906043458.png)

<!-- /CONTEST_PROGRESS -->

FAANG bar: today's central P(pass a full onsite: 2 easies + 2 mediums + at least one hard).

<!-- FAANG_PROGRESS -->

![FAANG Interview Readiness Progress (Ready by 2026-11-23 at 2h/day, in 78 days)](https://shyal.s3.amazonaws.com/faang_progress_20260906043458.png)

<!-- /FAANG_PROGRESS -->

The chart below puts the history and the forecast on one time axis. Left of today: cumulative solves by kind, how many nodes were STALE or FRAGILE at the end of each day, and the same pass model evaluated on the evidence visible that day. Right of today: `make simulate`, which runs the real picker (`kg_next.pick`, the function behind `make next`) forward one day at a time at my measured pace, draws each solve from the fitted forgetting curve, and stops when central P(onsite) reaches 50%. The bar above gets its date from the Monte Carlo, which simulates a policy of its own; this date comes from the policy that actually serves me, so the two differ by a week or two. The thin lines are other seeds of the same run.

<!-- FORECAST_CHART -->

![History and forecast to a 50% pass rate](https://shyal.s3.amazonaws.com/forecast_20260906043458.svg)

<!-- /FORECAST_CHART -->

Every projected date is recorded daily, so one chart tracks whether the projections are stable. A flat line means the model isn't fooled by what i did that week; drift upward means i'm slacking. The third line is `utils/kg/kg_predict`, a day-by-day simulation of how the picker would spend the hours; its date answers "when is the work done" (graph fully solid + enough mediums banked + a polish block), not "when would i pass", which is why it lands much earlier.

<!-- READINESS_PROJECTION_CHART -->

![Projected ready dates over time](https://shyal.s3.amazonaws.com/readiness_projection_20260906043458.png)

<!-- /READINESS_PROJECTION_CHART -->

As you can see, these readiness projections are currently highly unreliable. The first issue is the inconsistency in practice (with a huge gap between September 2025 and August 2026), and secondly it's because the monte carlo simulation tries to guess my progress. It's rolling dice with an incomplete picture.

I'm currently working on getting a more accurate picture than monte carlo, via a simulation of the picker, and predictions fitted to my actual performance. This was only added toward the end of August 2026, and the simulation is lacking about 50 hards before it can deliver an accurate pass rate of 50% on the on-site.

## The make next commands

Everything goes through one command. Each word after `next` is a filter or a switch, and the order does not matter.

```
make next                       what the graph says to do now: a fragile or stale
                                technique gets a problem that exercises it, or its
                                drill when no problem fits
make next 2                     the second recommendation instead of the first
make next why                   when there is nothing to serve, which techniques
                                are waiting and why
make next graph                 label the drawn tree with technique names instead
                                of shapes

make next sql                   restrict to one group: sql, trees, graphs,
                                recursion-dp, streaming, ...
make next sql cram              a drill is normally held until the technique under
                                it has a clean unaided rep. cram lifts that hold,
                                so a group can be walked in one sitting
make next sql early             ignore the forgetting curve: every technique in the
                                group gets its next drill, solid or not,
                                prerequisites first. implies cram
make next sql assisted          only the drills whose last rep needed a hint, a
                                walkthrough or a copy: the unaided rep each one
                                is waiting for. implies early

make next sql assisted prepare  any of the above, then load the pick into
                                current.py and start the clock
make next sql assisted graph    any of the above, with the labelled drawing
```

A drill is served at most once a day, whatever the switches.

Tab completion for the groups and switches: `. utils/harness/make-next-completion.bash` from `~/.bashrc`.

# Leetcode flavoured environment

Leetcode's python environment is non-standard: it seems to have pretty much everything in modules like `itertools`, `functools`, `bisect`, `operator` etc. readily available without the need for imports.

This is really great as it makes writing solutions way faster, without the need to import anything.

This repo tries to reproduce this same environment with `utils/harness/sitecustomize.py`. It also has a `stubs/builtins.pyi` for autocomplete to handle this custom import scheme, as well as all the utilities for trees, linked lists, pretty printing etc.

# Dependencies

```
python3 -m venv .venv
. .venv/bin/activate
cp utils/harness/sitecustomize.py .venv/lib/python3.10/site-packages/
pip3 install -r requirements.txt
```

# Running

```
PYTHONPATH=./utils:${PYTHONPATH} python3 utils/tests/test_runner.py
```

# Disclaimer

The utility scripts in this repo (for git log reports etc.), solve rate computations etc. are LLM generated, so not production quality code (throw away scripts).

Everything currently charted is measured or simulated; the retired LLM-guessed readiness dates only survive in git history.

Solves are all mine. When they're not, i.e. 'learning' commits etc., then credit to the author is given (which can include LLM generated solves, credit also given).
