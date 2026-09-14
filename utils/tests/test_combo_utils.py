from itertools import combinations

from combo_utils import pairs, triples


def test_pairs_lexicographic():
    assert list(pairs(4)) == [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]


def test_pairs_too_small_is_empty():
    assert list(pairs(1)) == []


def test_triples_lexicographic():
    assert list(triples(4)) == [(0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3)]


def test_triples_too_small_is_empty():
    assert list(triples(2)) == []


def test_matches_combinations():
    assert list(pairs(7)) == list(combinations(range(7), 2))
    assert list(triples(7)) == list(combinations(range(7), 3))


def test_type_builds_each_one():
    assert list(pairs(3, type=list)) == [[0, 1], [0, 2], [1, 2]]
    assert list(triples(4, type=list)) == [[0, 1, 2], [0, 1, 3], [0, 2, 3], [1, 2, 3]]
