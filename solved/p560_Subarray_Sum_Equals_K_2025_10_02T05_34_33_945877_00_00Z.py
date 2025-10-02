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

---

I completely blanked on prefix sum, which is unacceptable. I really feel i need to go to town
on prefix sum type problems, slowly ramping up complexity, else i'll keep forgetting it.

"""


class Solution:
    def subarraySum(self, nums: List[int], k: int) -> int:
        # had to look up solution
        res = 0
        prefix = 0
        D = defaultdict(int)
        D[0] = 1
        for n in nums:
            prefix += n
            if prefix - k in D:
                res += D[prefix - k]
            D[prefix] += 1
        return res


sol = Solution()
assert sol.subarraySum([1, 2, 3], k=2) == 1
assert sol.subarraySum([1, 2, 3], k=3) == 2
