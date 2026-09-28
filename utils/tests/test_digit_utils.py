from digit_utils import even, odd, to_digits, to_int


def test_to_digits_most_significant_first():
    assert to_digits(65875) == [6, 5, 8, 7, 5]


def test_to_digits_reverse():
    assert to_digits(65875, reverse=True) == [5, 7, 8, 5, 6]


def test_to_digits_accepts_str_and_keeps_leading_zeros():
    assert to_digits("0042") == [0, 0, 4, 2]


def test_to_digits_single_digit_and_zero():
    assert to_digits(0) == [0]
    assert to_digits(7) == [7]


def test_to_digits_negative_loses_sign():
    assert to_digits(-31) == [3, 1]


def test_to_int_most_significant_first():
    assert to_int([8, 7, 6, 5, 5]) == 87655


def test_to_int_reverse():
    assert to_int([5, 5, 6, 7, 8], reverse=True) == 87655


def test_to_int_leading_zeros_and_empty():
    assert to_int([0, 0, 4, 2]) == 42
    assert to_int([]) == 0


def test_to_digits_base_2_gives_bits():
    assert to_digits(13, base=2) == [1, 1, 0, 1]
    assert to_digits(13, reverse=True, base=2) == [1, 0, 1, 1]
    assert to_digits(0, base=2) == [0]
    assert to_digits("0101", base=2) == [0, 1, 0, 1]


def test_to_digits_base_16_reads_hex_str():
    assert to_digits("ff", base=16) == [15, 15]
    assert to_digits(255, base=16) == [15, 15]


def test_to_int_base_2_reads_bits():
    assert to_int([1, 1, 0, 1], base=2) == 13
    assert to_int([1, 0, 1, 1], reverse=True, base=2) == 13


def test_round_trip_any_base():
    for base in (2, 3, 8, 16):
        for n in (0, 5, 10, 1234, 1000000000):
            assert to_int(to_digits(n, base=base), base=base) == n
            assert (
                to_int(to_digits(n, reverse=True, base=base), reverse=True, base=base)
                == n
            )


def test_round_trip():
    for n in (0, 5, 10, 1234, 1000000000):
        assert to_int(to_digits(n)) == n
        assert to_int(to_digits(n, reverse=True), reverse=True) == n


def test_even_odd():
    assert [even(n) for n in range(5)] == [True, False, True, False, True]
    assert [odd(n) for n in range(5)] == [False, True, False, True, False]
    assert even(-4) and odd(-3)
