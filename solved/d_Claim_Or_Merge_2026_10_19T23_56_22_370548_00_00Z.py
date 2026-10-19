"""
DRILL: Claim Or Merge

Given accounts, where accounts[i] is the list of emails of account i,
union every two accounts that share an email, and return the dict owner
mapping each email to the first account that listed it. Solution
extends UnionFind from dsa/union_find.py over the accounts.

The first account to list an email claims it. When a later account
lists the same email, that account is merged with the owner: self.union.

Example 1:

Input: accounts = [["js@m.co", "jn@m.co"], ["mary@m.co"], ["jn@m.co", "j0@m.co"], ["m2@m.co", "mary@m.co"]]
Output: {"js@m.co": 0, "jn@m.co": 0, "mary@m.co": 1, "j0@m.co": 2, "m2@m.co": 3}
Explanation: account 2 lists jn@m.co, which account 0 already owns, so
union(2, 0). Account 3 lists mary@m.co, owned by account 1, so
union(3, 1).

    account 0:  js@m.co   jn@m.co
                            |
                            | shared: union(2, 0)
                            |
    account 2:  jn@m.co   j0@m.co

    account 1:  mary@m.co
                    |
                    | shared: union(3, 1)
                    |
    account 3:  m2@m.co   mary@m.co

Example 2:

Input: accounts = [["g@m.co"], ["g@m.co"], ["g@m.co"]]
Output: {"g@m.co": 0}
Explanation: account 0 claims g@m.co. Accounts 1 and 2 each list it, so
union(1, 0) and union(2, 0).

Constraints:

    1 <= len(accounts) <= 1000
    1 <= len(accounts[i]) <= 10

    REQUIRED: must do one dict lookup and at most one union per email.
    NO account-to-account pair tests; NO second pass over accounts.
"""

from dsa.union_find import UnionFind


# mu 0.12
# class Solution extends UnionFind
#   def union_shared(accounts: [[str]]) -> {str: int}
#     ret owner = {}
#     for >i, emails in accounts
#       for email in emails
#         if email in owner
#           self.union(i, owner[email])
#         else
#           owner[email] = i

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


class Solution(UnionFind):
    def union_shared(self, accounts: list[list[str]]) -> dict[str, int]:
        _in_accounts, accounts = accounts, Grid(accounts)
        _w_accounts = accounts
        try:
            owner = {}
            for i, emails in enumerate(accounts):
                for email in emails:
                    if email in owner:
                        self.union(i, owner[email])
                    else:
                        owner[email] = i
            return owner
        finally:
            _in_accounts[:] = _w_accounts


sol = Solution(4)
print(sol.union_shared([['js@m.co', 'jn@m.co'], ['mary@m.co'], ['jn@m.co', 'j0@m.co'], ['m2@m.co', 'mary@m.co']]))
print(sol.find(2), sol.find(3))
sol = Solution(4)
_l, _r = sol.union_shared([['js@m.co', 'jn@m.co'], ['mary@m.co'], ['jn@m.co', 'j0@m.co'], ['m2@m.co', 'mary@m.co']]), {'js@m.co': 0, 'jn@m.co': 0, 'mary@m.co': 1, 'j0@m.co': 2, 'm2@m.co': 3}
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
_l, _r = sol.find(2), 0
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
_l, _r = sol.find(3), 1
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
sol = Solution(3)
_l, _r = sol.union_shared([['g@m.co'], ['g@m.co'], ['g@m.co']]), {'g@m.co': 0}
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
_l, _r = sol.find(1), 0
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
_l, _r = sol.find(2), 0
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
sol = Solution(1)
_l, _r = sol.union_shared([['e@m.co']]), {'e@m.co': 0}
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
sol = Solution(2)
_l, _r = sol.union_shared([['a@m.co', 'b@m.co'], ['c@m.co', 'd@m.co']]), {'a@m.co': 0, 'b@m.co': 0, 'c@m.co': 1, 'd@m.co': 1}
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
_l, _r = sol.find(0), 0
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
_l, _r = sol.find(1), 1
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
sol = Solution(5)
_l, _r = sol.union_shared([['a@m.co'], ['b@m.co', 'a@m.co'], ['c@m.co'], ['d@m.co', 'c@m.co'], ['d@m.co']]), {'a@m.co': 0, 'b@m.co': 1, 'c@m.co': 2, 'd@m.co': 3}
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
_l, _r = sol.find(1), 0
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
_l, _r = sol.find(3), 2
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
_l, _r = sol.find(4), 2
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
