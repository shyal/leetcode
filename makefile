.PHONY: check fmt fmt-check lint types complexity duplicates test-fast cov rust audit secrets all asserts drop learning mirror q prepare force unforce preflight dependents kg-extract kg-status kg-viz rep movie next dive drill spot hard is_session_start readme rank-table residuals simulate sleep wake solved failed test timer viz graph snippets

all: graph/leet.db
	@cp utils/harness/sitecustomize.py .venv/lib/python3.10/site-packages/
	@if [ "$$(git rev-parse --abbrev-ref HEAD)" = "master" ]; then PYTHONPATH=./utils .venv/bin/python3 utils/kg/kg_status --summary; fi
	@PYTHONPATH=./utils:${PYTHONPATH} .venv/bin/python3 utils/tests/test_runner.py

goals:
	@PYTHONPATH=./utils .venv/bin/python3 utils/history/solve_rate.py --goals data/goals.json --timer-font=doh

today:
	@PYTHONPATH=./utils .venv/bin/python3 utils/kg/kg_today $(patsubst rebuild,--force,$(filter-out $@,$(MAKECMDGOALS)))

is_session_start:
	@PYTHONPATH=./utils .venv/bin/python3 utils/kg/is_session_start || true

learning:
	@PYTHONPATH=./utils .venv/bin/python3 utils/history/learning

prepare:
	@if [ "$(firstword $(MAKECMDGOALS))" != next ] && [ "$(firstword $(MAKECMDGOALS))" != dependents ]; then PYTHONPATH=./utils .venv/bin/python3 utils/kg/prepare $(filter-out $@,$(MAKECMDGOALS)); fi


force:
	@PYTHONPATH=./utils .venv/bin/python3 utils/kg/kg_force $(filter-out $@,$(MAKECMDGOALS))

unforce:
	@PYTHONPATH=./utils .venv/bin/python3 utils/kg/kg_force --clear

preflight:
	@PYTHONPATH=./utils .venv/bin/python3 utils/kg/preflight $(filter-out $@,$(MAKECMDGOALS))

kg-extract:
	@PYTHONPATH=./utils .venv/bin/python3 utils/kg/kg_extract --pending $(filter-out $@,$(MAKECMDGOALS))
	@PYTHONPATH=./utils .venv/bin/python3 utils/kg/kg_curve --if-stale
	@PYTHONPATH=./utils .venv/bin/python3 utils/kg/kg_solvecost --if-stale

# `make asserts 5` generates the extra asserts for the picker's next five
# problems, into .prepare_cache; `make asserts 5 dry` prints them instead.
asserts:
	@PYTHONPATH=./utils .venv/bin/python3 utils/kg/asserts --next $(or $(filter-out $@ dry,$(MAKECMDGOALS)),5) $(patsubst dry,--dry,$(filter dry,$(MAKECMDGOALS)))

kg-status:
	@PYTHONPATH=./utils .venv/bin/python3 utils/kg/kg_status

rep:
	@PYTHONPATH=./utils .venv/bin/python3 utils/kg/kg_rep $(filter-out $@,$(MAKECMDGOALS))

dependents:
	@PYTHONPATH=./utils .venv/bin/python3 utils/kg/kg_dependents $(filter-out $@,$(MAKECMDGOALS))

kg-viz:
	@PYTHONPATH=./utils .venv/bin/python3 utils/kg/kg_viz

curve:
	@PYTHONPATH=./utils .venv/bin/python3 utils/kg/kg_curve
	@PYTHONPATH=./utils .venv/bin/python3 utils/kg/kg_solvecost
	@PYTHONPATH=./utils .venv/bin/python3 utils/kg/kg_residuals

residuals:
	@PYTHONPATH=./utils .venv/bin/python3 utils/kg/kg_residuals

# make mock is implemented in Rust (utils/tests/test_mock.py guards it); the shared
# model math also lives in kg_lib.py for the README chart — change them
# together (utils/tests/test_golden.py diffs the two implementations)
MOCK_BIN := utils/kg/kg_mock_rs/target/release/kg_mock

