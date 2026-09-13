[![Run Tests](https://github.com/shyal/leetcode/actions/workflows/run-tests.yml/badge.svg)](https://github.com/shyal/leetcode/actions/workflows/run-tests.yml) <!-- ELO_BADGE -->![Elo](https://shyal.s3.amazonaws.com/elo_badge_20260913031920.svg)<!-- /ELO_BADGE --> <!-- STREAK_BADGE -->![Streak](https://shyal.s3.amazonaws.com/streak_badge_20260913031920.svg)<!-- /STREAK_BADGE --> <!-- RANK_ALL_BADGE -->![Elo against all rated LeetCode users](https://shyal.s3.amazonaws.com/rank_all_badge_20260913031920.svg)<!-- /RANK_ALL_BADGE --> <!-- RANK_REGULARS_BADGE -->![Elo against users with 20 or more contests](https://shyal.s3.amazonaws.com/rank_regulars_badge_20260913031920.svg)<!-- /RANK_REGULARS_BADGE --> <!-- RATE_BADGE -->![First-sight Elo per 100 hours](https://shyal.s3.amazonaws.com/rate_badge_20260913031920.svg)<!-- /RATE_BADGE -->

This is my leetcode repo. It uses [zerotrac] and [CLIST] so leetcode questions actually have an Elo rating attached to them, and has drills on an Anki schedule, a directed graph of moves, problems and drills that tries to categorize every leetcode question, a duolingo-style memory decay curve for nodes, and a pretty complex picker algorithm.

The biggest insight so far has been that i've been "grinding" well below my Elo, and it turns out a [Carnegie Mellon study] of 60k Codeforces users shows that rating gains come from problems at or above the solver's current Elo, and that solving easy problems correlates negatively with rating.

This probably explains why so many leetcode users refer to the infamous "leetcode grind", since leetcode does not let people pick questions that match their current Elo (unlike topcoder).

Every Elo on this page is scored on first sight only: the first time i meet a problem, on a clock. Re-solving a problem i already know is not a game, because part of that win is remembering the answer. The picker keeps its own Elo over every attempt for its own purposes, and that number is higher; it is not shown here. My current Elo moving average (over the last <!-- ELO_MA_WINDOW -->60<!-- /ELO_MA_WINDOW --> games) is <!-- ELO_MA -->1587<!-- /ELO_MA -->.

<!-- RATE_GAUGE -->

![Elo per 100 hours on problems seen for the first time](https://shyal.s3.amazonaws.com/rate_gauge_20260913031920.svg)

<!-- /RATE_GAUGE -->

The gauge is my Elo gains on problems i've seen for the first time: <!-- FS_RATE -->+84<!-- /FS_RATE --> Elo per 100h. Over the first <!-- FS_WINDOW -->60<!-- /FS_WINDOW --> days i was playing at <!-- FS_EARLY -->1572<!-- /FS_EARLY -->, over the last <!-- FS_WINDOW -->60<!-- /FS_WINDOW --> at <!-- FS_LATE -->1723<!-- /FS_LATE -->, divided by the hours in between. It's also the number the onsite chart below uses to guess when i get there. The hours chart is the raw Elo against hours over everything, old picking strategy included, so it looks a lot worse.

## Problems

The blue line is the median rating of my last 50 first sights, the green line is my Elo. The dots are every attempt, repeats included. For about a year the blue line was around 300 points below my Elo. That is the "leetcode grind" of semi randomly walking through problems, hoping for the best. It jumped in September 2026 when the picker started serving problems at my rating, and it now sits at <!-- SERVED_MEDIAN -->1647<!-- /SERVED_MEDIAN -->.

Right of the dotted line is a simulation: the picker running on its own for six months, five times over. Grey dots are the problems it would give me, the dashed lines are where the median and the Elo go. The Elo only goes up because the picker serves harder problems, not because i get better. The model assumes i don't, see below.

<!-- PROBLEM_RATING_CHART -->

![Rating of the problems attempted](https://shyal.s3.amazonaws.com/problem_rating_20260913031920.svg)

<!-- /PROBLEM_RATING_CHART -->

## Hours

The numbers in this chart are terrible, reflecting my previously poor problem picking strategy, which weighs the whole history down.

The study showed a 200 point gain at about 200 problems above one's rating, roughly 800 hours of practice, so 25 Elo per 100 hours. Since my picker algorithm, once reviews are cleared, aims to serve questions at my current Elo, i'm expecting to at least hit those 25 Elo per 100h (over the entire history), and hopefully beat it.

<!-- HOURS_CHART -->

![Elo against hours of recorded solving, with the Carnegie Mellon rate](https://shyal.s3.amazonaws.com/hours_20260913031920.svg)

<!-- /HOURS_CHART -->

## Onsite

Extrapolating noisy data. What could go wrong.

<!-- ONSITE_CHART -->

![Elo history and its projection to the onsite line, on dates](https://shyal.s3.amazonaws.com/onsite_20260913031920.svg)

<!-- /ONSITE_CHART -->

## Progress

The two projections above are extrapolations. This one isn't. The model that scores my solves knows the problem's rating and how well i remember the moves, and nothing about hours or time, because adding those didn't help it predict anything. So it assumes i'm not improving. This chart is my last 30 first sights minus what the model expected. Inside the band, the model is right. Above it for a while, i'm getting better and the model hasn't caught up yet.

<!-- PROGRESS_CHART -->

![Actual minus model on the last 30 first sights](https://shyal.s3.amazonaws.com/progress_20260913031920.svg)
<!-- /PROGRESS_CHART -->

## Backlog

<!-- BACKLOG_CHART -->

![Review backlog: open cards, due cards, due drills](https://shyal.s3.amazonaws.com/backlog_20260913031920.svg)

<!-- /BACKLOG_CHART -->

## Rank badges

The two rank badges put the Elo on LeetCode's contest scale. "vs all rated" is the share of all rated users at or above it, read off LeetCode's global ranking (snapshot in `data/leetcode_rank_table.json`, refreshed with `make rank-table`). "vs 20+ contests" is the share of a random sample of users with at least 20 attended contests, so it is an estimate from a few hundred people and moves a few points between snapshots.

The first one flatters me. Most rated users entered one contest, lost points, and never came back, so a rating a little above 1500 clears the bulk of them. The second one is the comparison that counts. Both read a problem-solving Elo, scored on first sights against [zerotrac] problem ratings, on a contest scale; a contest also has a 90 minute clock over four problems, which this does not measure.

[zerotrac]: https://zerotrac.github.io/leetcode_problem_rating/
[CLIST]: https://clist.by/
[Carnegie Mellon study]: https://carnegiemellon.shorthandstories.com/competitive-programming-talent-vs-tenacity/index.html
