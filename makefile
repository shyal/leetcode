.PHONY: all asserts audit chat check combos complexity cov curve dependents dive drill drop duplicates elo ext failed fmt fmt-check force graph hard harness-doc is_session_start kg-extract kg-status kg-viz lc-login lc-mocks learning lint mirror mock movie mu mu-vscode next predict preflight prepare prog progress q queue rank-table readme rep residuals rust secrets simulate sleep snippets solved spot stats studied submit test test-fast test-judge timer today types unforce viz wake

all: $(if $(filter master,$(shell git rev-parse --abbrev-ref HEAD)),graph/leet.db) $(EXT)
	@cp utils/harness/sitecustomize.py .venv/lib/python3.10/site-packages/
	@.venv/bin/python3 current.py

today: $(RS_BIN)/kg_today
	@$(RS_BIN)/kg_today $(patsubst rebuild,--force,$(filter-out $@,$(MAKECMDGOALS)))

is_session_start: $(RS_BIN)/is_session_start
	@$(RS_BIN)/is_session_start || true

learning: $(RS_BIN)/learning
	@$(RS_BIN)/learning

prepare: $(RS_BIN)/prepare
	@if [ "$(firstword $(MAKECMDGOALS))" != next ] && [ "$(firstword $(MAKECMDGOALS))" != dependents ] && [ "$(firstword $(MAKECMDGOALS))" != combos ]; then $(RS_BIN)/prepare $(filter-out $@,$(MAKECMDGOALS)); fi


force: $(RS_BIN)/kg_force
	@$(RS_BIN)/kg_force $(filter-out $@,$(MAKECMDGOALS))

unforce: $(RS_BIN)/kg_force
	@$(RS_BIN)/kg_force --clear

preflight: $(RS_BIN)/preflight
	@$(RS_BIN)/preflight $(filter-out $@,$(MAKECMDGOALS))

kg-extract: $(RS_BIN)/kg_extract $(RS_BIN)/kg_curve $(RS_BIN)/kg_solvecost
	@$(RS_BIN)/kg_extract --pending $(filter-out $@,$(MAKECMDGOALS))
	@$(RS_BIN)/kg_curve --if-stale
	@$(RS_BIN)/kg_solvecost --if-stale

# `make asserts 5` generates the extra asserts for the picker's next five
# problems, into .prepare_cache; `make asserts 5 dry` prints them instead.
asserts: $(RS_BIN)/asserts
	@$(RS_BIN)/asserts --next $(or $(filter-out $@ dry,$(MAKECMDGOALS)),5) $(patsubst dry,--dry,$(filter dry,$(MAKECMDGOALS)))

kg-status: $(RS_BIN)/kg_status
	@$(RS_BIN)/kg_status

# make stats [DAYS|all]: the scored games over a window, pass/fail, inside
# the clock, first sight against repeat
stats: $(RS_BIN)/kg_stats
	@$(RS_BIN)/kg_stats $(filter-out $@,$(MAKECMDGOALS))

# make progress: "am i progressing", three paragraphs of plain English
# (KG_TODAY=YYYY-MM-DD for the answer as of a past day)
progress: $(RS_BIN)/kg_progress
	@$(RS_BIN)/kg_progress

rep: $(RS_BIN)/kg_rep
	@$(RS_BIN)/kg_rep $(filter-out $@,$(MAKECMDGOALS))

dependents: $(RS_BIN)/kg_dependents
	@$(RS_BIN)/kg_dependents $(filter-out $@,$(MAKECMDGOALS))

# serve a chain from graph/chains/ in order: `make combos [chain] [prepare]`
combos: $(RS_BIN)/kg_combos
	@$(RS_BIN)/kg_combos $(filter-out $@,$(MAKECMDGOALS))

kg-viz: $(RS_BIN)/kg_viz
	@$(RS_BIN)/kg_viz

curve: $(RS_BIN)/kg_curve $(RS_BIN)/kg_solvecost $(RS_BIN)/kg_residuals
	@$(RS_BIN)/kg_curve
	@$(RS_BIN)/kg_solvecost
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

