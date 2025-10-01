"""
URL: https://leetcode.com/problems/pascals-triangle-ii/description/

119. Pascal's Triangle II

Given an integer rowIndex, return the rowIndexth (0-indexed) row of the Pascal's triangle.

In Pascal's triangle, each number is the sum of the two numbers directly above it as shown:


Example 1:
Input: rowIndex = 3
Output: [1,3,3,1]
Example 2:
Input: rowIndex = 0
Output: [1]
Example 3:
Input: rowIndex = 1
Output: [1,1]


Constraints:

    0 <= rowIndex <= 33


Follow up: Could you optimize your algorithm to use only O(rowIndex) extra space?

-------

so the rows are:

1
1
12
132
146

"""


class Solution:
    def getRow(self, rowIndex: int) -> List[int]:
        if rowIndex == 0:
            return [1]
        dp = [1, 1]
        for i in range(2, rowIndex + 1):
            dp = [1] + [a + b for a, b in pairwise(dp)] + [1]
        return dp


sol = Solution()
assert sol.getRow(3) == [1, 3, 3, 1]
assert sol.getRow(0) == [1]
assert sol.getRow(1) == [1, 1]


