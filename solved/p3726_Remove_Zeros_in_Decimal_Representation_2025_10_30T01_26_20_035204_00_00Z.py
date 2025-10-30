"""
URL: https://leetcode.com/problems/remove-zeros-in-decimal-representation/description/?envType=problem-list-v2&envId=vn57k9wr

3726. Remove Zeros in Decimal Representation

You are given a positive integer n.

Return the integer obtained by removing all zeros from the decimal representation of n.

Example 1:

Input: n = 1020030
Output: 123
Explanation: After removing all zeros from 1020030, we get 123.

Example 2:

Input: n = 1
Output: 1
Explanation: 1 has no zero in its decimal representation. Therefore, the answer is 1.

Constraints:

    1 <= n <= 10^15

"""


class Solution:

    def getDigits(self, num):
        digits = []
        while num:
            digits.append(num % 10)
            num //= 10
        return digits

    def removeZeros(self, n: int) -> int:
        res = 0
        digits = self.getDigits(n)
        for x in [x for x in digits[::-1] if x != 0]:
            res = res * 10 + x
        return res


sol = Solution()

# print(sol.removeZeros(1020030))  # 123

assert sol.removeZeros(1020030) == 123
assert sol.removeZeros(1) == 1
assert sol.removeZeros(10) == 1
assert sol.removeZeros(100) == 1
assert sol.removeZeros(101) == 11
assert sol.removeZeros(110) == 11
assert sol.removeZeros(1000000000000000) == 1
assert sol.removeZeros(123456789012345) == 12345678912345
assert sol.removeZeros(111111111111111) == 111111111111111
assert sol.removeZeros(102000000000000) == 12
