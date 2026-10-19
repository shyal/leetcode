"""
DRILL: First Lit Bulb

Given a row of bulbs lit, where lit[i] is True when bulb i is on, return
the index of the first bulb that is on. Every bulb before it is off and
every bulb after it is on. At least one bulb is on.

Example 1:

Input: lit = [False, False, False, True, True]
Output: 3

Example 2:

Input: lit = [False, False, False, False, False, False, False, True]
Output: 7

Example 3:

Input: lit = [False, True, True, True, True, True, True, True]
Output: 1

Example 4:

Input: lit = [True, True, True, True, True, True, True, True]
Output: 0

Example 5:

Input: lit = [False, False, False, False, True, True, True, True]
Output: 4

Constraints:

    1 <= len(lit) <= 10^5
    lit is False for a prefix and True for the rest.

    REQUIRED: must run in O(log n) time. NO scan from the left.
"""


# mu 0.12
# class Solution
#   def firstLit(lit: [bool]) -> int
#     first_true(0, len(lit)-1, x -> lit[x])

from bisect import bisect_left


def first_true(lo, hi, ok):
    return lo + bisect_left(range(lo, hi + 1), True, key=ok)


class Solution:
    def firstLit(self, lit: list[bool]) -> int:
        return first_true(0, len(lit) - 1, lambda x: lit[x])


sol = Solution()
print(sol.firstLit([False, False, False, True, True]))
_l, _r = sol.firstLit([False, False, False, True, True]), 3
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
_l, _r = sol.firstLit([False, False, False, False, False, False, False, True]), 7
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
_l, _r = sol.firstLit([False, True, True, True, True, True, True, True]), 1
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
_l, _r = sol.firstLit([True, True, True, True, True, True, True, True]), 0
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
_l, _r = sol.firstLit([False, False, False, False, True, True, True, True]), 4
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
_l, _r = sol.firstLit([True]), 0
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
_l, _r = sol.firstLit([False] * 99999 + [True]), 99999
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
_l, _r = sol.firstLit([True] * 100000), 0
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
