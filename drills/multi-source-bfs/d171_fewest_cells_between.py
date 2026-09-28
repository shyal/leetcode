"""
DRILL: Fewest Cells Between
TRAINS: multi-source-bfs

Given an n x m grid of 0, 1 and 2, return the fewest 0 cells on a path from
any 1 cell to any 2 cell. Each step of a path goes to the cell above, below,
left or right. The grid holds at least one 1 and at least one 2, and some
path between them exists.

Example 1:

Input: grid = [[1, 0, 0], [0, 0, 0], [0, 0, 2]]
Output: 3
Explanation: Right, right, down, down passes three 0 cells. No path passes
fewer.

Example 2:

Input: grid = [[1, 2], [0, 0]]
Output: 0
Explanation: The 1 and the 2 touch.

Example 3:

Input: grid = [[2, 0, 1, 0, 0, 0, 2]]
Output: 1
Explanation: The 2 on the left is nearer than the 2 on the right.

Constraints:

    1 <= n, m <= 400
    grid[r][c] is 0, 1 or 2

    REQUIRED: O(n * m) time, one breadth-first search whose queue starts with
    every 1 cell, returning on the first 2 popped. NO distance table, NO
    second search.
"""


class Solution:
    def fewest(self, grid: List[List[int]]) -> int:
        pass


sol = Solution()

print(sol.fewest([[1, 0, 0], [0, 0, 0], [0, 0, 2]]))  # 3

# assert sol.fewest([[1, 0, 0], [0, 0, 0], [0, 0, 2]]) == 3
# assert sol.fewest([[1, 2], [0, 0]]) == 0
# assert sol.fewest([[2, 0, 1, 0, 0, 0, 2]]) == 1
# assert sol.fewest([[1, 0, 0, 2]]) == 2
# assert sol.fewest([[2, 0, 0, 1]]) == 2
# assert sol.fewest([[1], [0], [0], [0], [2]]) == 3
# assert sol.fewest([[1, 1, 0, 0], [1, 0, 0, 0], [0, 0, 0, 2], [0, 0, 2, 2]]) == 3
# assert sol.fewest([[1, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 2], [0, 0, 0, 2, 2]]) == 6
# assert sol.fewest([[1, 1, 1, 1, 1], [1, 0, 0, 0, 1], [1, 0, 2, 0, 1], [1, 0, 0, 0, 1], [1, 1, 1, 1, 1]]) == 1
# assert sol.fewest([[1, 0, 0, 0, 1], [0, 0, 0, 0, 0], [0, 0, 2, 0, 0], [0, 0, 0, 0, 0], [1, 0, 0, 0, 1]]) == 3
# assert sol.fewest([[1, 0, 2], [0, 0, 0], [2, 0, 1]]) == 1
# assert sol.fewest([[1, 0, 0, 0, 0, 0, 0, 0, 0, 2]]) == 8
# assert sol.fewest([[1] + [0] * 399] + [[0] * 400 for _ in range(398)] + [[0] * 399 + [2]]) == 797
# assert sol.fewest([[1] * 400] + [[0] * 400 for _ in range(398)] + [[2] * 400]) == 398
