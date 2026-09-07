"""
URL: https://leetcode.com/problems/triangle/description/?envType=problem-list-v2&envId=vn57k9wr

120. Triangle

Given a triangle array, return the minimum path sum from top to bottom.

For each step, you may move to an adjacent number of the row below. More formally, if you are on index i on the current row, you may move to either index i or index i + 1 on the next row.

Example 1:

Input: triangle = [[2],[3,4],[6,5,7],[4,1,8,3]]
Output: 11
Explanation: The triangle looks like:
2
3 4
6 5 7
4 1 8 3
The minimum path sum from top to bottom is 2 + 3 + 5 + 1 = 11 (underlined above).

Example 2:

Input: triangle = [[-10]]
Output: -10

Constraints:

    1 <= triangle.length <= 200
    triangle[0].length == 1
    triangle[i].length == triangle[i - 1].length + 1
    -10^4 <= triangle[i][j] <= 10^4

Follow up: Could you do this using only O(n) extra space, where n is the total number of rows in the triangle?

---

[
[5],
[9, 6],
[4, 6, 8],
[0, 7, 1, 5]
]
"""


class Solution:
    def minimumTotal(self, triangle: List[List[int]]) -> int:
        @cache
        def tmin(row, col):
            if row >= len(triangle) - 1 or col >= len(triangle[row]):
                return triangle[row][col]
            return triangle[row][col] + min(tmin(row + 1, col), tmin(row + 1, col + 1))

        return tmin(0, 0)


sol = Solution()

print(sol.minimumTotal([[2], [3, 4], [6, 5, 7], [4, 1, 8, 3]]))  # 11

assert sol.minimumTotal([[2], [3, 4], [6, 5, 7], [4, 1, 8, 3]]) == 11
assert sol.minimumTotal([[-10]]) == -10

assert sol.minimumTotal([[0]]) == 0
assert sol.minimumTotal([[1], [2, 3]]) == 3
assert sol.minimumTotal([[1], [1, 1], [1, 1, 1]]) == 3
assert sol.minimumTotal([[10000], [10000, 10000], [10000, 10000, 10000]]) == 30000
assert (
    sol.minimumTotal([[-10000], [-10000, -10000], [-10000, -10000, -10000]]) == -30000
)
assert sol.minimumTotal([[1], [2, 2], [3, 3, 3], [4, 4, 4, 4]]) == 10
assert sol.minimumTotal([[1], [2, 3], [3, 1, 5], [4, 1, 1, 4]]) == 5
assert sol.minimumTotal([[5], [9, 6], [4, 6, 8], [0, 7, 1, 5]]) == 18
assert sol.minimumTotal([[1] * i for i in range(1, 201)]) == 200
assert (
    sol.minimumTotal([[i if j != i else -i for j in range(i)] for i in range(1, 201)])
    == 20100
)
assert sol.minimumTotal([[0] * i for i in range(1, 201)]) == 0


# edge cases: one line each, the values are the reference solution's.
assert Solution().minimumTotal([[0]]) == 0  # single_row_zero
assert Solution().minimumTotal([[-10000]]) == -10000  # single_row_most_negative
assert Solution().minimumTotal([[10000]]) == 10000  # single_row_largest
assert Solution().minimumTotal([[1], [2, 3]]) == 3  # two_rows_left_child_smaller
assert Solution().minimumTotal([[1], [3, 2]]) == 3  # two_rows_right_child_smaller
assert Solution().minimumTotal([[-1], [-2, -2]]) == -3  # two_rows_children_equal
assert (
    Solution().minimumTotal([[5], [1, 1], [1, 1, 1]]) == 7
)  # all_entries_below_apex_equal
assert (
    Solution().minimumTotal([[1], [2, 3], [3, 1, 5], [4, 1, 1, 4]]) == 5
)  # cheapest_path_bends_both_ways
assert (
    Solution().minimumTotal([[-1], [2, 3], [1, -1, -3], [4, 1, 8, -5]]) == -6
)  # mixed_signs_four_rows
assert (
    Solution().minimumTotal([[1], [10, 1], [10, 10, 1], [1, 1, 1, 1]]) == 4
)  # greedy_first_step_is_not_on_the_best_path
assert (
    Solution().minimumTotal([[10000] * i for i in range(1, 201)]) == 2000000
)  # 200_rows_all_maximum_values
assert (
    Solution().minimumTotal([[-10000] * i for i in range(1, 201)]) == -2000000
)  # 200_rows_all_minimum_values
