"""
URL: https://leetcode.com/problems/subarray-sums-divisible-by-k/description/

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

    1 <= nums.length <= 3 * 104
    -104 <= nums[i] <= 104
    2 <= k <= 104

---

This feels like magic to me. I barely remembered the subarray sum == k solution,
which i get when i step through it but still feels a touch like magic (starting to get it
but keep forgetting).

This solution however i had to look up, and feels entirely magical.

"""


class Solution:
    def subarraysDivByK(self, nums: List[int], k: int) -> int:
        D = defaultdict(int)
        D[0] = 1
        prefix_mod = 0
        res = 0
        for n in nums:
            prefix_mod = (prefix_mod + n) % k
            res += D[prefix_mod]
            D[prefix_mod] += 1
        return res


sol = Solution()
assert sol.subarraysDivByK([4, 5, 0, -2, -3, 1], 5) == 7
assert sol.subarraysDivByK([5], 9) == 0
