"""
URL: https://leetcode.com/problems/pascals-triangle/description/

118. Pascal's Triangle

Given an integer numRows, return the first numRows of Pascal's triangle.

In Pascal's triangle, each number is the sum of the two numbers directly above it as shown:


Example 1:
Input: numRows = 5
Output: [[1],[1,1],[1,2,1],[1,3,3,1],[1,4,6,4,1]]
Example 2:
Input: numRows = 1
Output: [[1]]


Constraints:

        1 <= numRows <= 30
"""

from itertools import pairwise


class Solution:
    def generate(self, numRows: int) -> List[List[int]]:
        res = [[1], [1, 1]]
        prev = res[-1]
        for _ in range(numRows - 2):
            res.append([1] + [a + b for a, b in pairwise(prev)] + [1])
            prev = res[-1]
        return res[:numRows]


sol = Solution()


res = sol.generate(1)
assert res == [[1]]

res = sol.generate(2)
assert res == [[1], [1, 1]]

res = sol.generate(3)
assert res == [[1], [1, 1], [1, 2, 1]]

res = sol.generate(5)
assert res == [[1], [1, 1], [1, 2, 1], [1, 3, 3, 1], [1, 4, 6, 4, 1]]
