"""
URL: https://leetcode.com/problems/minimum-sum-of-four-digit-number-after-splitting-digits/description/

2160. Minimum Sum of Four Digit Number After Splitting Digits

You are given a positive integer num consisting of exactly four digits. Split num into two new integers new1 and new2 by using the digits. Leading zeros are allowed in new1 and new2, and all the digits of num must be used.

Return the minimum possible sum of new1 and new2.


Example 1:

Input: num = 2932
Output: 52
Explanation: Some possible pairs (new1, new2) are (29, 32), (23, 92), and (223, 9).
The minimum sum is 23 + 29 = 52.

Example 2:

Input: num = 4009
Output: 13
Explanation: Some possible pairs (new1, new2) are (0, 409), (4, 900), and (40, 90).
The minimum sum is 4 + 9 = 13. One way of achieving this sum is new1 = 04 and new2 = 009, which evaluates to 4 + 9 = 13.


Constraints:

    1000 <= num <= 9999
"""


class Solution:
    def minimumSum(self, num: int) -> int:
        nums = list(str(num))
        nums.sort()
        a = nums[0] + nums[2]
        b = nums[1] + nums[3]
        return int(a) + int(b)


sol = Solution()

print(sol.minimumSum(2932))  # 52

assert sol.minimumSum(2932) == 52
assert sol.minimumSum(4009) == 13
assert sol.minimumSum(1000) == 1
assert sol.minimumSum(9999) == 198
assert sol.minimumSum(1111) == 22
assert sol.minimumSum(1010) == 2
assert sol.minimumSum(5000) == 5
assert sol.minimumSum(9000) == 9
assert sol.minimumSum(1234) == 37
assert sol.minimumSum(2999) == 128
assert sol.minimumSum(1001) == 2
assert sol.minimumSum(2000) == 2
assert sol.minimumSum(1023) == 15
assert sol.minimumSum(9998) == 188
assert sol.minimumSum(1002) == 3
