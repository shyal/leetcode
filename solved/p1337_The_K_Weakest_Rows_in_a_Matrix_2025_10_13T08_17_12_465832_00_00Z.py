"""
URL: https://leetcode.com/problems/the-k-weakest-rows-in-a-matrix/description/

1337. The K Weakest Rows in a Matrix

You are given an m x n binary matrix mat of 1's (representing soldiers) and 0's (representing civilians). The soldiers are positioned in front of the civilians. That is, all the 1's will appear to the left of all the 0's in each row.

A row i is weaker than a row j if one of the following is true:

    The number of soldiers in row i is less than the number of soldiers in row j.
    Both rows have the same number of soldiers and i < j.

Return the indices of the k weakest rows in the matrix ordered from weakest to strongest.


Example 1:

Input: mat = [[1,1,0,0,0],[1,1,1,1,0],[1,0,0,0,0],[1,1,0,0,0],[1,1,1,1,1]], k = 3
Output: [2,0,3]
Explanation:
The number of soldiers in each row is:
- row 0: 2
- row 1: 4
- row 2: 1
- row 3: 2
- row 4: 5
The rows ordered from the weakest to the strongest are [2,0,3,1,4].

Example 2:

Input: mat = [[1,0,0,0],[1,1,1,1],[1,0,0,0],[1,0,0,0]], k = 2
Output: [0,2]
Explanation:
The number of soldiers in each row is:
- row 0: 1
- row 1: 4
- row 2: 1
- row 3: 1
The rows ordered from the weakest to the strongest are [0,2,3,1].


Constraints:

    m == mat.length
    n == mat[i].length
    2 <= m, n <= 100
    1 <= k <= m
    mat[i][j] is either 0 or 1.
"""


class Solution:
    def kWeakestRows(self, mat: List[List[int]], k: int) -> List[int]:
        mat = [*sorted(enumerate(mat), key=lambda x: (sum(e == 1 for e in x[1]), x[0]))]
        return [x[0] for x in mat][:k]


sol = Solution()

# print(
#     sol.kWeakestRows(
#         [
#             [1, 1, 0, 0, 0],
#             [1, 1, 1, 1, 0],
#             [1, 0, 0, 0, 0],
#             [1, 1, 0, 0, 0],
#             [1, 1, 1, 1, 1],
#         ],
#         3,
#     )
# )  # [2,0,3]

assert sol.kWeakestRows(
    [
        [1, 1, 0, 0, 0],
        [1, 1, 1, 1, 0],
        [1, 0, 0, 0, 0],
        [1, 1, 0, 0, 0],
        [1, 1, 1, 1, 1],
    ],
    3,
) == [2, 0, 3]
assert sol.kWeakestRows(
    [[1, 0, 0, 0], [1, 1, 1, 1], [1, 0, 0, 0], [1, 0, 0, 0]], 2
) == [0, 2]
assert sol.kWeakestRows([[1, 0], [1, 0]], 2) == [0, 1]
assert sol.kWeakestRows([[1, 1], [1, 0]], 2) == [1, 0]
assert sol.kWeakestRows([[0, 0, 0], [1, 0, 0], [0, 0, 0]], 2) == [0, 2]
assert sol.kWeakestRows([[1, 1, 1], [1, 1, 1]], 1) == [0]
assert sol.kWeakestRows([[1, 0], [0, 0]], 1) == [1]
assert sol.kWeakestRows([[1, 1, 0], [1, 0, 0], [1, 1, 1], [1, 1, 0]], 3) == [1, 0, 3]
assert sol.kWeakestRows(
    [
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
    ],
    4,
) == [0, 1, 3, 4]
assert sol.kWeakestRows([[1, 1], [0, 0]], 2) == [1, 0]
assert sol.kWeakestRows([[0, 0], [0, 0], [0, 0]], 3) == [0, 1, 2]
assert sol.kWeakestRows(
    [[1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [1, 1, 1, 1, 1]], 4
) == [0, 1, 2, 3]
