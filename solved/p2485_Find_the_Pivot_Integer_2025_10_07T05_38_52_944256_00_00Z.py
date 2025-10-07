"""
URL: https://leetcode.com/problems/find-the-pivot-integer/description/

2485. Find the Pivot Integer

Given a positive integer n, find the pivot integer x such that:

The sum of all elements strictly to the left of x is equal to the sum of all elements strictly to the right of x.
The ith element (1-indexed) is i. So the array is [1,2,3,...,n].

If no such integer exists, return -1. It is guaranteed that if one exists, it is unique.


Example 1:

Input: n = 8
Output: 6
Explanation: 6 is the pivot integer since: 1 + 2 + 3 + 4 + 5 = 7 + 8 = 15.

Example 2:

Input: n = 1
Output: 1
Explanation: 1 is the pivot integer since: there are no elements to the left or right.

Example 3:

Input: n = 4
Output: -1
Explanation: It can be shown that no such integer x exists.


Constraints:

    1 <= n <= 1000
"""


class Solution:
    def pivotInteger(self, n: int) -> int:
        s = sum(range(1, n + 1))
        t = 0
        for i in range(1, n + 1):
            s -= i
            if t == s:
                return i
            t += i
        return -1


sol = Solution()

# print(sol.pivotInteger(8))  # 6

assert sol.pivotInteger(8) == 6
assert sol.pivotInteger(1) == 1
assert sol.pivotInteger(4) == -1
assert sol.pivotInteger(2) == -1
assert sol.pivotInteger(49) == 35
assert sol.pivotInteger(288) == 204
assert sol.pivotInteger(1000) == -1
