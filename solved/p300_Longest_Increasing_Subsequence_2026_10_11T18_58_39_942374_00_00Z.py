"""
URL: https://leetcode.com/problems/longest-increasing-subsequence/description/?envType=problem-list-v2&envId=vn57k9wr

300. Longest Increasing Subsequence

Given an integer array nums, return the length of the longest strictly increasing subsequence.

Example 1:

Input: nums = [10,9,2,5,3,7,101,18]
Output: 4
Explanation: The longest increasing subsequence is [2,3,7,101], therefore the length is 4.

Example 2:

Input: nums = [0,1,0,3,2,3]
Output: 4

Example 3:

Input: nums = [7,7,7,7,7,7,7]
Output: 1

Constraints:

    1 <= nums.length <= 2500
    -10^4 <= nums[i] <= 10^4

Follow up: Can you come up with an algorithm that runs in O(n log(n)) time complexity?
---
i keep forgetting this solve, and the reason is, i keep counting how many items are smaller
than j instead of asking the right question.
the right question is a recurrence: for this previous smaller item, do i use its dp[i] + 1
(since it's smaller, we're entitled to say +1) or stick to my current best dp[j]

learning

LEETCODE: Accepted (2220 ms, 19.6 MB)
"""


# mu 0.9
# class Solution
#   def lengthOfLIS(nums: [int]) -> int
#     dp = table(len(nums), fill=1)
#     for i, j in pairs(len(nums), back=True)
#       if nums[i] < nums[j]
#         dp[j] = max(dp[i] + 1, dp[j])
#     max(dp, default=0)

def table(*dims, fill=0):
    if len(dims) == 1:
        return [fill] * dims[0]
    if len(dims) == 2:
        return [[fill] * dims[1] for _ in range(dims[0])]
    return [table(*dims[1:], fill=fill) for _ in range(dims[0])]


def pairs(n, type=tuple, back=False):
    if back:
        for j in range(n):
            for i in range(j):
                yield type((i, j))
        return
    for i in range(n):
        for j in range(i + 1, n):
            yield type((i, j))


class Solution:
    def lengthOfLIS(self, nums: list[int]) -> int:
        dp = table(len(nums), fill=1)
        for i, j in pairs(len(nums), back=True):
            if nums[i] < nums[j]:
                dp[j] = max(dp[i] + 1, dp[j])
        return max(dp, default=0)


sol = Solution()
print(sol.lengthOfLIS([10, 9, 2, 5, 3, 7, 101, 18]))
_l, _r = sol.lengthOfLIS([10, 9, 2, 5, 3, 7, 101, 18]), 4
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.lengthOfLIS([0, 1, 0, 3, 2, 3]), 4
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.lengthOfLIS([7, 7, 7, 7, 7, 7, 7]), 1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.lengthOfLIS([]), 0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.lengthOfLIS([1]), 1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.lengthOfLIS([2, 2, 2, 2, 2]), 1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.lengthOfLIS([-1, -2, -3, -4]), 1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.lengthOfLIS([-1, 0, 1, 2, 3]), 5
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.lengthOfLIS([1, 3, 5, 4, 7]), 4
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.lengthOfLIS([10 ** 4] * 2500), 1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.lengthOfLIS(list(range(0, 2500))), 2500
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.lengthOfLIS(list(range(2500, 0, -1))), 1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.lengthOfLIS([1, 2, 2, 3, 4, 4, 5]), 5
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.lengthOfLIS([10000, -10000] * 1250), 2
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.lengthOfLIS([3, 1, 2]), 2
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
