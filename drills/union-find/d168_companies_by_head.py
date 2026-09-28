"""
DRILL: Companies By Head

Given self.parent, return the dict groups mapping each head to the list
of employees in that head's company, in increasing order. Solution
extends UnionFind from dsa/union_find.py: self.parent[i] is the manager
of employee i, an employee who is their own manager is a head, and
self.find(x) returns the head of x. Management chains never contain
cycles.

Example 1:

Input: parent = [1, 2, 2, 4, 5, 5]
Output: {2: [0, 1, 2], 5: [3, 4, 5]}
Explanation: 0, 1 and 2 reach head 2. 3, 4 and 5 reach head 5.

Example 2:

Input: parent = [1, 2, 5, 4, 5, 5]
Output: {5: [0, 1, 2, 3, 4, 5]}
Explanation: every employee reaches head 5.

Constraints:

    1 <= n <= 1000
    parent is free of cycles

    REQUIRED: must call self.find once per employee. NO comparison of
    employees in pairs; NO sort.
"""

from dsa.union_find import UnionFind


class Solution(UnionFind):
    def groups(self) -> Dict[int, List[int]]:
        pass


sol = Solution(6)
sol.parent = [1, 2, 2, 4, 5, 5]

print(dict(sol.groups()))  # {2: [0, 1, 2], 5: [3, 4, 5]}

## two heads
# sol = Solution(6)
# sol.parent = [1, 2, 2, 4, 5, 5]
# assert sol.groups() == {2: [0, 1, 2], 5: [3, 4, 5]}

## one head, after union(0, 3)
# sol = Solution(6)
# sol.parent = [1, 2, 5, 4, 5, 5]
# assert sol.groups() == {5: [0, 1, 2, 3, 4, 5]}

## nobody merged yet
# sol = Solution(4)
# assert sol.groups() == {0: [0], 1: [1], 2: [2], 3: [3]}

## one employee
# sol = Solution(1)
# assert sol.groups() == {0: [0]}

## heads at the first, a middle and the last index
# sol = Solution(7)
# sol.parent = [0, 0, 1, 3, 3, 6, 6]
# assert sol.groups() == {0: [0, 1, 2], 3: [3, 4], 6: [5, 6]}

## one chain, the head at the last index
# sol = Solution(5)
# sol.parent = [1, 2, 3, 4, 4]
# assert sol.groups() == {4: [0, 1, 2, 3, 4]}

## everybody under 0
# sol = Solution(4)
# sol.parent = [0, 0, 0, 0]
# assert sol.groups() == {0: [0, 1, 2, 3]}

## a head every third employee
# sol = Solution(9)
# sol.parent = [x if x % 3 == 0 else x - 1 for x in range(9)]
# assert sol.groups() == {0: [0, 1, 2], 3: [3, 4, 5], 6: [6, 7, 8]}