$(MOCK_BIN): utils/kg/kg_mock_rs/src/main.rs utils/kg/kg_mock_rs/Cargo.toml
	@cargo build --release --quiet --manifest-path utils/kg/kg_mock_rs/Cargo.toml

mock: $(MOCK_BIN)
	@$(MOCK_BIN) $(filter-out $@,$(MAKECMDGOALS))

predict:
	@PYTHONPATH=./utils .venv/bin/python3 utils/kg/kg_predict $(filter-out $@,$(MAKECMDGOALS))

# make simulate 2 [seed 7] [bank-rate 0.5]: run the real picker forward day by day on
# simulated evidence until central P(onsite) reaches 50% (utils/kg/kg_simulate;
# utils/readme/kg_forecast_svg draws the same run after the history for the README)
simulate:
	@PYTHONPATH=./utils .venv/bin/python3 utils/kg/kg_simulate $(patsubst bank-rate,--bank-rate,$(patsubst seed,--seed,$(filter-out $@,$(MAKECMDGOALS))))

# make movie is implemented in Rust: one pinned graphviz layout, the history
# replayed as SMIL animation into graph/kg_movie.svg (embedded by make readme)
MOVIE_BIN := utils/kg/kg_movie_rs/target/release/kg_movie

$(MOVIE_BIN): utils/kg/kg_movie_rs/src/main.rs utils/kg/kg_movie_rs/Cargo.toml
	@cargo build --release --quiet --manifest-path utils/kg/kg_movie_rs/Cargo.toml

movie: $(MOVIE_BIN)
	@$(MOVIE_BIN) $(filter-out $@,$(MAKECMDGOALS))

sleep:
	@PYTHONPATH=./utils .venv/bin/python3 utils/kg/kg_sleep $(filter-out $@,$(MAKECMDGOALS))

wake:
	@PYTHONPATH=./utils .venv/bin/python3 utils/kg/kg_sleep --wake $(filter-out $@,$(MAKECMDGOALS))

# nuke the current branch, no questions asked: discard the working tree,
# switch to master, delete the branch. refuses on master.
drop:
	@b="$$(git rev-parse --abbrev-ref HEAD)"; \
	if [ "$$b" = "master" ]; then echo "on master, nothing to drop"; exit 1; fi; \
	git checkout -q -- . && git clean -qfd && git checkout -q master && git branch -D "$$b"; \
	rm -f .solve_meta.json; \
	utils/kg/chat --switch

# file phase (freezes the solve time) -> placeholder evidence (no model
# call) -> ONE commit carrying solve + placeholder, with the frozen time in
# the message -> the judge spawned detached; it commits its verdict when
# done. Seconds, not the judge's minute. Ctrl-C anywhere: re-run
# `make solved`, every step resumes (utils/kg/solved).
solved:
	@PYTHONPATH=./utils .venv/bin/python3 utils/kg/kg_force --check
	@PYTHONPATH=./utils .venv/bin/python3 utils/kg/solved
	@PYTHONPATH=./utils .venv/bin/python3 utils/kg/kg_extract --stub
	@PYTHONPATH=./utils .venv/bin/python3 utils/kg/solved --commit

# file the current attempt as a FAILED one: same flow as solved (archive,
# solve-time trailer, placeholder -> struggled evidence), honest label
failed:
	@PYTHONPATH=./utils .venv/bin/python3 utils/kg/solved --failed
	@PYTHONPATH=./utils .venv/bin/python3 utils/kg/kg_extract --stub
	@PYTHONPATH=./utils .venv/bin/python3 utils/kg/solved --commit

# --- code quality gates -------------------------------------------------------
# make check is the aggregate every change to utils/ or dsa/ must pass (CI runs
# the same targets as separate jobs). Thresholds live next to each gate:
# pyproject.toml (black, ruff, mypy, coverage floor), utils/check/complexity
# (radon max/avg), .jscpd.json (duplication). Ratchet them down, never up.
PYSRC = $(shell utils/check/pyfiles)
PYSRC_MYPY = $(shell utils/check/pyfiles --mypy)
CRATES = utils/kg/kg_mock_rs utils/kg/kg_movie_rs utils/kg/kg_next_rs

