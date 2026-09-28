# digit_utils.py
#
# Digit helpers preloaded by sitecustomize: a number as its list of digits and
# back, and the parity tests even and odd.

from typing import List, Union


def to_digits(num: Union[int, str], reverse: bool = False, base: int = 10) -> List[int]:
    """The digits of num in the given base as ints, most significant first.

    With reverse=True the least significant digit comes first, so digit i
    is the coefficient of base**i. A negative int loses its sign. A str is
    read one character at a time, so leading zeros are kept; base=2 gives
    the bits.
    """
    if isinstance(num, str):
        ds = [int(c, base) for c in num.lstrip("-")]
    else:
        num = abs(num)
        ds = []
        while True:
            num, d = divmod(num, base)
            ds.append(d)
            if num == 0:
                break
        ds.reverse()
    return ds[::-1] if reverse else ds


def to_int(digits: List[int], reverse: bool = False, base: int = 10) -> int:
    """The int whose digits in the given base are the list, most significant first.

    With reverse=True the list is read least significant first, the inverse
    of to_digits(num, reverse=True). An empty list is 0. base=2 reads bits.
    """
    ds = digits[::-1] if reverse else digits
    out = 0
    for d in ds:
        out = out * base + d
    return out


def even(n: int) -> bool:
    """True when n is even."""
    return n % 2 == 0


def odd(n: int) -> bool:
    """True when n is odd."""
    return n % 2 == 1
