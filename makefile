.PHONY: all parse learning prepare recommend force unforce preflight kg-extract kg-status kg-viz movie next dive drill hard is_session_start readme residuals sleep wake solved failed test timer viz

all:
	@cp utils/sitecustomize.py .venv/lib/python3.10/site-packages/
	@if [ "$$(git rev-parse --abbrev-ref HEAD)" = "master" ]; then PYTHONPATH=./utils .venv/bin/python3 utils/kg_status --summary; fi
	@PYTHONPATH=./utils:${PYTHONPATH} .venv/bin/python3 utils/test_runner.py

goals:
	@.venv/bin/python3 utils/solve_rate.py --goals data/goals.json --timer-font=doh

today:
	@PYTHONPATH=./utils .venv/bin/python3 utils/kg_today $(patsubst rebuild,--force,$(filter-out $@,$(MAKECMDGOALS)))

is_session_start:
	@PYTHONPATH=./utils .venv/bin/python3 utils/is_session_start || true

parse:
	@.venv/bin/python3 utils/parse.py

learning:
	@.venv/bin/python3 utils/learning

prepare:
	@.venv/bin/python3 utils/prepare $(filter-out $@,$(MAKECMDGOALS))

recommend:
	@PYTHONPATH=./utils .venv/bin/python3 utils/kg_next

force:
	@PYTHONPATH=./utils .venv/bin/python3 utils/kg_force $(filter-out $@,$(MAKECMDGOALS))

unforce:
	@PYTHONPATH=./utils .venv/bin/python3 utils/kg_force --clear

preflight:
	@PYTHONPATH=./utils .venv/bin/python3 utils/preflight $(filter-out $@,$(MAKECMDGOALS))

kg-extract:
	@PYTHONPATH=./utils .venv/bin/python3 utils/kg_extract $(filter-out $@,$(MAKECMDGOALS))
	@PYTHONPATH=./utils .venv/bin/python3 utils/kg_curve --if-stale

kg-status:
	@PYTHONPATH=./utils .venv/bin/python3 utils/kg_status

kg-viz:
	@PYTHONPATH=./utils .venv/bin/python3 utils/kg_viz

curve:
	@PYTHONPATH=./utils .venv/bin/python3 utils/kg_curve
	@PYTHONPATH=./utils .venv/bin/python3 utils/kg_residuals

residuals:
	@PYTHONPATH=./utils .venv/bin/python3 utils/kg_residuals

# make mock is implemented in Rust (utils/test_mock.py guards it); the shared
# model math also lives in kg_lib.py for the README chart — change them
# together (utils/test_golden.py diffs the two implementations)
MOCK_BIN := utils/kg_mock_rs/target/release/kg_mock

$(MOCK_BIN): utils/kg_mock_rs/src/main.rs utils/kg_mock_rs/Cargo.toml
	@cargo build --release --quiet --manifest-path utils/kg_mock_rs/Cargo.toml

mock: $(MOCK_BIN)
	@$(MOCK_BIN) $(filter-out $@,$(MAKECMDGOALS))

predict:
	@PYTHONPATH=./utils .venv/bin/python3 utils/kg_predict $(filter-out $@,$(MAKECMDGOALS))

# make movie is implemented in Rust: one pinned graphviz layout, the history
# replayed as SMIL animation into graph/kg_movie.svg (embedded by make readme)
MOVIE_BIN := utils/kg_movie_rs/target/release/kg_movie

$(MOVIE_BIN): utils/kg_movie_rs/src/main.rs utils/kg_movie_rs/Cargo.toml
	@cargo build --release --quiet --manifest-path utils/kg_movie_rs/Cargo.toml

movie: $(MOVIE_BIN)
	@$(MOVIE_BIN) $(filter-out $@,$(MAKECMDGOALS))

sleep:
	@PYTHONPATH=./utils .venv/bin/python3 utils/kg_sleep $(filter-out $@,$(MAKECMDGOALS))

wake:
	@PYTHONPATH=./utils .venv/bin/python3 utils/kg_sleep --wake $(filter-out $@,$(MAKECMDGOALS))

solved:
	@PYTHONPATH=./utils .venv/bin/python3 utils/kg_force --check
	@.venv/bin/python3 utils/solved
	@PYTHONPATH=./utils .venv/bin/python3 utils/kg_extract
	@PYTHONPATH=./utils .venv/bin/python3 utils/kg_curve --if-stale
	@# fold the solve's own evidence/curve into its commit (only if HEAD is fresh)
	@if ! git diff --quiet graph/ && [ $$(( $$(date +%s) - $$(git log -1 --format=%ct) )) -lt 600 ]; then \
		git add graph/ && git commit --amend --no-edit --quiet && echo "evidence folded into $$(git log -1 --format=%h)"; \
	fi

# file the current attempt as a FAILED one: same flow as solved (archive,
# solve-time trailer, extraction -> struggled evidence), honest label
failed:
	@.venv/bin/python3 utils/solved --failed
	@PYTHONPATH=./utils .venv/bin/python3 utils/kg_extract
	@PYTHONPATH=./utils .venv/bin/python3 utils/kg_curve --if-stale
	@if ! git diff --quiet graph/ && [ $$(( $$(date +%s) - $$(git log -1 --format=%ct) )) -lt 600 ]; then \
		git add graph/ && git commit --amend --no-edit --quiet && echo "evidence folded into $$(git log -1 --format=%h)"; \
	fi

test:
	@.venv/bin/pytest

viz:
	@.venv/bin/python3 misc/viz.py
	@PYTHONPATH=./utils:${PYTHONPATH} .venv/bin/python3 utils/test_runner.py --viz

%:
	@:
next:
	@PYTHONPATH=./utils .venv/bin/python3 utils/kg_next $(patsubst why,--why,$(patsubst graph,--graph,$(filter-out $@,$(MAKECMDGOALS))))

dive:
	@PYTHONPATH=./utils .venv/bin/python3 utils/kg_dive $(filter-out $@,$(MAKECMDGOALS))

hard:
	@PYTHONPATH=./utils .venv/bin/python3 utils/kg_hard $(patsubst graph,--graph,$(filter-out $@,$(MAKECMDGOALS)))

drill:
	@PYTHONPATH=./utils .venv/bin/python3 utils/drill $(filter-out $@,$(MAKECMDGOALS))

timer:
	@PYTHONPATH=./utils .venv/bin/python3 utils/timer

# the SVG renders run alongside estimate (all deterministic now — no LLM call)
readme: $(MOVIE_BIN) $(MOCK_BIN)
	@PYTHONPATH=./utils .venv/bin/python3 utils/kg_positions_svg & p1=$$!; \
	PYTHONPATH=./utils .venv/bin/python3 utils/kg_calibration_svg && PYTHONPATH=./utils .venv/bin/python3 utils/kg_timing_svg && PYTHONPATH=./utils .venv/bin/python3 utils/kg_solvetime_svg && PYTHONPATH=./utils .venv/bin/python3 utils/kg_connectivity_svg & p2=$$!; \
	$(MOVIE_BIN) & p3=$$!; \
	PYTHONPATH=./utils .venv/bin/python3 utils/kg_reach_svg & p4=$$!; \
	PYTHONPATH=./utils .venv/bin/python3 utils/estimate; s=$$?; \
	wait $$p1 && wait $$p2 && wait $$p3 && wait $$p4 && [ $$s -eq 0 ]
	@AWS_PROFILE=root PYTHONPATH=./utils .venv/bin/python3 utils/update_readme.py