# copy then rename: cp straight over the loaded extension keeps its inode,
# and macOS then kills every python that imports it (Killed: 9, invalid
# code signature at page-in, 2026-09-13). The rename is atomic and gives a
# fresh inode, so a running python keeps the old file and a new one gets
# the new file.
$(EXT): $(EXT_SRC)
	@cp $(EXT_SRC) $(EXT).tmp && mv -f $(EXT).tmp $(EXT)

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
# simulated evidence until central P(onsite) reaches the target (utils/rs/kg_simulate;
# kg_readme problem-rating draws the same run after the history for the README)
simulate: $(RS_BIN)/kg_simulate
	@$(RS_BIN)/kg_simulate $(patsubst bank-rate,--bank-rate,$(patsubst seed,--seed,$(filter-out $@,$(MAKECMDGOALS))))

# make movie is implemented in Rust: one pinned graphviz layout, the history
# replayed as SMIL animation into graph/kg_movie.svg (embedded by make readme)
MOVIE_BIN := $(RS_BIN)/kg_movie

movie: $(MOVIE_BIN)
	@$(MOVIE_BIN) $(filter-out $@,$(MAKECMDGOALS))

sleep: $(RS_BIN)/kg_sleep
	@$(RS_BIN)/kg_sleep $(filter-out $@,$(MAKECMDGOALS))

wake: $(RS_BIN)/kg_sleep
	@$(RS_BIN)/kg_sleep --wake $(filter-out $@,$(MAKECMDGOALS))

# make queue [-- --size N]: the next N (default 10) problems the picker
# would serve, rating against elo (the table under make next). make queue gate [-- --gap 50] [-- --apply]:
# ask the judge model which mapped plainer problems should gate the queued
# ones rated GAP or more above elo; --apply writes them into "after".
queue: $(RS_BIN)/kg_queue
	@$(RS_BIN)/kg_queue $(filter-out $@,$(MAKECMDGOALS))

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
solved: $(RS_BIN)/kg_solved $(RS_BIN)/kg_force $(RS_BIN)/kg_extract $(RS_BIN)/lc_submit
	@$(RS_BIN)/kg_force --check
	@$(RS_BIN)/lc_submit --auto
	@$(RS_BIN)/kg_solved
	@$(RS_BIN)/kg_extract --stub
	@$(RS_BIN)/kg_solved --commit

# submit current.py's last `class Solution` to leetcode and write the verdict
# into its notes (LEETCODE: Accepted / Time Limit Exceeded ...) for the judge.
# make solved does this itself. The requests run inside the browser exposing
# devtools at LC_CDP_ENDPOINT (misc/lc_fetch.mjs): only a real browser gets
# every solution past Cloudflare.
submit: $(RS_BIN)/lc_submit
	@$(RS_BIN)/lc_submit $(filter-out $@,$(MAKECMDGOALS))

# copy the leetcode login out of that browser into the cookie file lc_mocks reads
lc-login:
	@node misc/lc_cookies.mjs

# pull every leetcode mock assessment into data/mock_assessments.json
# (make lc-mocks show prints the cache as a table)
lc-mocks:
	@.venv/bin/python3 utils/history/lc_mocks.py $(patsubst show,--show,$(filter-out $@,$(MAKECMDGOALS)))

# file the current attempt as a FAILED one: same flow as solved (archive,
# solve-time trailer, placeholder -> struggled evidence), honest label
failed: $(RS_BIN)/kg_solved $(RS_BIN)/kg_extract
	@$(RS_BIN)/kg_solved --failed
	@$(RS_BIN)/kg_extract --stub
	@$(RS_BIN)/kg_solved --commit

# file the current problem as STUDIED: read, run, played with, submitted
# maybe, and nothing scored. The record has no moves (no node, no curve,
# no Elo, no stats row) but it opens the problem's card (kg::clock) and
# cools it as a carrier, so the next serve is a repeat and not tomorrow.
# `make drop` instead leaves the picker thinking you never saw it.
studied: $(RS_BIN)/kg_solved $(RS_BIN)/kg_extract
	@$(RS_BIN)/kg_solved --studied
	@$(RS_BIN)/kg_extract --stub
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

# the guard suite without the 988-solve sweep (make test, and CI, run it)
SLOW_TESTS = --ignore=utils/tests/test_runner.py
test-fast: $(EXT)
	@.venv/bin/pytest -q -p no:cacheprovider $(SLOW_TESTS)

# the live judge: real DeepSeek calls on solve files whose verdict was once
# corrected by hand (utils/tests/test_judge_live.py). Opt-in, never in check.
test-judge: $(RS_BIN)/kg_extract
	@KG_LIVE_JUDGE=1 .venv/bin/pytest -q -p no:cacheprovider utils/tests/test_judge_live.py

