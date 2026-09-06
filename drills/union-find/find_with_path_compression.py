"""
DRILL: Find with Path Compression
TRAINS: union-find
SNIPPET: lcunionfind

Given an employee x, return the head of x. Solution extends UnionFind from
dsa/union_find.py: self.parent[i] is the manager of employee i, and an
employee who is their own manager is a head. Write find so that after the
call every employee on the walk from x reports directly to the head.
Employees off the walk keep their manager. Management chains never
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
"""

from dsa.union_find import UnionFind


class Solution(UnionFind):
    def find(self, x: int) -> int:
        pass


sol = Solution(5)
sol.parent[0] = 1
sol.parent[1] = 2
sol.parent[2] = 3
sol.parent[3] = 4

print(sol.find(0), sol.parent)  # 4 [4, 4, 4, 4, 4]

# sol = Solution(5)
# sol.parent[0] = 1
# sol.parent[1] = 2
# sol.parent[2] = 3
# sol.parent[3] = 4
# assert sol.find(0) == 4
# assert sol.parent == [4, 4, 4, 4, 4]

# sol = Solution(7)
# sol.parent[0] = 1
# sol.parent[1] = 2
# sol.parent[3] = 4
# sol.parent[4] = 5
# assert sol.find(0) == 2
# assert sol.parent == [2, 2, 2, 4, 5, 5, 6]
# assert sol.find(3) == 5
# assert sol.parent == [2, 2, 2, 5, 5, 5, 6]

# sol = Solution(3)
# assert sol.find(0) == 0
# assert sol.parent == [0, 1, 2]

# sol = Solution(4)
# sol.parent[1] = 0
# assert sol.find(1) == 0
# assert sol.parent == [0, 0, 2, 3]

# sol = Solution(1)
# assert sol.find(0) == 0
# assert sol.parent == [0]
