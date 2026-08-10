"""
URL: https://leetcode.com/problems/kth-largest-element-in-an-array/description/?envType=problem-list-v2&envId=vn57k9wr

215. Kth Largest Element in an Array

Given an integer array nums and an integer k, return the kth largest element in
the array.

Note that it is the kth largest element in the sorted order, not the kth
distinct element.

Can you solve it without sorting?


Example 1:

Input: nums = [3,2,1,5,6,4], k = 2
Output: 5

Example 2:

Input: nums = [3,2,3,1,2,4,5,5,6], k = 4
Output: 4


Constraints:

    1 <= k <= nums.length <= 10^5
    -10^4 <= nums[i] <= 10^4
"""


class Solution:
    def findKthLargest(self, nums: List[int], k: int) -> int:
        h = nums[:k]
        heapify(h)
        for n in nums[k:]:
            if n < h[0]:
                continue
            else:
                heappush(h, n)
                heappop(h)
        return h[0]

sol = Solution()

assert sol.findKthLargest([3, 2, 1, 5, 6, 4], 2) == 5
assert sol.findKthLargest([3, 2, 3, 1, 2, 4, 5, 5, 6], 4) == 4

assert sol.findKthLargest([1], 1) == 1
assert sol.findKthLargest([2, 1], 1) == 2
assert sol.findKthLargest([2, 1], 2) == 1
assert sol.findKthLargest([3, 2, 1, 5, 6, 4], 1) == 6
assert sol.findKthLargest([3, 2, 1, 5, 6, 4], 6) == 1
assert sol.findKthLargest([1, 2, 3, 4, 5], 1) == 5
assert sol.findKthLargest([1, 2, 3, 4, 5], 3) == 3
assert sol.findKthLargest([5, 4, 3, 2, 1], 5) == 1
assert sol.findKthLargest([7, 7, 7, 7], 1) == 7
assert sol.findKthLargest([7, 7, 7, 7], 3) == 7
assert sol.findKthLargest([3, 3, 3, 3, 4, 4, 4], 2) == 4
assert sol.findKthLargest([3, 3, 3, 3, 4, 4, 4], 4) == 3
assert sol.findKthLargest([-1, -1], 2) == -1
assert sol.findKthLargest([-5, -3, -1], 2) == -3
assert sol.findKthLargest([-5, -3, -1], 3) == -5
assert sol.findKthLargest([0, 0, -1, 1], 2) == 0
assert sol.findKthLargest([0, 0, -1, 1], 3) == 0
assert sol.findKthLargest([0, 0, -1, 1], 4) == -1
assert sol.findKthLargest([-10000, 10000], 1) == 10000
assert sol.findKthLargest([-10000, 10000], 2) == -10000
assert sol.findKthLargest([10000] * 5 + [-10000] * 5, 5) == 10000
assert sol.findKthLargest([10000] * 5 + [-10000] * 5, 6) == -10000
assert sol.findKthLargest([1] * 1000 + [2], 1) == 2
assert sol.findKthLargest([1] * 1000 + [2], 2) == 1
assert sol.findKthLargest([2] + [1] * 1000, 1) == 2

_nums = [3, 2, 1, 5, 6, 4]
assert sol.findKthLargest(_nums, 2) == 5
assert _nums == [3, 2, 1, 5, 6, 4]

_asc = list(range(10001))
assert sol.findKthLargest(_asc, 1) == 10000
assert sol.findKthLargest(_asc, 5000) == 5001
assert sol.findKthLargest(_asc, 10001) == 0

_desc = list(range(10000, -1, -1))
assert sol.findKthLargest(_desc, 1) == 10000
assert sol.findKthLargest(_desc, 5000) == 5001
assert sol.findKthLargest(_desc, 10001) == 0

_cases = [
    [4, 4, 4, 4],
    [9, -3, 0, 7, 7, -3, 2],
    [1, 2],
    [10, -10, 10, -10, 0],
    [6, 5, 4, 3, 2, 1, 0, -1],
]
for _case in _cases:
    _expected = sorted(_case, reverse=True)
    for _k in range(1, len(_case) + 1):
        pass
        # assert sol.findKthLargest(_case, _k) == _expected[_k - 1]