cov: $(EXT)
	@.venv/bin/pytest -q -p no:cacheprovider $(SLOW_TESTS) --cov --cov-report=term-missing

test: $(EXT)
	@.venv/bin/pytest -o verbosity_assertions=2

# VS Code snippets (the lc* prefixes the SNIPPET: drill header names) live in
# misc/vscode-snippets/; this copies them into VS Code's User/snippets.
snippets:
	@cp misc/vscode-snippets/* "$$HOME/Library/Application Support/Code/User/snippets/"
	@echo "deployed: $$(ls misc/vscode-snippets | tr '\n' ' ')"

# mu REPL: expressions print their value, blocks read until a blank line, :help
mu:
	@.venv/bin/python3 mu/repl.py

# links mu/vscode into VS Code's extensions (highlighting + formatter); reload the window after
mu-vscode:
	@ln -sfn "$(CURDIR)/mu/vscode" "$$HOME/.vscode/extensions/leet.mu-0.0.1"
	@echo "linked: $$HOME/.vscode/extensions/leet.mu-0.0.1 -> mu/vscode"

viz:
	@.venv/bin/python3 dsa/viz.py
	@PYTHONPATH=./utils:${PYTHONPATH} .venv/bin/python3 utils/tests/test_runner.py --viz

%:
	@:
graph:
	@:
# make next is implemented in Rust (utils/rs/kg_next); the picker's rules
# are pinned by the tests in utils/rs/kg/src/tests/ (make rust)
NEXT_BIN := $(RS_BIN)/kg_next

next: $(NEXT_BIN) $(RS_BIN)/kg_llm_next
	@if [ -n "$(filter llm,$(MAKECMDGOALS))" ]; then \
		$(RS_BIN)/kg_llm_next $(patsubst fresh,--fresh,$(patsubst prepare,--prepare,$(filter-out $@ llm,$(MAKECMDGOALS)))); \
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

dive: $(RS_BIN)/kg_dive
	@$(RS_BIN)/kg_dive $(filter-out $@,$(MAKECMDGOALS))

hard: $(RS_BIN)/kg_hard
	@if [ "$(firstword $(MAKECMDGOALS))" != spot ]; then $(RS_BIN)/kg_hard $(patsubst graph,--graph,$(filter-out $@,$(MAKECMDGOALS))); fi

drill: $(RS_BIN)/drill
	@$(RS_BIN)/drill $(filter-out $@,$(MAKECMDGOALS))

# a recognition rep, asked for: same as `make prepare spot`, served whether
# or not make next says one is due (the SPOT_EVERY ratio only governs that)
spot: $(RS_BIN)/spot
	@$(RS_BIN)/spot $(filter-out $@,$(MAKECMDGOALS))

timer: $(RS_BIN)/timer
	@$(RS_BIN)/timer

# make elo: the Elo dashboard, live like make timer (kg_readme now)
elo: $(RS_BIN)/kg_readme
	@$(RS_BIN)/kg_readme now

# make prog: the numbers behind make progress as a live panel (the make elo
# of the proven rating); KG_TODAY=YYYY-MM-DD for a past day
prog: $(RS_BIN)/kg_readme
	@$(RS_BIN)/kg_readme prog

# this branch's Claude Code conversation: resumed if it exists, started if not
chat: $(RS_BIN)/kg_chat
	@$(RS_BIN)/kg_chat $(filter-out $@,$(MAKECMDGOALS))

# make rank-table: refresh data/leetcode_rank_table.json, the population
# snapshot the rank badge is read against
rank-table: $(RS_BIN)/kg_readme
	@$(RS_BIN)/kg_readme rank-table

# utils/harness/README.md: the reference for the helpers sitecustomize
# preloads (signatures and docstrings), read off the running harness.
harness-doc:
	@.venv/bin/python3 utils/readme/harness_doc.py

# make readme is implemented in Rust (utils/rs/kg_readme): the charts and
# badges the README carries (problem rating, hours, onsite, progress,
# backlog, the rate gauge, and the Elo, streak, rank and rate badges), then
# the S3 upload and the README's generated regions. The movie is
# $(MOVIE_BIN); the old Python chart renderers were deleted, they live in
# git history before 2026-09-21 if a chart comes back.
readme: harness-doc $(MOCK_BIN) $(RS_BIN)/estimate $(RS_BIN)/kg_readme
	@$(RS_BIN)/kg_readme
	@$(RS_BIN)/estimate
	@AWS_PROFILE=readme-uploader $(RS_BIN)/kg_readme update
