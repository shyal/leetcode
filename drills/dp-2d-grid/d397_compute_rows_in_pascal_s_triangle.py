"""
EPI 5.20 Compute rows in Pascal's Triangle

Given an integer n, return the first n rows of Pascal's triangle. Row 0
is [1]. Row i has i + 1 elements: the first and the last are 1, and
each other element is the sum of the two elements above it in row
i - 1.

Example 1:

Input: n = 5
Output: [[1], [1, 1], [1, 2, 1], [1, 3, 3, 1], [1, 4, 6, 4, 1]]
Explanation: In row 4, 6 = 3 + 3 and 4 = 1 + 3.

Example 2:

Input: n = 1
Output: [[1]]

Example 3:

Input: n = 0
Output: []

Constraints:

    0 <= n <= 1000

    REQUIRED: O(n^2) time. NO comb(), NO factorial().
"""


class Solution:
    def generate_pascal_triangle(self, n: int) -> list[list[int]]:
        pass


sol = Solution()

print(sol.generate_pascal_triangle(5))  # [[1], [1, 1], [1, 2, 1], [1, 3, 3, 1], [1, 4, 6, 4, 1]]

# assert sol.generate_pascal_triangle(5) == [[1], [1, 1], [1, 2, 1], [1, 3, 3, 1], [1, 4, 6, 4, 1]]
# assert sol.generate_pascal_triangle(1) == [[1]]
# assert sol.generate_pascal_triangle(0) == []
# assert sol.generate_pascal_triangle(2) == [[1], [1, 1]]
# assert sol.generate_pascal_triangle(3) == [[1], [1, 1], [1, 2, 1]]
# assert sol.generate_pascal_triangle(6)[-1] == [1, 5, 10, 10, 5, 1]
# assert sol.generate_pascal_triangle(8)[7] == [1, 7, 21, 35, 35, 21, 7, 1]
# assert sol.generate_pascal_triangle(11)[10] == [1, 10, 45, 120, 210, 252, 210, 120, 45, 10, 1]
# T = sol.generate_pascal_triangle(30)
# assert len(T) == 30 and len(T[29]) == 30 and T[29][14] == 77558760
# assert all(len(T[i]) == i + 1 for i in range(30))
# T = sol.generate_pascal_triangle(1000)
# assert len(T) == 1000 and T[999][1] == 999 and T[999][-2] == 999
# assert sum(T[999]) == 2 ** 999 and T[999] == T[999][::-1]
# assert T[999][2] == 999 * 998 // 2
