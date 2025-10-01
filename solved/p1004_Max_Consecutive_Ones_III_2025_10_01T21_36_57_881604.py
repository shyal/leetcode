"""
1004. Max Consecutive Ones III
Medium
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

1 <= nums.length <= 105
nums[i] is either 0 or 1.
0 <= k <= nums.length
"""


class Solution:
    def longestOnes(self, nums: List[int], k: int) -> int:
        one_count = 0
        zeros = 0
        ones = 0
        left = 0
        _max = 0
        for right in range(len(nums)):
            v = nums[right]
            ones += v == 1
            zeros += v == 0
            if zeros > k:
                ones -= nums[left] == 1
                zeros -= nums[left] == 0
                left += 1
            _max = max(_max, ones + zeros)
        return _max


sol = Solution()

assert sol.longestOnes(nums=[1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0], k=2) == 6
assert (
    sol.longestOnes(nums=[0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1], k=3)
    == 10
)
assert sol.longestOnes(nums=[1], k=0) == 1
assert sol.longestOnes(nums=[0], k=0) == 0
assert sol.longestOnes(nums=[0], k=1) == 1
assert sol.longestOnes(nums=[1, 1, 1], k=0) == 3
assert sol.longestOnes(nums=[1, 0, 1], k=1) == 3
assert sol.longestOnes(nums=[1, 0, 1], k=0) == 1
assert sol.longestOnes(nums=[0, 0, 0], k=2) == 2
assert sol.longestOnes(nums=[1, 1, 0, 0, 1, 1], k=1) == 3
assert sol.longestOnes(nums=[0, 1, 0, 1, 0], k=2) == 4
assert sol.longestOnes(nums=[1, 1, 1, 0, 1, 1, 1], k=1) == 7
assert sol.longestOnes(nums=[0] * 5, k=3) == 3
assert sol.longestOnes(nums=[1, 0, 0, 0, 1], k=2) == 3
assert sol.longestOnes(nums=[1, 1, 0, 1, 0, 1, 1], k=2) == 7

