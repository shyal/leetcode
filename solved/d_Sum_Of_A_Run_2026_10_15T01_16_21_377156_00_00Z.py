"""
DRILL: Sum Of A Run
TRAINS: consecutive-sum-split

Given two positive integers n and k, return the sum of the k consecutive
integers that start at n: n + (n + 1) + ... + (n + k - 1).

Example 1:

Input: n = 4, k = 3
Output: 15
Explanation: 4 + 5 + 6 = 15.

Example 2:

Input: n = 1, k = 100
Output: 5050

Example 3:

Input: n = 7, k = 1
Output: 7
Explanation: A run of one integer is the integer itself.

Constraints:

    1 <= n <= 10^9
    1 <= k <= 10^5

    REQUIRED: O(1), one arithmetic expression. NO loop. NO sum. NO range.
---
Learning
"""


# mu 0.10
# class Solution
#   def sumOfRun(n: int, k: int) -> int
#     k * (2 * n + k - 1) // 2

class Solution:
    def sumOfRun(self, n: int, k: int) -> int:
        return k * (2 * n + k - 1) // 2


sol = Solution()
print(sol.sumOfRun(4, 3))
