"""
DRILL: Find with Path Compression
SNIPPET: lcunionfind

Given an employee x, return the head of x. Solution extends UnionFind from
dsa/union_find.py: self.parent[i] is the manager of employee i, and an
employee who is their own manager is a head. Write find so that after the
call every employee on the walk from x reports directly to the head.
The manager of an employee off the walk does not change. Management chains never
contain cycles.

Example 1:

Input: parent = [1, 2, 3, 4, 4], find(0)
Output: 4, parent = [4, 4, 4, 4, 4]
Explanation: the walk is 0, 1, 2, 3, 4. All four are rewired to 4.

Example 2:

Input: parent = [1, 2, 2, 4, 5, 5, 6], find(3)
Output: 5, parent = [1, 2, 2, 5, 5, 5, 6]
Explanation: the walk is 3, 4, 5. Employees 0, 1, 2 and 6 are untouched.

Constraints:

    1 <= n <= 1000
    0 <= x < n
    parent is free of cycles whenever find is called

    REQUIRED: must leave every employee on the walk one hop from the head.
    NO partial compression (one level up is not enough); NO copy of parent.
---
forgot to assign the result so self.parent[x] :self.parent[x] = self.find(self.parent[x])
hinted
"""

from dsa.union_find import UnionFind


# mu 0.12
# class Solution extends UnionFind
#   def find(x: int) -> int
#     if x == self.parent[x]
#       return x
#     self.parent[x] = self.find(self.parent[x])
#     return self.parent[x]

class Solution(UnionFind):
    def find(self, x: int) -> int:
        if x == self.parent[x]:
            return x
        self.parent[x] = self.find(self.parent[x])
        return self.parent[x]


sol = Solution(5)
sol.parent[0] = 1
sol.parent[1] = 2
sol.parent[2] = 3
sol.parent[3] = 4
print(sol.find(0), sol.parent)
sol = Solution(5)
sol.parent[0] = 1
sol.parent[1] = 2
sol.parent[2] = 3
sol.parent[3] = 4
_l, _r = sol.find(0), 4
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
_l, _r = sol.parent, [4, 4, 4, 4, 4]
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
sol = Solution(7)
sol.parent[0] = 1
sol.parent[1] = 2
sol.parent[3] = 4
sol.parent[4] = 5
_l, _r = sol.find(0), 2
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
_l, _r = sol.parent, [2, 2, 2, 4, 5, 5, 6]
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
_l, _r = sol.find(3), 5
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
_l, _r = sol.parent, [2, 2, 2, 5, 5, 5, 6]
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
sol = Solution(3)
_l, _r = sol.find(0), 0
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
_l, _r = sol.parent, [0, 1, 2]
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
sol = Solution(4)
sol.parent[1] = 0
_l, _r = sol.find(1), 0
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
_l, _r = sol.parent, [0, 0, 2, 3]
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
sol = Solution(1)
_l, _r = sol.find(0), 0
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
_l, _r = sol.parent, [0]
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
