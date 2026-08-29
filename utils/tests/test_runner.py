# test_runner.py

import argparse
import pytest
import os
import time
import subprocess
import contextlib

parser = argparse.ArgumentParser(description="Test leetcode codebase.")
parser.add_argument(
    "--viz", action="store_true", required=False, help="Enable visualizations"
)

# parse_args() at import time made a bare `pytest` (i.e. `make test`) abort with
# an INTERNALERROR on collection, since pytest's own argv is not ours. Only take
# argv when run as a script; under collection, fall back to the defaults.
args = parser.parse_args() if __name__ == "__main__" else parser.parse_args([])


class StatsPlugin:
    def __init__(self):
        self.num_tests_run = 0

    @pytest.hookimpl
    def pytest_runtest_logreport(self, report):
        if report.when == "call":
            self.num_tests_run += 1


pytest.register_assert_rewrite("current")

solved_dir = "./solved"
modules = []
for filename in os.listdir(solved_dir):
    # _FAILED archives preserve abandoned attempts verbatim — broken by
    # definition, never part of the green suite
    if filename.endswith(".py") and "_FAILED" not in filename:
        module_name = filename[:-3]  # Remove .py extension
        pytest.register_assert_rewrite(f"solved.{module_name}")
        modules.append(module_name)


@pytest.mark.parametrize("module_name", modules)
def test_solved(module_name):
    if not args.viz:
        with open(os.devnull, "w") as f, contextlib.redirect_stdout(f):
            __import__(f"solved.{module_name}")
    else:
        __import__(f"solved.{module_name}")


def test_current():
    print("")
    import current


if __name__ == "__main__":

    stats = StatsPlugin()

    start_time = time.perf_counter()

    try:
        current_branch = (
            subprocess.check_output(["git", "branch", "--show-current"])
            .decode()
            .strip()
        )
    except Exception:
        current_branch = "unknown"

    if current_branch == "master" and not args.viz:
        os.environ["RUNNING_TESTS"] = "True"

    args = [
        __file__,
        "-s",
        "-q",
        "-c",
        os.devnull,
        "--override-ini",
        "python_files=*.py",
        "-p",
        "no:cacheprovider",
    ]

    if current_branch != "master":
        args.extend(["-k", "test_current"])

    pytest.main(
        args,
        plugins=[stats],
    )

    end_time = time.perf_counter()
    total_time = end_time - start_time

    print(f"Number of tests run: {stats.num_tests_run}")
    print(f"Total time taken: {total_time:.2f} seconds")
