"""
URL: https://leetcode.com/problems/split-array-largest-sum/description/?envType=problem-list-v2&envId=vn57k9wr

410. Split Array Largest Sum

Given an integer array nums and an integer k, split nums into k non-empty subarrays such that the largest sum of any subarray is minimized.

Return the minimized largest sum of the split.

A subarray is a contiguous part of the array.


Example 1:

Input: nums = [7,2,5,10,8], k = 2
Output: 18
Explanation: There are four ways to split nums into two subarrays.
The best way is to split it into [7,2,5] and [10,8], where the largest sum among the two subarrays is only 18.

Example 2:

Input: nums = [1,2,3,4,5], k = 2
Output: 9
Explanation: There are four ways to split nums into two subarrays.
The best way is to split it into [1,2,3] and [4,5], where the largest sum among the two subarrays is only 9.


Constraints:

    1 <= nums.length <= 1000
    0 <= nums[i] <= 10^6
    1 <= k <= min(50, nums.length)

---

OK i had to look at solutions, and consult Grok to piece this together. I like this solution a lot,
but will need to revisit this problem at a later date, and solve it myself.

"""


class Solution:

    def count_smaller_subarrays(self, nums, max_sum, m):
        cuts, prefix = 0, 0
        for x in nums:
            if x > max_sum:
                return False
            prefix += x
            if prefix > max_sum:
                cuts += 1
                prefix = x
        return cuts + 1

    def can_split(self, nums, max_sum, m):
        return self.count_smaller_subarrays(nums, max_sum, m) <= m

    # @viz_binary_search()
    def splitArray(self, nums: List[int], k: int) -> int:
        low = max(nums)
        high = sum(nums)
        result = -1
        is_minimization = True

        while low <= high:
            mid = low + (high - low) // 2
            if self.can_split(nums, mid, k):
                result = mid
                if is_minimization:
                    high = mid - 1
                else:
                    low = mid + 1
            else:
                if is_minimization:
                    low = mid + 1
                else:
                    high = mid - 1

        return result


sol = Solution()

assert sol.splitArray([7, 2, 5, 10, 8], 2) == 18
assert sol.splitArray([1, 2, 3, 4, 5], 2) == 9
assert sol.splitArray([1, 2, 3, 4, 5], 1) == 15
assert sol.splitArray([1, 2, 3, 4, 5], 3) == 6
assert sol.splitArray([1, 2, 3, 4, 5], 5) == 5
assert sol.splitArray([0], 1) == 0
assert sol.splitArray([1, 1000000], 2) == 1000000
assert sol.splitArray([1, 2, 1000000, 3], 2) == 1000003
assert sol.splitArray([1, 2, 1000000, 3], 3) == 1000000
assert sol.splitArray([7, 2, 5, 10, 8], 1) == 32
assert sol.splitArray([7, 2, 5, 10, 8], 5) == 10
assert sol.splitArray([0, 0, 0], 2) == 0
assert sol.splitArray([1000000, 1000000], 1) == 2000000
assert sol.splitArray([1000000, 1000000], 2) == 1000000
