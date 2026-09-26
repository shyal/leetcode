"""
URL: https://leetcode.com/problems/longest-consecutive-sequence/description/?envType=problem-list-v2&envId=vn57k9wr

128. Longest Consecutive Sequence

Given an unsorted array of integers nums, return the length of the longest consecutive elements sequence.

You must write an algorithm that runs in O(n) time.

Example 1:

Input: nums = [100,4,200,1,3,2]
Output: 4
Explanation: The longest consecutive elements sequence is [1, 2, 3, 4]. Therefore its length is 4.

Example 2:

Input: nums = [0,3,7,2,5,8,4,6,0,1]
Output: 9

Example 3:

Input: nums = [1,0,1,2]
Output: 3

Constraints:

    0 <= nums.length <= 10^5
    -10^9 <= nums[i] <= 10^9
"""


# mu 0.4
# def longestConsecutive(nums: [int]) -> int
#   numss = set(nums)
#   res = 0
#   curr = inf
#   for i, v in nums
#     if v > curr
#       continue
#     curr = v
#     c = 0
#     while v in numss
#       c += 1
#       res = max(res, c)
#       v += 1
#   res

from math import inf


class Solution:
    def longestConsecutive(self, nums: list[int]) -> int:
        numss = set(nums)
        res = 0
        curr = inf
        for i, v in enumerate(nums):
            if v > curr:
                continue
            curr = v
            c = 0
            while v in numss:
                c += 1
                res = max(res, c)
                v += 1
        return res


sol = Solution()
print(sol.longestConsecutive([100, 4, 200, 1, 3, 2]))
assert sol.longestConsecutive([100, 4, 200, 1, 3, 2]) == 4
assert sol.longestConsecutive([0, 3, 7, 2, 5, 8, 4, 6, 0, 1]) == 9
assert sol.longestConsecutive([1, 0, 1, 2]) == 3
assert sol.longestConsecutive([]) == 0
assert sol.longestConsecutive([1]) == 1
assert sol.longestConsecutive([2, 2, 2, 2]) == 1
assert sol.longestConsecutive([-1, -2, -3, -4]) == 4
assert sol.longestConsecutive([10 ** 9, 10 ** 9 - 1, 10 ** 9 - 2]) == 3
assert sol.longestConsecutive([-10 ** 9, -10 ** 9 + 1, -10 ** 9 + 2]) == 3
assert sol.longestConsecutive(list(range(0, 100000))) == 100000
assert sol.longestConsecutive(list(range(0, 100000, 2))) == 1
assert sol.longestConsecutive([5, 4, 3, 2, 1]) == 5
assert sol.longestConsecutive([1, 3, 5, 7, 9, 11]) == 1
assert sol.longestConsecutive([1, 2, 2, 3, 4, 4, 5]) == 5
assert sol.longestConsecutive([0]) == 1
