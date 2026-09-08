"""
URL: https://leetcode.com/problems/arranging-coins/description/?envType=problem-list-v2&envId=vn57k9wr

441. Arranging Coins

You have n coins and you want to build a staircase with these coins. The staircase consists of k rows where the ith row has exactly i coins. The last row of the staircase may be incomplete.

Given the integer n, return the number of complete rows of the staircase you will build.

Example 1:

Input: n = 5
Output: 2
Explanation: Because the 3rd row is incomplete, we return 2.

Example 2:

Input: n = 8
Output: 3
Explanation: Because the 4th row is incomplete, we return 3.

Constraints:

    1 <= n <= 2^31 - 1
"""


class Solution:
    def arrangeCoins(self, n: int) -> int:
        left, right = 0, n
        while left <= right:
            mid = (left + right) // 2
            res = (mid * (mid + 1)) // 2
            if res < n:
                left = mid + 1
            elif res > n:
                right = mid - 1
            else:
                return mid
        return left - 1


sol = Solution()

assert sol.arrangeCoins(5) == 2
assert sol.arrangeCoins(8) == 3

assert sol.arrangeCoins(1) == 1
assert sol.arrangeCoins(0) == 0
assert sol.arrangeCoins(2) == 1
assert sol.arrangeCoins(3) == 2
assert sol.arrangeCoins(10) == 4
assert sol.arrangeCoins(15) == 5
assert sol.arrangeCoins(16) == 5
assert sol.arrangeCoins(1000000000) == 44720
assert sol.arrangeCoins(2147483647) == 65535
assert sol.arrangeCoins(6) == 3
assert sol.arrangeCoins(7) == 3
assert sol.arrangeCoins(500000000) == 31622
