"""
URL: https://leetcode.com/problems/matrix-cells-in-distance-order/description/?envType=problem-list-v2&envId=vn57k9wr

1030. Matrix Cells in Distance Order

You are given four integers: rows, cols, rCenter, and cCenter.

These represent a rows x cols grid, where each cell has coordinates (r, c). You are currently located at the cell (rCenter, cCenter).

Your task is to return a list of all cell coordinates in the grid, sorted by their Manhattan distance from (rCenter, cCenter), starting from the smallest distance to the largest.

The Manhattan distance between two cells (r1, c1) and (r2, c2) is defined as:

|r1 - r2| + |c1 - c2|

If multiple cells have the same distance, they can appear in any order relative to each other.

⸻

Example 1:

Input: rows = 1, cols = 2, rCenter = 0, cCenter = 0
Output: [[0,0], [0,1]]
Explanation: Distances from (0,0) → [0, 1].

⸻

Example 2:

Input: rows = 2, cols = 2, rCenter = 0, cCenter = 1
Output: [[0,1], [0,0], [1,1], [1,0]]
Explanation: Distances from (0,1) → [0, 1, 1, 2].
Other valid outputs: [[0,1], [1,1], [0,0], [1,0]].

⸻

Example 3:

Input: rows = 2, cols = 3, rCenter = 1, cCenter = 2
Output: [[1,2], [0,2], [1,1], [0,1], [1,0], [0,0]]
Explanation: Distances from (1,2) → [0, 1, 1, 2, 2, 3].
Other valid outputs with the same ordering by distance are also acceptable.

⸻

Constraints:
        •	1 ≤ rows, cols ≤ 100
        •	0 ≤ rCenter < rows
        •	0 ≤ cCenter < cols

---

Terribly written question.

"""


class Solution:
    def allCellsDistOrder(
        self, rows: int, cols: int, rCenter: int, cCenter: int
    ) -> List[List[int]]:
        res = []
        for row in range(rows):
            for col in range(cols):
                res.append([row, col])
        res.sort(key=lambda x: abs(x[0] - rCenter) + abs(x[1] - cCenter))
        return res


sol = Solution()

assert sol.allCellsDistOrder(1, 2, 0, 0) == [[0, 0], [0, 1]]
assert sol.allCellsDistOrder(2, 2, 0, 1) == [[0, 1], [0, 0], [1, 1], [1, 0]]
assert sol.allCellsDistOrder(2, 3, 1, 2) == [
    [1, 2],
    [0, 2],
    [1, 1],
    [0, 1],
    [1, 0],
    [0, 0],
]
assert sol.allCellsDistOrder(1, 1, 0, 0) == [[0, 0]]
assert sol.allCellsDistOrder(2, 2, 0, 0) == [[0, 0], [0, 1], [1, 0], [1, 1]]
assert sol.allCellsDistOrder(2, 2, 1, 1) == [[1, 1], [0, 1], [1, 0], [0, 0]]
assert sol.allCellsDistOrder(3, 1, 1, 0) == [[1, 0], [0, 0], [2, 0]]
assert sol.allCellsDistOrder(1, 3, 0, 1) == [[0, 1], [0, 0], [0, 2]]
assert sol.allCellsDistOrder(3, 3, 0, 0) == [
    [0, 0],
    [0, 1],
    [1, 0],
    [0, 2],
    [1, 1],
    [2, 0],
    [1, 2],
    [2, 1],
    [2, 2],
]
