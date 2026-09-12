from graph_utils import as_dict_of_dicts


def test_dict_of_lists_becomes_dict_of_dicts():
    assert as_dict_of_dicts({0: [1, 2], 1: []}) == {0: {1: 1, 2: 1}, 1: {}}


def test_dict_of_dicts_unchanged():
    G = {0: {1: 5}, 1: {}}
    assert as_dict_of_dicts(G) == G


def test_dict_of_scalars_is_one_edge_per_key():
    assert as_dict_of_dicts({41: 0, 42: 0, 43: 1}) == {
        41: {0: 1},
        42: {0: 1},
        43: {1: 1},
    }


def test_parent_array_is_a_forest_without_self_loops():
    assert as_dict_of_dicts([2, 2, 2, 1]) == {0: {2: 1}, 1: {2: 1}, 2: {}, 3: {1: 1}}


def test_mixed_dict_values():
    assert as_dict_of_dicts({0: [1], 1: 2, 2: {3: 7}}) == {
        0: {1: 1},
        1: {2: 1},
        2: {3: 7},
    }
