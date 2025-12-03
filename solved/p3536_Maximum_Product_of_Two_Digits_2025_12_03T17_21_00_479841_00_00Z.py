"""
URL: https://leetcode.com/problems/maximum-product-of-two-digits/description/?envType=problem-list-v2&envId=vn57k9wr

3536. Maximum Product of Two Digits

You are given a positive integer n.

Return the maximum product of any two digits in n.

Note: You may use the same digit twice if it appears more than once in n.

Example 1:

Input: n = 31
Output: 3
Explanation:
- The digits of n are [3, 1].
- The possible products of any two digits are: 3 * 1 = 3.
- The maximum product is 3.

Example 2:

Input: n = 22
Output: 4
Explanation:
- The digits of n are [2, 2].
- The possible products of any two digits are: 2 * 2 = 4.
- The maximum product is 4.

Example 3:

Input: n = 124
Output: 8
Explanation:
- The digits of n are [1, 2, 4].
- The possible products of any two digits are: 1 * 2 = 2, 1 * 4 = 4, 2 * 4 = 8.
- The maximum product is 8.

Constraints:
- 10 <= n <= 10^9
"""

class Solution:

    def getDigits(self, n):
        digits = []
        while n:
            digits.append(n % 10)
            n //= 10
        return digits

    def maxProduct(self, n: int) -> int:
        return max(a * b for a, b in combinations(self.getDigits(n), 2))


sol = Solution()

print(sol.maxProduct(31))  # 3


assert sol.maxProduct(31) == 3
assert sol.maxProduct(22) == 4
assert sol.maxProduct(124) == 8
assert sol.maxProduct(10) == 0
assert sol.maxProduct(11) == 1
assert sol.maxProduct(99) == 81
assert sol.maxProduct(90) == 0
assert sol.maxProduct(100) == 0
assert sol.maxProduct(101) == 1
assert sol.maxProduct(202) == 4
assert sol.maxProduct(201) == 2
assert sol.maxProduct(999999999) == 81
assert sol.maxProduct(123456789) == 72
assert sol.maxProduct(111111111) == 1
assert sol.maxProduct(987654321) == 72
assert sol.maxProduct(20) == 0
assert sol.maxProduct(1000000000) == 0
assert sol.maxProduct(992) == 81
assert sol.maxProduct(13579) == 63