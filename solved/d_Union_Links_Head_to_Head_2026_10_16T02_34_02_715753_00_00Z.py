"""
DRILL: Union Links Head to Head
SNIPPET: lcunionunion

Given employees a and b, merge their companies and return True, or return
False when they are already one company. Solution extends UnionFind from
dsa/union_find.py: self.parent[i] is the manager of employee i, an
employee who is their own manager is a head, and self.find(x) returns the
head of x. Write union so that the head of a reports to the head of b.
Neither a nor b moves. Management chains never contain cycles.

Example 1:

Input: parent = [1, 2, 2, 4, 5, 5], union(0, 3)
Output: True, parent = [1, 2, 5, 4, 5, 5]
Explanation: the head of 0 is 2 and the head of 3 is 5. Only the entry of
2 changes.

Example 2:

Input: parent = [1, 2, 2, 3], union(0, 1)
Output: False, parent unchanged
Explanation: 0 and 1 both have head 2.

Constraints:

    1 <= n <= 1000
    0 <= a, b < n
    parent is free of cycles whenever union is called

    REQUIRED: must change at most one entry of self.parent per call. NO
    reassignment of a or b themselves; NO find of your own.
"""

from dsa.union_find import UnionFind


# mu 0.11
# class Solution extends UnionFind
#   def union(a: int, b: int) -> bool
#     pa = self.find(a)
#     pb = self.find(b)
#     if pa != pb
#       self.parent[pa] = pb
#       return true
#     return false

class Solution(UnionFind):
    def union(self, a: int, b: int) -> bool:
        pa = self.find(a)
        pb = self.find(b)
        if pa != pb:
            self.parent[pa] = pb
            return True
        return False


sol = Solution(6)
sol.parent[0] = 1
sol.parent[1] = 2
sol.parent[3] = 4
sol.parent[4] = 5
sol.union(0, 3)
print(sol.parent)
sol = Solution(2)
_l, _r = sol.union(0, 1), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.parent, [1, 1]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol = Solution(4)
sol.union(0, 1)
_l, _r = sol.parent, [1, 1, 2, 3]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol = Solution(4)
sol.union(2, 0)
_l, _r = sol.parent, [0, 1, 0, 3]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol = Solution(6)
sol.parent[0] = 1
sol.parent[1] = 2
sol.parent[3] = 4
sol.parent[4] = 5
_l, _r = sol.union(0, 3), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.parent, [1, 2, 5, 4, 5, 5]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol = Solution(4)
sol.parent[0] = 1
sol.parent[1] = 2
_l, _r = sol.union(0, 1), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.parent, [1, 2, 2, 3]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol = Solution(3)
_l, _r = sol.union(0, 0), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.parent, [0, 1, 2]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol = Solution(4)
sol.union(0, 1)
_l, _r = sol.parent, [1, 1, 2, 3]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.union(2, 3)
_l, _r = sol.parent, [1, 1, 3, 3]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.union(0, 2)
_l, _r = sol.parent, [1, 3, 3, 3]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol = Solution(1)
sol.union(0, 0)
_l, _r = sol.parent, [0]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
