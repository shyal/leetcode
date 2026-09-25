"""
DRILL: Reach The Far Corner
TRAINS: graph-bfs-shortest

Given an n x m grid of integers and an integer k, return True when you can
walk from cell (0, 0) to cell (n - 1, m - 1). Each move goes to the cell
above, below, left or right. You may stand only on cells whose value is at
least k, and that includes the first and the last cell.

Example 1:

Input: grid = [[3, 1, 2], [3, 0, 2], [3, 3, 3]], k = 3
Output: True
Explanation: Down the left column, then along the bottom row.

Example 2:

Input: grid = [[4, 1], [1, 4]], k = 2
Output: False
Explanation: Both corners hold 4, but no move goes diagonally.

Example 3:

Input: grid = [[1, 5], [5, 5]], k = 2
Output: False
Explanation: Cell (0, 0) holds 1, so you cannot stand on it.

Constraints:

    1 <= n, m <= 400
    0 <= grid[r][c] <= 10^6
    0 <= k <= 10^6

    REQUIRED: O(n * m) time, one breadth-first search from (0, 0). A cell
    below k must never be entered, the first cell included. NO recursion.
"""


class Solution:
    def reach(self, grid: List[List[int]], k: int) -> bool:
        pass


sol = Solution()

print(sol.reach([[3, 1, 2], [3, 0, 2], [3, 3, 3]], 3))  # True

# assert sol.reach([[3, 1, 2], [3, 0, 2], [3, 3, 3]], 3) is True
# assert sol.reach([[3, 1, 2], [3, 0, 2], [3, 3, 3]], 4) is False
# assert sol.reach([[4, 1], [1, 4]], 2) is False
# assert sol.reach([[1, 5], [5, 5]], 2) is False
# assert sol.reach([[5, 5], [5, 1]], 2) is False
# assert sol.reach([[7]], 7) is True
# assert sol.reach([[6]], 7) is False
# assert sol.reach([[0, 0], [0, 0]], 0) is True
# assert sol.reach([[2, 2, 2, 2, 2]], 2) is True
# assert sol.reach([[2, 2, 1, 2, 2]], 2) is False
# assert sol.reach([[5, 5, 5], [0, 0, 5], [5, 5, 5], [5, 0, 0], [5, 5, 5]], 5) is True
# assert sol.reach([[5, 5, 5], [0, 0, 5], [5, 5, 4], [5, 0, 0], [5, 5, 5]], 5) is False
# assert sol.reach([[9] * 400 for _ in range(400)], 9) is True
# assert sol.reach([[9] * 400 for _ in range(399)] + [[9] * 399 + [8]], 9) is False
