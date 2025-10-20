"""
URL: https://leetcode.com/problems/subarray-sum-equals-k/description/

560. Subarray Sum Equals K

Given an array of integers nums and an integer k, return the total number of subarrays whose sum equals to k.

A subarray is a contiguous non-empty sequence of elements within an array.


Example 1:
Input: nums = [1,1,1], k = 2
Output: 2
Example 2:
Input: nums = [1,2,3], k = 3
Output: 2


Constraints:

    1 <= nums.length <= 2 * 104
    -1000 <= nums[i] <= 1000
    -107 <= k <= 107
"""


class Solution:
    def subarraySum(self, nums: List[int], k: int) -> int:
        prefix = 0
        D = defaultdict(int)
        D[0] = 1
        res = 0
        for n in nums:
            prefix += n
            c = prefix - k
            if c in D:
                res += D[c]
            D[prefix] += 1
        return res


sol = Solution()
assert sol.subarraySum([1, 2, 3], k=2) == 1
assert sol.subarraySum([1, 2, 3], k=3) == 2
