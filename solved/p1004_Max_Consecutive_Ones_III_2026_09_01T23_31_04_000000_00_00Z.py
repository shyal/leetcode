"""
URL: https://leetcode.com/problems/max-consecutive-ones-iii/description/?envType=problem-list-v2&envId=vn57k9wr

1004. Max Consecutive Ones III

Given a binary array nums and an integer k, return the maximum number of consecutive 1's in the array if you can flip at most k 0's.

Example 1:

Input: nums = [1,1,1,0,0,0,1,1,1,1,0], k = 2
Output: 6
Explanation: [1,1,1,0,0,1,1,1,1,1,1]
Bolded numbers were flipped from 0 to 1. The longest subarray is underlined.

Example 2:

Input: nums = [0,0,1,1,0,0,1,1,1,0,1,1,0,0,0,1,1,1,1], k = 3
Output: 10
Explanation: [0,0,1,1,1,1,1,1,1,1,1,1,0,0,0,1,1,1,1]
Bolded numbers were flipped from 0 to 1. The longest subarray is underlined.

Constraints:

    1 <= nums.length <= 10^5
    nums[i] is either 0 or 1.
    0 <= k <= nums.length
"""


class Solution:
    def longestOnes(self, nums: List[int], k: int) -> int:
        best = 0
        zeros = 0
        left = 0
        for right, n in enumerate(nums):
            if nums[right] == 0:
                zeros += 1
            if zeros > k:
                if nums[left] == 0:
                    zeros -= 1
                left += 1
            best = max(best, right - left + 1)
        return best


sol = Solution()

print(sol.longestOnes([1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0], 2))  # 6

assert sol.longestOnes([1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0], 2) == 6
assert (
    sol.longestOnes([0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1], 3) == 10
)

assert sol.longestOnes([], 0) == 0
assert sol.longestOnes([0], 0) == 0
assert sol.longestOnes([1], 0) == 1
assert sol.longestOnes([0], 1) == 1
assert sol.longestOnes([1], 1) == 1
assert sol.longestOnes([0, 0, 0, 0, 0], 0) == 0
assert sol.longestOnes([0, 0, 0, 0, 0], 5) == 5
assert sol.longestOnes([1, 1, 1, 1, 1], 0) == 5
assert sol.longestOnes([1, 1, 1, 1, 1], 5) == 5
assert sol.longestOnes([0, 1, 0, 1, 0, 1, 0, 1], 2) == 5
assert sol.longestOnes([0, 1, 0, 1, 0, 1, 0, 1], 4) == 8
assert sol.longestOnes([1] * 100000, 0) == 100000
