"""
URL: https://leetcode.com/problems/consecutive-numbers-sum/description/?envType=problem-list-v2&envId=vn57k9wr

829. Consecutive Numbers Sum

Given an integer n, return the number of ways you can write n as the sum of consecutive positive integers.

Example 1:

Input: n = 5
Output: 2
Explanation: 5 = 2 + 3

Example 2:

Input: n = 9
Output: 3
Explanation: 9 = 4 + 5 = 2 + 3 + 4

Example 3:

Input: n = 15
Output: 4
Explanation: 15 = 8 + 7 = 4 + 5 + 6 = 1 + 2 + 3 + 4 + 5

Constraints:

    1 <= n <= 10^9
---
if we divide 15 by 2, we get 7.5 + 7.5, but if we carry the fraction over
we get 7 + 8

that's one way

we can also divide it by 3: which is 5 + 5 + 5 and steal 1 to become: 4 + 5 + 6

interestingly 16 only has one way? 16 / 2 = 8 + 8

ok this is super hard
"""


# mu 0.10
# class Solution
#   def consecutiveNumbersSum(n: int) -> int
#     ret res = 0
#     k = 1
#     while k * (k - 1) // 2 < n
#       if (n - k * (k - 1) // 2) % k == 0
#         res += 1
#       k += 1

class Solution:
    def consecutiveNumbersSum(self, n: int) -> int:
        res = 0
        k = 1
        while k * (k - 1) // 2 < n:
            if (n - k * (k - 1) // 2) % k == 0:
                res += 1
            k += 1
        return res


sol = Solution()
print(sol.consecutiveNumbersSum(5))


# FAILED: walked away after 29m 32s; no working solution.
# Judge the move the defect is in as struggled, not clean. A move the code never reached gets no verdict.
