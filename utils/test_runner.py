import pytest
import os
import time


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
    if filename.endswith(".py"):
        module_name = filename[:-3]  # Remove .py extension
        pytest.register_assert_rewrite(f"solved.{module_name}")
        modules.append(module_name)


@pytest.mark.parametrize("module_name", modules)
def test_solved(module_name):
    __import__(f"solved.{module_name}")


def test_current():
    import current


if __name__ == "__main__":
    stats = StatsPlugin()

    start_time = time.perf_counter()

    pytest.main(
        [
            __file__,
            solved_dir,
            "-s",
            "-q",
            "-c",
            os.devnull,
            "--override-ini",
            "python_files=*.py",
            "-p",
            "no:cacheprovider",
        ],
        plugins=[stats],
    )

    end_time = time.perf_counter()
    total_time = end_time - start_time

    print(f"Number of tests run: {stats.num_tests_run}")
    print(f"Total time taken: {total_time:.2f} seconds")
