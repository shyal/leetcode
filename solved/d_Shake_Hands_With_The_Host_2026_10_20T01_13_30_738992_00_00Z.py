"""
DRILL: Shake Hands With The Host

Given parties, where parties[i] lists the numbered guests at party i in
arrival order, return the dict adj of who shook hands with whom. The
parties happen over a week, so a guest can attend several. The first to
arrive hosts the party. Every other guest shakes hands with the host.
The dict adj is one record for the week: every guest is a key, and
adj[g] holds every guest g shook hands with, at any party, in the order
the handshakes happen, repeats included.

Example 1:

Input: parties = [[11, 12, 15], [14, 15], [16, 14], [19]]
Output: {11: [12, 15], 12: [11], 15: [11, 14], 14: [15, 16], 16: [14], 19: []}
Explanation: guest 15 goes to party 0, hosted by 11, and party 1, hosted
by 14, so 15 shakes hands once at each. Guest 19 parties alone.

Example 2:

Input: parties = [[13], [13], [13]]
Output: {13: []}

Constraints:

    1 <= len(parties) <= 1000
    1 <= len(parties[i]) <= 10
    0 <= guest number < 10^6

    REQUIRED: must run in O(L) time, where L is the total guest count over
    all parties. NO party-to-party pair tests; NO all-pairs handshakes
    inside a party.
"""


# mu 0.12
# class Solution
#   def handshakes(parties: [[int]]) -> {int: [int]}
#     ret res = {:list}
#     for guests in parties
#       res[guests[0]]
#       for guest in guests[1:]
#         res[guests[0]] <- guest
#         res[guest] <- guests[0]

from collections import defaultdict


class Grid(list):
    """A list of rows that also takes a (row, col) pair as an index."""

    def __getitem__(self, k):
        if type(k) is tuple:
            return list.__getitem__(self, k[0])[k[1]]
        return list.__getitem__(self, k)

    def __setitem__(self, k, v):
        if type(k) is tuple:
            list.__getitem__(self, k[0])[k[1]] = v
        else:
            list.__setitem__(self, k, v)


class Solution:
    def handshakes(self, parties: list[list[int]]) -> dict[int, list[int]]:
        _in_parties, parties = parties, Grid(parties)
        _w_parties = parties
        try:
            res = defaultdict(list)
            for guests in parties:
                res[guests[0]]
                for guest in guests[1:]:
                    res[guests[0]].append(guest)
                    res[guest].append(guests[0])
            return res
        finally:
            _in_parties[:] = _w_parties


sol = Solution()
print(dict(sol.handshakes([[11, 12, 15], [14, 15], [16, 14], [19]])))
_l, _r = sol.handshakes([[11, 12, 15], [14, 15], [16, 14], [19]]), {11: [12, 15], 12: [11], 15: [11, 14], 14: [15, 16], 16: [14], 19: []}
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
_l, _r = sol.handshakes([[13], [13], [13]]), {13: []}
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
_l, _r = sol.handshakes([[17]]), {17: []}
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
_l, _r = sol.handshakes([[11, 12], [13, 14]]), {11: [12], 12: [11], 13: [14], 14: [13]}
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
_l, _r = sol.handshakes([[11, 12], [12, 11]]), {11: [12, 12], 12: [11, 11]}
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
_l, _r = sol.handshakes([[11, 12], [11, 13]]), {11: [12, 13], 12: [11], 13: [11]}
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
_l, _r = sol.handshakes([[15, 11], [12, 11]]), {15: [11], 11: [15, 12], 12: [11]}
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
_l, _r = sol.handshakes([[12, 11], [11, 13]]), {12: [11], 11: [12, 13], 13: [11]}
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