check: fmt-check lint types complexity rust test-fast

fmt:
	@.venv/bin/black -q $(PYSRC)
	@.venv/bin/ruff check -q --fix --select I $(PYSRC)
	@for c in $(CRATES); do cargo fmt --manifest-path $$c/Cargo.toml; done

fmt-check:
	@.venv/bin/black -q --check $(PYSRC)

lint:
	@.venv/bin/ruff check -q $(PYSRC)

types:
	@.venv/bin/mypy $(PYSRC_MYPY)

complexity:
	@.venv/bin/python3 utils/check/complexity $(PYSRC)

duplicates:
	@npx --yes jscpd utils dsa

rust:
	@for c in $(CRATES); do cargo fmt --check --manifest-path $$c/Cargo.toml && cargo clippy -q --manifest-path $$c/Cargo.toml -- -D warnings && cargo test -q --manifest-path $$c/Cargo.toml || exit 1; done

audit:
	@for c in $(CRATES); do (cd $$c && cargo audit -q) || exit 1; done

secrets:
	@gitleaks detect --source . --no-banner --redact

# the guard suite without the 988-solve sweep and without the Python/Rust
# picker parity diff (minutes: the Python picker runs once per argument
# set). Both are make test, and CI.
SLOW_TESTS = --ignore=utils/tests/test_runner.py --ignore=utils/tests/test_next_parity.py
test-fast:
	@.venv/bin/pytest -q -p no:cacheprovider $(SLOW_TESTS)

cov:
	@.venv/bin/pytest -q -p no:cacheprovider $(SLOW_TESTS) --cov --cov-report=term-missing

test:
	@.venv/bin/pytest -o verbosity_assertions=2

