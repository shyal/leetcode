import pytest

pytest.register_assert_rewrite("current")


def test_current():
    import leetcode
    import leetcode_easy
    import leetcode_medium
    import leetcode_hard
    import current


if __name__ == "__main__":
    pytest.main([__file__, "-s", "-q"])
