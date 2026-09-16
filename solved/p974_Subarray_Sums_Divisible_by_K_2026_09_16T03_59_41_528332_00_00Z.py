"""
URL: https://leetcode.com/problems/subarray-sums-divisible-by-k/description/?envType=problem-list-v2&envId=vn57k9wr

974. Subarray Sums Divisible by K

Given an integer array nums and an integer k, return the number of non-empty subarrays that have a sum divisible by k.

A subarray is a contiguous part of an array.

Example 1:

Input: nums = [4,5,0,-2,-3,1], k = 5
Output: 7
Explanation: There are 7 subarrays with a sum divisible by k = 5:
[4, 5, 0, -2, -3, 1], [5], [5, 0], [5, 0, -2, -3], [0], [0, -2, -3], [-2, -3]

Example 2:

Input: nums = [5], k = 9
Output: 0

Constraints:

    1 <= nums.length <= 3 * 10^4
    -10^4 <= nums[i] <= 10^4
    2 <= k <= 10^4

---

Another super awesome DP problem. Solving as brute force. TLE.

LEETCODE: Time Limit Exceeded (66/76 cases)
"""


class Solution:

    def subarraysDivByK(self, nums: List[int], k: int) -> int:
        acc = [*accumulate(nums)]
        range_sum = lambda a, b: acc[b] - (acc[a - 1] if a > 0 else 0)
        count = 0
        for i in range(len(nums)):
            for j in range(i, len(nums)):
                divisible = range_sum(i, j) % k == 0
                if divisible:
                    count += 1
        return count


sol = Solution()

# print(sol.subarraysDivByK([4, 5, 0, -2, -3, 1], 5))  # 7

assert sol.subarraysDivByK([4, 5, 0, -2, -3, 1], 5) == 7
assert sol.subarraysDivByK([5], 9) == 0

assert sol.subarraysDivByK([0], 2) == 1
assert sol.subarraysDivByK([1, 2, 3, 4, 5], 1) == 15
assert sol.subarraysDivByK([-1, -2, -3, -4, -5], 3) == 7
# assert sol.subarraysDivByK([10**4] * 30000, 10**4) == 450015000
# assert sol.subarraysDivByK([1] * 30000, 2) == 225000000
# assert sol.subarraysDivByK([1, -1] * 15000, 2) == 225000000
assert sol.subarraysDivByK([2, 2, 2, 2], 2) == 10
assert sol.subarraysDivByK([7, 7, 7, 7], 7) == 10
assert sol.subarraysDivByK([3, 1, 4, 1, 5, 9, 2, 6, 5], 10) == 2
assert sol.subarraysDivByK([0, 0, 0, 0], 3) == 10
assert sol.subarraysDivByK([-(10**4), 10**4, -(10**4), 10**4], 5) == 10
assert sol.subarraysDivByK([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 11) == 5
