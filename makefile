.PHONY: all parse learning prepare recommend force unforce preflight kg-extract kg-status kg-viz movie next dive drill hard readme residuals sleep solved test viz warmup

all:
	@cp utils/sitecustomize.py .venv/lib/python3.10/site-packages/
	@if [ "$$(git rev-parse --abbrev-ref HEAD)" = "master" ]; then PYTHONPATH=./utils .venv/bin/python3 utils/kg_warmup; fi
	@if [ "$$(git rev-parse --abbrev-ref HEAD)" = "master" ]; then PYTHONPATH=./utils .venv/bin/python3 utils/kg_today; fi
	@PYTHONPATH=./utils:${PYTHONPATH} .venv/bin/python3 utils/test_runner.py

goals:
	@.venv/bin/python3 utils/solve_rate.py --goals goals.json --timer-font=doh

today:
	@PYTHONPATH=./utils .venv/bin/python3 utils/kg_today $(filter-out $@,$(MAKECMDGOALS))

warmup:
	@PYTHONPATH=./utils .venv/bin/python3 utils/kg_warmup

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

mock:
	@PYTHONPATH=./utils .venv/bin/python3 utils/kg_mock $(filter-out $@,$(MAKECMDGOALS))

predict:
	@PYTHONPATH=./utils .venv/bin/python3 utils/kg_predict $(filter-out $@,$(MAKECMDGOALS))

movie:
	@PYTHONPATH=./utils .venv/bin/python3 utils/kg_movie $(filter-out $@,$(MAKECMDGOALS))

sleep:
	@PYTHONPATH=./utils .venv/bin/python3 utils/kg_sleep $(filter-out $@,$(MAKECMDGOALS))

solved:
	@PYTHONPATH=./utils .venv/bin/python3 utils/kg_force --check
	@.venv/bin/python3 utils/solved
	@PYTHONPATH=./utils .venv/bin/python3 utils/kg_extract
	@PYTHONPATH=./utils .venv/bin/python3 utils/kg_curve --if-stale
	@# fold the solve's own evidence/curve into its commit (only if HEAD is fresh)
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
	@PYTHONPATH=./utils .venv/bin/python3 utils/kg_next $(filter-out $@,$(MAKECMDGOALS))

dive:
	@PYTHONPATH=./utils .venv/bin/python3 utils/kg_dive $(filter-out $@,$(MAKECMDGOALS))

hard:
	@PYTHONPATH=./utils .venv/bin/python3 utils/kg_hard $(filter-out $@,$(MAKECMDGOALS))

drill:
	@PYTHONPATH=./utils .venv/bin/python3 utils/drill $(filter-out $@,$(MAKECMDGOALS))

readme:
	@PYTHONPATH=./utils .venv/bin/python3 utils/estimate
	@PYTHONPATH=./utils .venv/bin/python3 utils/kg_positions_svg
	@AWS_PROFILE=root PYTHONPATH=./utils .venv/bin/python3 utils/update_readme.py
