"""
DRILL: Companies Left

Given self.parent, return the number of companies. Solution extends
UnionFind from dsa/union_find.py: self.parent[i] is the manager of
employee i, and an employee who is their own manager is a head. A company
is one head together with every employee whose chain of managers reaches
that head. Management chains never contain cycles.

Example 1:

Input: parent = [1, 2, 2, 4, 5, 5]
Output: 2
Explanation: 0, 1 and 2 reach head 2. 3, 4 and 5 reach head 5.

Example 2:

Input: parent = [1, 2, 5, 4, 5, 5]
Output: 1
Explanation: every employee reaches head 5.

Constraints:

    1 <= n <= 1000
    parent is free of cycles

    REQUIRED: must run in O(n) time with one pass over self.parent. NO
    find calls; NO set or dict of heads.
"""

from dsa.union_find import UnionFind


class Solution(UnionFind):
    def countCompanies(self) -> int:
        return sum(x == p for x, p in enumerate(self.parent))


sol = Solution(6)
sol.parent = [1, 2, 2, 4, 5, 5]

print(sol.countCompanies())  # 2

# two heads
sol = Solution(6)
sol.parent = [1, 2, 2, 4, 5, 5]
assert sol.countCompanies() == 2

# one head, after union(0, 3)
sol = Solution(6)
sol.parent = [1, 2, 5, 4, 5, 5]
assert sol.countCompanies() == 1

# nobody merged yet
sol = Solution(4)
assert sol.countCompanies() == 4

# one employee
sol = Solution(1)
assert sol.countCompanies() == 1

# heads at the first, a middle and the last index
sol = Solution(7)
sol.parent = [0, 0, 1, 3, 3, 6, 6]
assert sol.countCompanies() == 3

# one chain, the head at the last index
sol = Solution(5)
sol.parent = [1, 2, 3, 4, 4]
assert sol.countCompanies() == 1

# everybody under 0
sol = Solution(4)
sol.parent = [0, 0, 0, 0]
assert sol.countCompanies() == 1

# a head every third employee
sol = Solution(999)
sol.parent = [x if x % 3 == 0 else x - 1 for x in range(999)]
assert sol.countCompanies() == 333
