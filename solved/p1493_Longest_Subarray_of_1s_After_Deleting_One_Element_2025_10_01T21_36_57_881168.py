"""
1493. Longest Subarray of 1's After Deleting One Element
Medium
Given a binary array nums, you should delete one element from it.

Return the size of the longest non-empty subarray containing only 1's in the resulting array. Return 0 if there is no such subarray.

Example 1:

Input: nums = [1,1,0,1]
Output: 3
Explanation: After deleting the number in position 2, [1,1,1] contains 3 numbers with value of 1's.
Example 2:

Input: nums = [0,1,1,1,0,1,1,0,1]
Output: 5
Explanation: After deleting the number in position 4, [0,1,1,1,1,1,0,1] longest subarray with value of 1's is [1,1,1,1,1].
Example 3:

Input: nums = [1,1,1]
Output: 2
Explanation: You must delete one element.
 

Constraints:

1 <= nums.length <= 105
nums[i] is either 0 or 1.

Hint 1
Maintain a sliding window where there is at most one zero in it.
"""


class Solution:  # stub
    def longestSubarray(self, nums: List[int]) -> int:
        # todo
        pass


if False:
    sol = Solution()
    assert sol.longestSubarray(nums=[1, 1, 0, 1]) == 3
    assert sol.longestSubarray(nums=[0, 1, 1, 1, 0, 1, 1, 0, 1]) == 5
    assert sol.longestSubarray(nums=[1, 1, 1]) == 2
    assert sol.longestSubarray(nums=[1]) == 0
    assert sol.longestSubarray(nums=[1, 1, 1, 1, 0]) == 4
    assert sol.longestSubarray(nums=[1, 1, 0, 1, 1]) == 4
    assert sol.longestSubarray(nums=[1, 1, 0, 0, 1, 1]) == 2

