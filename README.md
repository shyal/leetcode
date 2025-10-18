[![Run Tests](https://github.com/shyal/leetcode/actions/workflows/run-tests.yml/badge.svg)](https://github.com/shyal/leetcode/actions/workflows/run-tests.yml)

# Leetcode grind

Here are some little charts, generated from the git log.

![Problem Grid Animation](https://shyal.s3.amazonaws.com/problem_grid_20251018030739.gif)

## Solve rate

This is the daily solve rate.

![Solves Per Day (Full Repo History)](https://shyal.s3.amazonaws.com/solves_per_day_20251018030739.png)

## Unique solve rate

This is the daily unique solve rate. This is because as complexity ramps up, questions will need to be revisited.

![Unique Problems Solved Daily (Full Repo History)](https://shyal.s3.amazonaws.com/uniques_per_day_20251018030739.png)

## Contest progress

Grok estimates when i'll be ready to take part in leetcode contests.

![Contest Readiness Progress (Ready by 2025-11-30)](https://shyal.s3.amazonaws.com/contest_progress_20251018030739.png)

## FAANG progress

Grok estimates when i'll be ready to pass FAANG mock interviews. Currently the focus of this repo is just fun, but this is an interesting metric regardless.

![FAANG Interview Readiness Progress (Ready by 2026-02-15)](https://shyal.s3.amazonaws.com/faang_progress_20251018030739.png)

## Estimate dates variance charts

I'm curious to see the amount of variance in the estimates, i.e whether they're stable over time.

![Contest Readiness Projection Over Time](https://shyal.s3.amazonaws.com/contest_variance_20251018030739.png)

![FAANG Interview Readiness Projection Over Time](https://shyal.s3.amazonaws.com/faang_variance_20251018030739.png)

## Contest topics readines chart

![Contest Topics Readiness Over Time](https://shyal.s3.amazonaws.com/contest_topics_readiness_20251018030739.gif)

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
