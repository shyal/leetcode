"""
URL: https://leetcode.com/problems/longest-subarray-of-1s-after-deleting-one-element/description/?envType=study-plan-v2&envId=leetcode-75

1493. Longest Subarray of 1's After Deleting One Element

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
"""

from itertools import groupby


class Solution:
    def longestSubarray(self, nums: List[int]) -> int:
        counts = ((v, len([*it])) for v, it in groupby(nums))
        a, b, _max, zeroes = None, None, 0, False
        for num, count in counts:
            if num == 0:
                zeroes = True
            if num == 1 and a is None:
                a = count
                _max = max(_max, a)
            elif num == 0 and count > 1:
                a = None
            elif num == 1 and a is not None:
                _max = max(_max, a + count)
                a, b = count, None
        return _max - int(not zeroes)


sol = Solution()

assert sol.longestSubarray(nums=[1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1]) == 11

assert sol.longestSubarray(nums=[1, 1, 1]) == 2
assert sol.longestSubarray(nums=[0, 1, 1, 1, 0, 0, 1, 1, 0, 1]) == 3
assert sol.longestSubarray(nums=[0, 1, 1, 1, 0, 1, 1, 0, 1]) == 5
assert sol.longestSubarray(nums=[1, 1, 1, 0, 1, 1, 1]) == 6
assert sol.longestSubarray(nums=[1, 1, 1, 0, 0, 1, 1, 1]) == 3
assert sol.longestSubarray(nums=[0, 1, 1, 1, 0, 0, 1, 1, 1]) == 3
assert sol.longestSubarray(nums=[0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0]) == 3
assert sol.longestSubarray(nums=[0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0]) == 3
assert (
    sol.longestSubarray(nums=[0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0])
    == 6
)
assert sol.longestSubarray(nums=[1]) == 0
assert sol.longestSubarray(nums=[0]) == 0
assert sol.longestSubarray(nums=[1, 1]) == 1
assert sol.longestSubarray(nums=[0, 0]) == 0
assert sol.longestSubarray(nums=[1, 0, 1]) == 2
assert sol.longestSubarray(nums=[1, 0, 0, 1]) == 1
assert sol.longestSubarray(nums=[0, 1, 0]) == 1
assert sol.longestSubarray(nums=[1, 0, 1, 0, 1]) == 2
assert sol.longestSubarray(nums=[0, 1, 0, 1, 0, 1]) == 2
assert sol.longestSubarray(nums=[1, 0, 1, 0, 1, 0]) == 2
assert sol.longestSubarray(nums=[0, 0, 0, 0, 0]) == 0
assert sol.longestSubarray(nums=[1, 1, 1, 1, 1]) == 4
assert sol.longestSubarray(nums=[1, 1, 0, 0, 0, 1, 1]) == 2
