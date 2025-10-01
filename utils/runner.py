import pytest
import os

pytest.register_assert_rewrite("current")

solved_dir = "./solved"
for filename in os.listdir(solved_dir):
    if filename.endswith(".py"):
        module_name = filename[:-3]  # Remove .py extension
        pytest.register_assert_rewrite(f"solved.{module_name}")


def test_current():
    import current


if __name__ == "__main__":
    pytest.main([__file__, solved_dir, "-s", "-q"])
