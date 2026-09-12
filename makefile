.PHONY: ext check fmt fmt-check lint types complexity duplicates test-fast cov rust audit secrets all asserts drop learning mirror q prepare force unforce preflight dependents kg-extract kg-status kg-viz rep movie next dive drill spot hard is_session_start readme rank-table residuals simulate sleep wake solved failed test timer viz graph snippets

all: graph/leet.db $(EXT) $(RS_BIN)/kg_status
	@cp utils/harness/sitecustomize.py .venv/lib/python3.10/site-packages/
	@if [ "$$(git rev-parse --abbrev-ref HEAD)" = "master" ]; then $(RS_BIN)/kg_status --summary; fi
	@PYTHONPATH=./utils:${PYTHONPATH} .venv/bin/python3 utils/tests/test_runner.py

goals:
	@PYTHONPATH=./utils .venv/bin/python3 utils/history/solve_rate.py --goals data/goals.json --timer-font=doh

today:
	@PYTHONPATH=./utils .venv/bin/python3 utils/kg/kg_today $(patsubst rebuild,--force,$(filter-out $@,$(MAKECMDGOALS)))

is_session_start: $(RS_BIN)/is_session_start
	@$(RS_BIN)/is_session_start || true

learning:
	@PYTHONPATH=./utils .venv/bin/python3 utils/history/learning

prepare:
	@if [ "$(firstword $(MAKECMDGOALS))" != next ] && [ "$(firstword $(MAKECMDGOALS))" != dependents ]; then PYTHONPATH=./utils .venv/bin/python3 utils/kg/prepare $(filter-out $@,$(MAKECMDGOALS)); fi


force: $(RS_BIN)/kg_force
	@$(RS_BIN)/kg_force $(filter-out $@,$(MAKECMDGOALS))

unforce: $(RS_BIN)/kg_force
	@$(RS_BIN)/kg_force --clear

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

kg-status: $(RS_BIN)/kg_status
	@$(RS_BIN)/kg_status

rep: $(RS_BIN)/kg_rep
	@$(RS_BIN)/kg_rep $(filter-out $@,$(MAKECMDGOALS))

dependents: $(RS_BIN)/kg_dependents
	@$(RS_BIN)/kg_dependents $(filter-out $@,$(MAKECMDGOALS))

kg-viz: $(RS_BIN)/kg_viz
	@$(RS_BIN)/kg_viz

curve: $(RS_BIN)/kg_residuals
	@PYTHONPATH=./utils .venv/bin/python3 utils/kg/kg_curve
	@PYTHONPATH=./utils .venv/bin/python3 utils/kg/kg_solvecost
	@$(RS_BIN)/kg_residuals

residuals: $(RS_BIN)/kg_residuals
	@$(RS_BIN)/kg_residuals