# VS Code snippets (the lc* prefixes the SNIPPET: drill header names) live in
# misc/vscode-snippets/; this copies them into VS Code's User/snippets.
snippets:
	@cp misc/vscode-snippets/* "$$HOME/Library/Application Support/Code/User/snippets/"
	@echo "deployed: $$(ls misc/vscode-snippets | tr '\n' ' ')"

viz:
	@.venv/bin/python3 dsa/viz.py
	@PYTHONPATH=./utils:${PYTHONPATH} .venv/bin/python3 utils/tests/test_runner.py --viz

%:
	@:
graph:
	@:
# make next is implemented in Rust (utils/kg/kg_next_rs); utils/kg/kg_next is
# the Python reference and utils/tests/test_next_parity.py diffs the two over
# the real graph/ data - change them together
NEXT_BIN := utils/kg/kg_next_rs/target/release/kg_next

$(NEXT_BIN): $(wildcard utils/kg/kg_next_rs/src/*.rs) utils/kg/kg_next_rs/Cargo.toml utils/kg/kg_mock_rs/src/lib.rs
	@cargo build --release --quiet --manifest-path utils/kg/kg_next_rs/Cargo.toml

next: $(NEXT_BIN)
	@if [ -n "$(filter llm,$(MAKECMDGOALS))" ]; then \
		PYTHONPATH=./utils .venv/bin/python3 utils/kg/kg_llm_next $(patsubst fresh,--fresh,$(patsubst prepare,--prepare,$(filter-out $@ llm,$(MAKECMDGOALS)))); \
	else \
		$(NEXT_BIN) $(patsubst why,--why,$(patsubst graph,--graph,$(patsubst cram,--cram,$(patsubst early,--early,$(patsubst assisted,--assisted,$(patsubst prepare,--prepare,$(filter-out $@,$(MAKECMDGOALS)))))))); \
	fi

GRAPH_JSON = graph/nodes.json graph/problems.json graph/evidence.json

graph/leet.db: $(GRAPH_JSON) utils/kg/kg_mirror
	@PYTHONPATH=./utils .venv/bin/python3 utils/kg/kg_mirror

mirror: graph/leet.db

q: graph/leet.db
	@f="$(filter-out $@,$(MAKECMDGOALS))"; \
	if [ -z "$$f" ]; then grep -H "^-- QUERY:" graph/queries/*.sql | sed 's|graph/queries/||; s|\.sql:-- QUERY:||'; exit 0; fi; \
	m=$$(ls graph/queries/*.sql | grep -- "$$f" | head -1); \
	if [ -z "$$m" ]; then echo "no query matching '$$f'"; exit 1; fi; \
	echo "-- $$m"; sqlite3 -header -column graph/leet.db < "$$m"

dive:
	@PYTHONPATH=./utils .venv/bin/python3 utils/kg/kg_dive $(filter-out $@,$(MAKECMDGOALS))

hard:
	@if [ "$(firstword $(MAKECMDGOALS))" != spot ]; then PYTHONPATH=./utils .venv/bin/python3 utils/kg/kg_hard $(patsubst graph,--graph,$(filter-out $@,$(MAKECMDGOALS))); fi

drill:
	@PYTHONPATH=./utils .venv/bin/python3 utils/kg/drill $(filter-out $@,$(MAKECMDGOALS))

# a recognition rep, asked for: same as `make prepare spot`, served whether
# or not make next says one is due (the SPOT_EVERY ratio only governs that)
spot:
	@PYTHONPATH=./utils .venv/bin/python3 utils/kg/spot $(filter-out $@,$(MAKECMDGOALS))

timer:
	@PYTHONPATH=./utils .venv/bin/python3 utils/kg/timer

# this branch's Claude Code conversation: resumed if it exists, started if not
chat:
	@utils/kg/chat $(filter-out $@,$(MAKECMDGOALS))

# rank-table: refresh data/leetcode_rank_table.json from LeetCode's global
# ranking (a few hundred requests, a few minutes). The rank badges read the
# file; make readme never fetches.
rank-table:
	@PYTHONPATH=./utils .venv/bin/python3 utils/readme/kg_rank_fetch

# chart generation is mostly disabled: the README carries the problem-rating
# chart, the hours chart, the backlog chart and the two badges, so kg_elo_svg
# (Elo badge; its chart is no longer linked), kg_streak_svg (streak badge),
# kg_rank_svg (the two rank badges),
# kg_problem_rating_svg, kg_backlog_svg, kg_hours_svg, kg_onsite_svg and kg_progress_svg run. The other renderers still work standalone if a chart comes back:
#   kg_positions_svg kg_calibration_svg kg_residuals_svg kg_timing_svg
#   kg_solvetime_svg kg_connectivity_svg kg_rates_svg kg_commits_svg
#   kg_zpd_svg kg_degree_track kg_reach_svg kg_3d_svg kg_full_svg
#   kg_compression_svg kg_forecast_svg, and $(MOVIE_BIN) (make movie)
readme: $(MOCK_BIN)
	@PYTHONPATH=./utils .venv/bin/python3 utils/readme/kg_elo_svg && PYTHONPATH=./utils .venv/bin/python3 utils/readme/kg_streak_svg && PYTHONPATH=./utils .venv/bin/python3 utils/readme/kg_rank_svg && PYTHONPATH=./utils .venv/bin/python3 utils/readme/kg_rate_svg && PYTHONPATH=./utils .venv/bin/python3 utils/readme/kg_problem_rating_svg && PYTHONPATH=./utils .venv/bin/python3 utils/readme/kg_backlog_svg && PYTHONPATH=./utils .venv/bin/python3 utils/readme/kg_hours_svg && PYTHONPATH=./utils .venv/bin/python3 utils/readme/kg_onsite_svg && PYTHONPATH=./utils .venv/bin/python3 utils/readme/kg_progress_svg
	@PYTHONPATH=./utils .venv/bin/python3 utils/kg/estimate
	@AWS_PROFILE=readme-uploader PYTHONPATH=./utils .venv/bin/python3 utils/readme/update_readme.py
