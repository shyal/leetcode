from counter_utils import Multiset


def test_key_vanishes_at_zero():
    m = Multiset()
    m["a"] += 1
    m["a"] -= 1
    assert "a" not in m
    assert len(m) == 0
    assert m == {}


def test_missing_key_reads_as_zero():
    m = Multiset()
    assert m["x"] == 0
    assert "x" not in m


def test_negative_counts_are_kept():
    m = Multiset()
    m["a"] -= 1
    assert m["a"] == -1
    m["a"] += 1
    assert "a" not in m


def test_constructor_and_update_go_through_the_filter():
    m = Multiset("aab")
    assert m == {"a": 2, "b": 1}
    m.update("b")
    m.subtract("aabb")
    assert m == {}
    m.update({"z": 0})
    assert "z" not in m


def test_zero_assignment_on_missing_key_is_a_no_op():
    m = Multiset()
    m["q"] = 0
    assert m == {}