# The Rust tooling is one cargo workspace, utils/rs: the kg library and one
# binary per target (kg_next, kg_mock, kg_movie). One build produces all of
# them. RS_SRC is every file the build depends on.
RS_DIR := utils/rs
RS_SRC := $(RS_DIR)/Cargo.toml $(wildcard $(RS_DIR)/*/Cargo.toml) $(wildcard $(RS_DIR)/*/build.rs) $(wildcard $(RS_DIR)/*/src/*.rs)
RS_BIN := $(RS_DIR)/target/release

$(RS_BIN)/%: $(RS_SRC)
	@cargo build --release --quiet --manifest-path $(RS_DIR)/Cargo.toml

# kg_rs: the kg library as a Python extension (utils/rs/kg_py), copied into
# the venv so utils/kg/kg_lib.py can import it. make all and the test
# targets depend on it; CI runs make ext before pytest.
EXT_SRC := $(RS_BIN)/libkg_rs.$(if $(filter Darwin,$(shell uname)),dylib,so)
EXT := .venv/lib/python3.10/site-packages/kg_rs.abi3.so

$(EXT): $(EXT_SRC)
	@cp $(EXT_SRC) $(EXT)

ext: $(EXT)

# make mock is implemented in Rust (utils/tests/test_mock.py guards it); the shared
# model math also lives in kg_lib.py for the README chart - change them
# together (utils/tests/test_golden.py diffs the two implementations)
MOCK_BIN := $(RS_BIN)/kg_mock

mock: $(MOCK_BIN)
	@$(MOCK_BIN) $(filter-out $@,$(MAKECMDGOALS))

predict: $(RS_BIN)/kg_predict
	@$(RS_BIN)/kg_predict $(filter-out $@,$(MAKECMDGOALS))

# make simulate 2 [seed 7] [bank-rate 0.5]: run the real picker forward day by day on
# simulated evidence until central P(onsite) reaches 50% (utils/kg/kg_simulate;
# utils/readme/kg_forecast_svg draws the same run after the history for the README)
simulate:
	@PYTHONPATH=./utils .venv/bin/python3 utils/kg/kg_simulate $(patsubst bank-rate,--bank-rate,$(patsubst seed,--seed,$(filter-out $@,$(MAKECMDGOALS))))

# make movie is implemented in Rust: one pinned graphviz layout, the history
# replayed as SMIL animation into graph/kg_movie.svg (embedded by make readme)
MOVIE_BIN := $(RS_BIN)/kg_movie

movie: $(MOVIE_BIN)
	@$(MOVIE_BIN) $(filter-out $@,$(MAKECMDGOALS))

sleep: $(RS_BIN)/kg_sleep
	@$(RS_BIN)/kg_sleep $(filter-out $@,$(MAKECMDGOALS))

wake: $(RS_BIN)/kg_sleep
	@$(RS_BIN)/kg_sleep --wake $(filter-out $@,$(MAKECMDGOALS))

# nuke the current branch, no questions asked: discard the working tree,
# switch to master, delete the branch. refuses on master.
drop:
	@b="$$(git rev-parse --abbrev-ref HEAD)"; \
	if [ "$$b" = "master" ]; then echo "on master, nothing to drop"; exit 1; fi; \
	git checkout -q -- . && git clean -qfd && git checkout -q master && git branch -D "$$b"; \
	rm -f .solve_meta.json; \
	$(RS_BIN)/kg_chat --switch

# file phase (freezes the solve time) -> placeholder evidence (no model
# call) -> ONE commit carrying solve + placeholder, with the frozen time in
# the message -> the judge spawned detached; it commits its verdict when
# done. Seconds, not the judge's minute. Ctrl-C anywhere: re-run
# `make solved`, every step resumes (utils/rs/kg_solved).
solved: $(RS_BIN)/kg_solved $(RS_BIN)/kg_force
	@$(RS_BIN)/kg_force --check
	@$(RS_BIN)/kg_solved
	@PYTHONPATH=./utils .venv/bin/python3 utils/kg/kg_extract --stub
	@$(RS_BIN)/kg_solved --commit

# file the current attempt as a FAILED one: same flow as solved (archive,
# solve-time trailer, placeholder -> struggled evidence), honest label
failed: $(RS_BIN)/kg_solved
	@$(RS_BIN)/kg_solved --failed
	@PYTHONPATH=./utils .venv/bin/python3 utils/kg/kg_extract --stub
	@$(RS_BIN)/kg_solved --commit

# --- code quality gates -------------------------------------------------------
# make check is the aggregate every change to utils/ or dsa/ must pass (CI runs
# the same targets as separate jobs). Thresholds live next to each gate:
# pyproject.toml (black, ruff, mypy, coverage floor), utils/check/complexity
# (radon max/avg), .jscpd.json (duplication). Ratchet them down, never up.
PYSRC = $(shell utils/check/pyfiles)
PYSRC_MYPY = $(shell utils/check/pyfiles --mypy)

check: fmt-check lint types complexity rust test-fast

fmt:
	@.venv/bin/black -q $(PYSRC)
	@.venv/bin/ruff check -q --fix --select I $(PYSRC)
	@cargo fmt --all --manifest-path $(RS_DIR)/Cargo.toml

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
	@cargo fmt --all --check --manifest-path $(RS_DIR)/Cargo.toml && cargo clippy -q --manifest-path $(RS_DIR)/Cargo.toml -- -D warnings && cargo test -q --manifest-path $(RS_DIR)/Cargo.toml

audit:
	@cd $(RS_DIR) && cargo audit -q

secrets:
	@gitleaks detect --source . --no-banner --redact

# the guard suite without the 988-solve sweep and without the Python/Rust
# picker parity diff (minutes: the Python picker runs once per argument
# set). Both are make test, and CI.
SLOW_TESTS = --ignore=utils/tests/test_runner.py --ignore=utils/tests/test_next_parity.py
test-fast: $(EXT)
	@.venv/bin/pytest -q -p no:cacheprovider $(SLOW_TESTS)

cov: $(EXT)
	@.venv/bin/pytest -q -p no:cacheprovider $(SLOW_TESTS) --cov --cov-report=term-missing

test: $(EXT)
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
# make next is implemented in Rust (utils/rs/kg_next); utils/kg/kg_next is
# the Python reference and utils/tests/test_next_parity.py diffs the two over
# the real graph/ data - change them together
NEXT_BIN := $(RS_BIN)/kg_next

next: $(NEXT_BIN)
	@if [ -n "$(filter llm,$(MAKECMDGOALS))" ]; then \
		PYTHONPATH=./utils .venv/bin/python3 utils/kg/kg_llm_next $(patsubst fresh,--fresh,$(patsubst prepare,--prepare,$(filter-out $@ llm,$(MAKECMDGOALS)))); \
	else \
		$(NEXT_BIN) $(patsubst why,--why,$(patsubst graph,--graph,$(patsubst cram,--cram,$(patsubst early,--early,$(patsubst assisted,--assisted,$(patsubst prepare,--prepare,$(filter-out $@,$(MAKECMDGOALS)))))))); \
	fi

GRAPH_JSON = graph/nodes.json graph/problems.json graph/evidence.json

graph/leet.db: $(GRAPH_JSON) $(RS_BIN)/kg_mirror
	@$(RS_BIN)/kg_mirror

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

drill: $(RS_BIN)/drill
	@$(RS_BIN)/drill $(filter-out $@,$(MAKECMDGOALS))

# a recognition rep, asked for: same as `make prepare spot`, served whether
# or not make next says one is due (the SPOT_EVERY ratio only governs that)
spot:
	@PYTHONPATH=./utils .venv/bin/python3 utils/kg/spot $(filter-out $@,$(MAKECMDGOALS))

timer: $(RS_BIN)/timer
	@$(RS_BIN)/timer

# this branch's Claude Code conversation: resumed if it exists, started if not
chat: $(RS_BIN)/kg_chat
	@$(RS_BIN)/kg_chat $(filter-out $@,$(MAKECMDGOALS))

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
#   kg_positions_svg kg_calibration_svg kg_timing_svg
#   kg_solvetime_svg kg_connectivity_svg kg_rates_svg kg_commits_svg
#   kg_zpd_svg kg_degree_track kg_reach_svg kg_3d_svg kg_full_svg
#   kg_compression_svg kg_forecast_svg, and $(MOVIE_BIN) (make movie)
readme: $(MOCK_BIN) $(RS_BIN)/estimate
	@PYTHONPATH=./utils .venv/bin/python3 utils/readme/kg_elo_svg && PYTHONPATH=./utils .venv/bin/python3 utils/readme/kg_streak_svg && PYTHONPATH=./utils .venv/bin/python3 utils/readme/kg_rank_svg && PYTHONPATH=./utils .venv/bin/python3 utils/readme/kg_rate_svg && PYTHONPATH=./utils .venv/bin/python3 utils/readme/kg_problem_rating_svg && PYTHONPATH=./utils .venv/bin/python3 utils/readme/kg_backlog_svg && PYTHONPATH=./utils .venv/bin/python3 utils/readme/kg_hours_svg && PYTHONPATH=./utils .venv/bin/python3 utils/readme/kg_onsite_svg && PYTHONPATH=./utils .venv/bin/python3 utils/readme/kg_progress_svg
	@$(RS_BIN)/estimate
	@AWS_PROFILE=readme-uploader PYTHONPATH=./utils .venv/bin/python3 utils/readme/update_readme.py
