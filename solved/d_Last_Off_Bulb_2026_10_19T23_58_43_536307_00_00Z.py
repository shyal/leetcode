"""
DRILL: Last Off Bulb

Given a row of bulbs lit, where lit[i] is True when bulb i is on, return
the index of the last bulb that is off. Every bulb before it is off and
every bulb after it is on. At least one bulb is off.

Example 1:

Input: lit = [False, False, False, True, True]
Output: 2

Example 2:

Input: lit = [False, False, False, False, False, False, False, True]
Output: 6

Example 3:

Input: lit = [False, True, True, True, True, True, True, True]
Output: 0

Example 4:

Input: lit = [False, False, False, False, False, False, False, False]
Output: 7

Example 5:

Input: lit = [False, False, False, False, True, True, True, True]
Output: 3

Constraints:

    1 <= len(lit) <= 10^5
    lit is False for a prefix and True for the rest.

    REQUIRED: must run in O(log n) time. NO scan from the right.
"""


# mu 0.12
# class Solution
#   def lastOff(lit: [bool]) -> int
#     last_false(0, len(lit) -1, x -> lit[x])

from bisect import bisect_left


def first_true(lo, hi, ok):
    return lo + bisect_left(range(lo, hi + 1), True, key=ok)


def last_false(lo, hi, ok):
    return first_true(lo, hi, ok) - 1


class Solution:
    def lastOff(self, lit: list[bool]) -> int:
        return last_false(0, len(lit) - 1, lambda x: lit[x])


sol = Solution()
print(sol.lastOff([False, False, False, True, True]))
_l, _r = sol.lastOff([False, False, False, True, True]), 2
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
_l, _r = sol.lastOff([False, False, False, False, False, False, False, True]), 6
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
_l, _r = sol.lastOff([False, True, True, True, True, True, True, True]), 0
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
_l, _r = sol.lastOff([False, False, False, False, False, False, False, False]), 7
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
_l, _r = sol.lastOff([False, False, False, False, True, True, True, True]), 3
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
_l, _r = sol.lastOff([False]), 0
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
_l, _r = sol.lastOff([False] + [True] * 99999), 0
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
_l, _r = sol.lastOff([False] * 99999 + [True]), 99998
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
_l, _r = sol.lastOff([False] * 100000), 99999
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
