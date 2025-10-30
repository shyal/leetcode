"""
URL: https://leetcode.com/problems/find-the-sum-of-encrypted-integers/description/?envType=problem-list-v2&envId=vn57k9wr

3079. Find the Sum of Encrypted Integers

You are given an integer array nums containing positive integers. We define a function encrypt such that encrypt(x) replaces every digit in x with the largest digit in x. For example, encrypt(523) = 555 and encrypt(213) = 333.

Return the sum of encrypted elements.

Example 1:

Input: nums = [1,2,3]
Output: 6
Explanation: The encrypted elements are [1,2,3]. The sum of encrypted elements is 1 + 2 + 3 == 6.

Example 2:

Input: nums = [10,21,31]
Output: 66
Explanation: The encrypted elements are [11,22,33]. The sum of encrypted elements is 11 + 22 + 33 == 66.

Constraints:

    1 <= nums.length <= 50
    1 <= nums[i] <= 1000
"""


class Solution:
    def getDigits(self, num):
        digits = []
        while num:
            digits.append(num % 10)
            num //= 10
        return digits

    def encrypt(self, digits):
        _max = max(digits)
        digits = [_max] * len(digits)
        res = 0
        for d in digits:
            res = res * 10 + d
        return res

    def sumOfEncryptedInt(self, nums: List[int]) -> int:
        res = 0
        for n in nums:
            res += self.encrypt(self.getDigits(n))
        return res


sol = Solution()

assert sol.sumOfEncryptedInt([1, 2, 3]) == 6
assert sol.sumOfEncryptedInt([10, 21, 31]) == 66
assert sol.sumOfEncryptedInt([1]) == 1
assert sol.sumOfEncryptedInt([100]) == 111
assert sol.sumOfEncryptedInt([1000]) == 1111
assert sol.sumOfEncryptedInt([999]) == 999
assert sol.sumOfEncryptedInt([10]) == 11
assert sol.sumOfEncryptedInt([523]) == 555
assert sol.sumOfEncryptedInt([213]) == 333
assert sol.sumOfEncryptedInt([1, 1000, 999]) == 2111
assert sol.sumOfEncryptedInt([901]) == 999
assert sol.sumOfEncryptedInt([20, 90, 9]) == 22 + 99 + 9
