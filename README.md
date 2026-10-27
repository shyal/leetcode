[![Run Tests](https://github.com/shyal/leetcode/actions/workflows/run-tests.yml/badge.svg)](https://github.com/shyal/leetcode/actions/workflows/run-tests.yml) <!-- CONTEST_BADGE -->![Virtual contests: the proven rating over their problems](https://shyal.s3.amazonaws.com/contest_badge_20261027161315.svg)<!-- /CONTEST_BADGE -->

This is a mix of leetcode problems, as well as several language drills. The contest badge is LeetCode's contest rating formula applied to my [virtual contests](contests/), which LeetCode itself does not rate: my virtual rank against the real field of each contest, sampled.

<!-- GAUGES -->

![Progress: algorithms first sight, algorithms current reach, python, typescript, rust, sql, systems design](https://shyal.s3.amazonaws.com/gauges_20261027161315.svg)

<!-- /GAUGES -->

## The technique graph

Each problem is a set of techniques. Each technique is a node, and an edge connects a technique to the techniques it needs.

<!-- KG_MOVIE -->

![Technique graph growing solve by solve](https://shyal.s3.amazonaws.com/kg_movie_20261027164413.svg)

<!-- /KG_MOVIE -->

## The mock simulator

A Monte Carlo of cold mocks, drawn from the graph state on each date.

<!-- PASS_PROB_CHART -->

![P(pass a mock) over time](https://shyal.s3.amazonaws.com/pass_probability_20261027164413.svg)

<!-- /PASS_PROB_CHART -->

<!-- MOCK_SWARM_CHART -->

![Individual simulated mocks over time](https://shyal.s3.amazonaws.com/mock_swarm_20261027164413.svg)

<!-- /MOCK_SWARM_CHART -->

<!-- MOCK_BLAME_CHART -->

![Share of simulated problems failed, by group](https://shyal.s3.amazonaws.com/mock_blame_20261027164413.svg)

<!-- /MOCK_BLAME_CHART -->

## Elo

Every Elo here is first sight only.

<!-- RATE_GAUGE -->

![Elo per 100 hours on problems seen for the first time](https://shyal.s3.amazonaws.com/rate_gauge_20261027164413.svg)

<!-- /RATE_GAUGE -->

<!-- PROBLEM_RATING_CHART -->

![Rating of the problems attempted](https://shyal.s3.amazonaws.com/problem_rating_20261027164616.svg)

<!-- /PROBLEM_RATING_CHART -->

<!-- PROBLEM_RATING_MONTH_CHART -->

![Rating of the problems attempted in the last 30 days](https://shyal.s3.amazonaws.com/problem_rating_month_20261027164413.svg)

<!-- /PROBLEM_RATING_MONTH_CHART -->

<!-- HOURS_CHART -->

![Elo against hours of recorded solving, with the Carnegie Mellon rate](https://shyal.s3.amazonaws.com/hours_20261027164413.svg)

<!-- /HOURS_CHART -->

<!-- ONSITE_CHART -->

![Elo history and its projection to the onsite line, on dates](https://shyal.s3.amazonaws.com/onsite_20261027164413.svg)

<!-- /ONSITE_CHART -->

<!-- PROGRESS_CHART -->

![Actual minus model on the last 30 first sights](https://shyal.s3.amazonaws.com/progress_20261027164413.svg)

<!-- /PROGRESS_CHART -->

<!-- BACKLOG_CHART -->

![Backlog and forecast: review cards, solves by kind, STALE and FRAGILE nodes](https://shyal.s3.amazonaws.com/backlog_20261027164616.svg)

<!-- /BACKLOG_CHART -->

## Earlier charts

These charts are frozen copies from earlier versions of this README. Their renderers were deleted on 2026-09-20 with the Python library they used, and the models that drew them have changed since. Before 2026-10, the picker gated what it served, and that gate made the pass and readiness numbers too high. The charts above are redrawn by every `make readme`.

### The technique graph in three dimensions (2026-09-01)

![The technique graph in three dimensions, turning while the history replays](https://shyal.s3.amazonaws.com/kg_3d_20260901231346.svg)

### The zone of proximal development (2026-09-01)

The picker served a problem only when its input tree had one fragile or stale node and all other nodes were solid.

![The input tree of each of my last 50 solves, one per second](https://shyal.s3.amazonaws.com/zpd_20260901231024.svg)

### The forgetting curve (2026-09-01)

The model is power-law forgetting with a slip rate: P(recall) = (1 - slip) * (1 + Δ/s)^(-β). The stability s increases with each clean rep and decreases with each fail. The model compares its predictions with the results, per group and over time.

![Nodes sliding down their forgetting curves](https://shyal.s3.amazonaws.com/positions_20260901231024.svg)

![Curve calibration](https://shyal.s3.amazonaws.com/curve_calibration_20260901231024.svg)

![Residuals per group over time](https://shyal.s3.amazonaws.com/residuals_20260901231024.svg)

![Review timing](https://shyal.s3.amazonaws.com/review_timing_20260901231024.svg)

### Solve time (2026-08-25 and 2026-09-01)

![How solve time changes with repetition and shared moves](https://shyal.s3.amazonaws.com/solvetime_20260901225646.svg)

![Move connectivity vs solve time](https://shyal.s3.amazonaws.com/connectivity_20260901225646.svg)

![What a solve buys](https://shyal.s3.amazonaws.com/yield_20260825004153.svg)

![Two kinds of sideways](https://shyal.s3.amazonaws.com/yield_time_20260825004153.svg)

![Problems in reach](https://shyal.s3.amazonaws.com/reach_20260901231024.svg)

### Volume (2026-09-01)

![Solves and drills per day](https://shyal.s3.amazonaws.com/rates_20260901225646.svg)

![Tooling commits versus solves](https://shyal.s3.amazonaws.com/commits_20260901225646.svg)

## Leetcode sitecustomize, harness and helpers

Moved to [HARNESS.md](HARNESS.md).
