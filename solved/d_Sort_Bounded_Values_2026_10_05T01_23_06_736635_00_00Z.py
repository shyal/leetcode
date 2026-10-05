"""
DRILL: Sort Bounded Values

Given an integer array nums whose values all lie between 0 and 100
inclusive, return the same values in non-decreasing order.

Example 1:

Input: nums = [1, 3, 6, 9, 9, 3, 5, 9]
Output: [1, 3, 3, 5, 6, 9, 9, 9]
Explanation: the values tallied by value are

    value  1 2 3 4 5 6 7 8 9
    count  1 0 2 0 1 1 0 0 3

and reading that tally left to right, each value repeated count times,
is the output.

Example 2:

Input: nums = [100, 0, 100]
Output: [0, 100, 100]

Constraints:

    1 <= len(nums) <= 10^5
    0 <= nums[i] <= 100

    REQUIRED: O(n + 100) time. NO sort(), NO sorted(), NO heapq, NO
    comparison of one element of nums against another. Reaching for a
    comparison sort when the value domain is tiny is the failure mode
    this drill exists to kill.
"""


# mu 0.7
# def sortBounded(nums: [int]) -> [int]
#   buckets = table(101)
#   for n in nums
#     buckets[n] += 1
#   ret res = []
#   for i, n in buckets
#     if n
#       res.extend([i] * n)

def table(*dims, fill=0):
    if len(dims) == 1:
        return [fill] * dims[0]
    if len(dims) == 2:
        return [[fill] * dims[1] for _ in range(dims[0])]
    return [table(*dims[1:], fill=fill) for _ in range(dims[0])]


class Solution:
    def sortBounded(self, nums: list[int]) -> list[int]:
        buckets = table(101)
        for n in nums:
            buckets[n] += 1
        res = []
        for i, n in enumerate(buckets):
            if n:
                res.extend([i] * n)
        return res


sol = Solution()
print(sol.sortBounded([1, 3, 6, 9, 9, 3, 5, 9]))
assert sol.sortBounded([1, 3, 6, 9, 9, 3, 5, 9]) == [1, 3, 3, 5, 6, 9, 9, 9]
assert sol.sortBounded([100, 0, 100]) == [0, 100, 100]
assert sol.sortBounded([7]) == [7]
assert sol.sortBounded([0, 0, 0]) == [0, 0, 0]
assert sol.sortBounded([5, 4, 3, 2, 1, 0]) == [0, 1, 2, 3, 4, 5]
assert sol.sortBounded([50, 50, 49, 51]) == [49, 50, 50, 51]
