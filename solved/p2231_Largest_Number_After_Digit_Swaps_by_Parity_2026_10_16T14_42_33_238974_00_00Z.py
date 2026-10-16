"""
URL: https://leetcode.com/problems/largest-number-after-digit-swaps-by-parity/description/?envType=problem-list-v2&envId=vn57k9wr

2231. Largest Number After Digit Swaps by Parity

You are given a positive integer num. You may swap any two digits of num that have the same parity (i.e. both odd digits or both even digits).

Return the largest possible value of num after any number of swaps.

Example 1:

Input: num = 1234
Output: 3412
Explanation: Swap the digit 3 with the digit 1, this results in the number 3214.
Swap the digit 2 with the digit 4, this results in the number 3412.
Note that there may be other sequences of swaps but it can be shown that 3412 is the largest possible number.
Also note that we may not swap the digit 4 with the digit 1 since they are of different parities.

Example 2:

Input: num = 65875
Output: 87655
Explanation: Swap the digit 8 with the digit 6, this results in the number 85675.
Swap the first digit 5 with the digit 7, this results in the number 87655.
Note that there may be other sequences of swaps but it can be shown that 87655 is the largest possible number.

Constraints:

    1 <= num <= 10^9

---

LEETCODE: Accepted (1 ms, 19.3 MB)
"""


# mu 0.12
# class Solution
#   def largestInteger(num: int) -> int
#     lists = {:list}
#     digits = to_digits(num)
#     parity = [even(x) for x in digits]
#     lists[True] = [x for x in digits if even(x)]
#     lists[False] = [x for x in digits if odd(x)]
#     lists[True].sort(reverse=False)
#     lists[False].sort(reverse=False)
#     to_int([lists[p] . for p in parity])

from collections import defaultdict


def to_digits(num, reverse=False, base=10):
    if isinstance(num, str):
        ds = [int(c, base) for c in num.lstrip('-')]
    else:
        num = abs(num)
        ds = []
        while True:
            (num, d) = divmod(num, base)
            ds.append(d)
            if num == 0:
                break
        ds.reverse()
    return ds[::-1] if reverse else ds


def even(n):
    return n % 2 == 0


def odd(n):
    return n % 2 == 1


def to_int(digits, reverse=False, base=10):
    ds = digits[::-1] if reverse else digits
    out = 0
    for d in ds:
        out = out * base + d
    return out


class Solution:
    def largestInteger(self, num: int) -> int:
        lists = defaultdict(list)
        digits = to_digits(num)
        parity = [even(x) for x in digits]
        lists[True] = [x for x in digits if even(x)]
        lists[False] = [x for x in digits if odd(x)]
        lists[True].sort(reverse=False)
        lists[False].sort(reverse=False)
        return to_int([lists[p].pop() for p in parity])


sol = Solution()
print(sol.largestInteger(1234))
_l, _r = sol.largestInteger(1234), 3412
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.largestInteger(65875), 87655
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.largestInteger(1), 1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.largestInteger(2), 2
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.largestInteger(111111111), 111111111
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.largestInteger(222222222), 222222222
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.largestInteger(13579), 97531
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.largestInteger(24680), 86420
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.largestInteger(102030405), 542030001
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.largestInteger(987654321), 987654321
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.largestInteger(1000000000), 1000000000
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.largestInteger(999999999), 999999999
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.largestInteger(123456789), 987654321
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.largestInteger(908172635), 986752031
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
