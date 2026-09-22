from seq_utils import lcs


def test_lcs_is_the_length_by_default():
    assert lcs("abac", "cab") == 2


def test_lcs_full_is_the_table_of_lengths():
    assert lcs("ab", "b", full=True) == [[0, 0], [0, 0], [0, 1]]


def test_lcs_type_str_is_one_longest_common_subsequence():
    assert lcs("abac", "cab", type=str) == "ab"


def test_lcs_type_list_and_tuple_work_on_numbers():
    assert lcs([1, 4, 2], [1, 2, 4], type=list) == [1, 4]
    assert lcs([1, 4, 2], [1, 2, 4], type=tuple) == (1, 4)


def test_lcs_full_type_str_is_the_table_of_strings():
    assert lcs("ab", "b", full=True, type=str) == [["", ""], ["", ""], ["", "b"]]


def test_lcs_of_an_empty_input_is_empty():
    assert (lcs("", "abc"), lcs("", "", type=str)) == (0, "")
