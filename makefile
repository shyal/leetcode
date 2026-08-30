.PHONY: all learning mirror q prepare force unforce preflight kg-extract kg-status kg-viz movie next dive drill hard is_session_start readme residuals sleep wake solved failed test timer viz graph

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
	@if [ "$(firstword $(MAKECMDGOALS))" != next ]; then PYTHONPATH=./utils .venv/bin/python3 utils/kg/prepare $(filter-out $@,$(MAKECMDGOALS)); fi


force:
	@PYTHONPATH=./utils .venv/bin/python3 utils/kg/kg_force $(filter-out $@,$(MAKECMDGOALS))

unforce:
	@PYTHONPATH=./utils .venv/bin/python3 utils/kg/kg_force --clear

preflight:
	@PYTHONPATH=./utils .venv/bin/python3 utils/kg/preflight $(filter-out $@,$(MAKECMDGOALS))

kg-extract:
	@PYTHONPATH=./utils .venv/bin/python3 utils/kg/kg_extract $(filter-out $@,$(MAKECMDGOALS))
	@PYTHONPATH=./utils .venv/bin/python3 utils/kg/kg_curve --if-stale
	@PYTHONPATH=./utils .venv/bin/python3 utils/kg/kg_solvecost --if-stale

kg-status:
	@PYTHONPATH=./utils .venv/bin/python3 utils/kg/kg_status

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

# file phase (freezes the solve time) -> judge -> curve -> ONE commit at the
# end carrying solve + evidence + curve, with the frozen time in the message.
# Ctrl-C anywhere: re-run `make solved`, every step resumes (utils/kg/solved).
solved:
	@PYTHONPATH=./utils .venv/bin/python3 utils/kg/kg_force --check
	@PYTHONPATH=./utils .venv/bin/python3 utils/kg/solved
	@PYTHONPATH=./utils .venv/bin/python3 utils/kg/kg_extract
	@PYTHONPATH=./utils .venv/bin/python3 utils/kg/kg_curve --if-stale
	@PYTHONPATH=./utils .venv/bin/python3 utils/kg/kg_solvecost --if-stale
	@PYTHONPATH=./utils .venv/bin/python3 utils/kg/solved --commit

# file the current attempt as a FAILED one: same flow as solved (archive,
# solve-time trailer, extraction -> struggled evidence), honest label
failed:
	@PYTHONPATH=./utils .venv/bin/python3 utils/kg/solved --failed
	@PYTHONPATH=./utils .venv/bin/python3 utils/kg/kg_extract
	@PYTHONPATH=./utils .venv/bin/python3 utils/kg/kg_curve --if-stale
	@PYTHONPATH=./utils .venv/bin/python3 utils/kg/kg_solvecost --if-stale
	@PYTHONPATH=./utils .venv/bin/python3 utils/kg/solved --commit

test:
	@.venv/bin/pytest

viz:
	@.venv/bin/python3 dsa/viz.py
	@PYTHONPATH=./utils:${PYTHONPATH} .venv/bin/python3 utils/tests/test_runner.py --viz

%:
	@:
graph:
	@:
next:
	@PYTHONPATH=./utils .venv/bin/python3 utils/kg/kg_next $(patsubst why,--why,$(patsubst graph,--graph,$(patsubst spark,--group=spark,$(patsubst sql,--group=sql,$(patsubst cram,--cram,$(patsubst early,--early,$(patsubst prepare,--prepare,$(filter-out $@,$(MAKECMDGOALS)))))))))

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
	@PYTHONPATH=./utils .venv/bin/python3 utils/kg/kg_hard $(patsubst graph,--graph,$(filter-out $@,$(MAKECMDGOALS)))

drill:
	@PYTHONPATH=./utils .venv/bin/python3 utils/kg/drill $(filter-out $@,$(MAKECMDGOALS))

timer:
	@PYTHONPATH=./utils .venv/bin/python3 utils/kg/timer

# the SVG renders run alongside estimate (all deterministic now — no LLM call)
readme: $(MOVIE_BIN) $(MOCK_BIN)
	@PYTHONPATH=./utils .venv/bin/python3 utils/readme/kg_positions_svg & p1=$$!; \
	PYTHONPATH=./utils .venv/bin/python3 utils/readme/kg_calibration_svg && PYTHONPATH=./utils .venv/bin/python3 utils/readme/kg_timing_svg && PYTHONPATH=./utils .venv/bin/python3 utils/readme/kg_solvetime_svg && PYTHONPATH=./utils .venv/bin/python3 utils/readme/kg_connectivity_svg && PYTHONPATH=./utils .venv/bin/python3 utils/readme/kg_rates_svg && PYTHONPATH=./utils .venv/bin/python3 utils/readme/kg_zpd_svg & p2=$$!; \
	$(MOVIE_BIN) & p3=$$!; \
	PYTHONPATH=./utils .venv/bin/python3 utils/readme/kg_reach_svg & p4=$$!; \
	PYTHONPATH=./utils .venv/bin/python3 utils/kg/estimate; s=$$?; \
	wait $$p1 && wait $$p2 && wait $$p3 && wait $$p4 && [ $$s -eq 0 ]
	@AWS_PROFILE=readme-uploader PYTHONPATH=./utils .venv/bin/python3 utils/readme/update_readme.py
