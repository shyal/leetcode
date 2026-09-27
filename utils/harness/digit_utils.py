# digit_utils.py
#
# Digit helpers preloaded by sitecustomize: a number as its list of digits and
# back, and the parity tests even and odd.

from typing import List, Union


def to_digits(num: Union[int, str], reverse: bool = False) -> List[int]:
    """The digits of num as ints, most significant first.

    With reverse=True the least significant digit comes first, so digit i
    is the coefficient of 10**i. A negative int loses its sign.
    """
    ds = [int(c) for c in str(num).lstrip("-")]
    return ds[::-1] if reverse else ds


def to_int(digits: List[int], reverse: bool = False) -> int:
    """The int whose digits are the list, most significant first.

    With reverse=True the list is read least significant first, the inverse
    of to_digits(num, reverse=True). An empty list is 0.
    """
    ds = digits[::-1] if reverse else digits
    out = 0
    for d in ds:
        out = out * 10 + d
    return out


def even(n: int) -> bool:
    """True when n is even."""
    return n % 2 == 0


def odd(n: int) -> bool:
    """True when n is odd."""
    return n % 2 == 1
