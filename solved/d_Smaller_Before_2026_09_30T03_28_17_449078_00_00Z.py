"""
DRILL: Smaller Before
TRAINS: dp-1d-rolling

Given an integer array nums, return an array dp of the same length where
dp[i] is how many values at an index below i are strictly smaller than
nums[i].

Example 1:

Input: nums = [4, 1, 6, 2, 8, 5, 9]
Output: [0, 0, 2, 1, 4, 3, 6]
Explanation: before the 5 at index 5 sit 4, 1, 6, 2, 8, and three of
them are smaller than 5.

Example 2:

Input: nums = [5, 4, 3, 2, 1]
Output: [0, 0, 0, 0, 0]

Example 3:

Input: nums = [2, 2, 3, 3]
Output: [0, 0, 2, 2]
Explanation: equal values do not count.

Constraints:

    1 <= len(nums) <= 2500
    -10^4 <= nums[i] <= 10^4

    REQUIRED: O(n^2), every earlier index compared against i. NO sorting.
    The test is strictly smaller: counting an equal value is the fail.
"""


# mu 0.7
# def numPrevSmaller(nums: [int]) -> [int]
#   ret res = table(len(nums))
#   for (j, i) in pairs(len(nums), back=True)
#     if nums[j] < nums[i]
#       res[i] = max(res[j], res[i] + 1)
#   res

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
    def numPrevSmaller(self, nums: list[int]) -> list[int]:
        res = table(len(nums))
        for (j, i) in pairs(len(nums), back=True):
            if nums[j] < nums[i]:
                res[i] = max(res[j], res[i] + 1)
        res
        return res


sol = Solution()
print(sol.numPrevSmaller([4, 1, 6, 2, 8, 5, 9]))
