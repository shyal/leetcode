from bs_utils import first_false, first_true, last_false, last_true


def test_first_true_boundary_in_the_middle():
    assert first_true(1, 100, lambda x: x * x >= 50) == 8


def test_first_true_at_both_ends():
    assert first_true(1, 100, lambda x: x >= 1) == 1
    assert first_true(1, 100, lambda x: x >= 100) == 100
    assert first_true(7, 7, lambda x: True) == 7


def test_first_true_all_false_is_hi_plus_one():
    assert first_true(1, 100, lambda x: False) == 101


def test_first_true_is_logarithmic():
    calls = []

    def ok(x):
        calls.append(x)
        return x >= 5

    assert first_true(1, 10**9, ok) == 5
    assert len(calls) <= 31


def test_last_true_boundary_in_the_middle():
    assert last_true(1, 100, lambda x: x * x <= 50) == 7


def test_last_true_at_both_ends():
    assert last_true(1, 100, lambda x: x <= 1) == 1
    assert last_true(1, 100, lambda x: x <= 100) == 100
    assert last_true(7, 7, lambda x: True) == 7


def test_last_true_all_false_is_lo_minus_one():
    assert last_true(1, 100, lambda x: False) == 0


def test_last_true_is_logarithmic():
    calls = []

    def ok(x):
        calls.append(x)
        return x <= 5

    assert last_true(1, 10**9, ok) == 5
    assert len(calls) <= 31


def test_first_false_boundary_and_ends():
    assert first_false(1, 100, lambda x: x * x <= 50) == 8
    assert first_false(1, 100, lambda x: x <= 1) == 2
    assert first_false(1, 100, lambda x: x <= 100) == 101


def test_last_false_boundary_and_ends():
    assert last_false(1, 100, lambda x: x * x >= 50) == 7
    assert last_false(1, 100, lambda x: x >= 100) == 99
    assert last_false(1, 100, lambda x: x >= 1) == 0
