"""
URL: https://leetcode.com/problems/minimum-sum-of-four-digit-number-after-splitting-digits/description/?envType=problem-list-v2&envId=vn57k9wr

2160. Minimum Sum of Four Digit Number After Splitting Digits

You are given a positive integer num consisting of exactly four digits. Split num into two new integers new1 and new2 by using the digits found in num. Leading zeros are allowed in new1 and new2, and all the digits found in num must be used.

For example, given num = 2932, you have the following digits: two 2's, one 9 and one 3. Some of the possible pairs [new1, new2] are [22, 93], [23, 92], [223, 9] and [2, 329].

Return the minimum possible sum of new1 and new2.

Example 1:

Input: num = 2932
Output: 52
Explanation: Some possible pairs [new1, new2] are [29, 23], [223, 9], etc.
The minimum sum can be obtained by the pair [29, 23]: 29 + 23 = 52.

Example 2:

Input: num = 4009
Output: 13
Explanation: Some possible pairs [new1, new2] are [0, 49], [490, 0], etc.
The minimum sum can be obtained by the pair [4, 9]: 4 + 9 = 13.

Constraints:

    1000 <= num <= 9999
"""


class Solution:

    def getDigits(self, num):
        digits = []
        while num:
            digits.append(num % 10)
            num = num // 10
        return digits

    def minimumSum(self, num: int) -> int:
        digits = self.getDigits(num)
        digits.sort(reverse=True)
        A = digits.pop() * 10
        B = digits.pop() * 10
        A += digits.pop()
        B += digits.pop()
        return A + B


sol = Solution()

# print(sol.minimumSum(2932))  # 52

assert sol.minimumSum(2932) == 52
assert sol.minimumSum(4009) == 13

assert sol.minimumSum(1000) == 1
assert sol.minimumSum(9999) == 198
assert sol.minimumSum(1111) == 22
assert sol.minimumSum(2222) == 44
assert sol.minimumSum(9090) == 18
assert sol.minimumSum(1234) == 37
assert sol.minimumSum(4321) == 37
assert sol.minimumSum(8080) == 16
assert sol.minimumSum(1010) == 2
assert sol.minimumSum(9900) == 18
assert sol.minimumSum(5678) == 125
assert sol.minimumSum(8765) == 125
