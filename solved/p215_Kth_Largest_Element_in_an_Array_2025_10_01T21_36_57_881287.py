"""
URL: https://leetcode.com/problems/kth-largest-element-in-an-array/description/?envType=study-plan-v2&envId=leetcode-75

215. Kth Largest Element in an Array

Given an integer array nums and an integer k, return the kth largest element in the array.

Note that it is the kth largest element in the sorted order, not the kth distinct element.

Can you solve it without sorting?


Example 1:
Input: nums = [3,2,1,5,6,4], k = 2
Output: 5
Example 2:
Input: nums = [3,2,3,1,2,4,5,5,6], k = 4
Output: 4


Constraints:

        1 <= k <= nums.length <= 105
        -104 <= nums[i] <= 104
"""


class Solution:
    def findKthLargest(self, nums: List[int], k: int) -> int:
        heap = []
        for n in nums:
            heappush(heap, n)
            draw_heap(heap)
            if len(heap) > k:
                heappop(heap)
        return heap[0]


sol = Solution()
assert sol.findKthLargest([1], 1) == 1
assert sol.findKthLargest([3, 2, 1], 1) == 3
assert sol.findKthLargest([1, 2, 3], 3) == 1
assert sol.findKthLargest([1, 2, 3, 4, 5, 6], 2) == 5
assert sol.findKthLargest([1, 3, 3, 2], 2) == 3
assert sol.findKthLargest([-3, -1, 0, 2], 2) == 0
assert sol.findKthLargest([1, 4, 2, 3], 3) == 2
assert sol.findKthLargest([1, 5, 3], 3) == 1
assert sol.findKthLargest([1, 100, 2, 50], 3) == 2
assert sol.findKthLargest([-5, 10, -3, 2], 3) == -3
assert sol.findKthLargest([0, -10, 5, -1], 2) == 0
assert sol.findKthLargest([8, 7, 6, 5, 4, 3], 4) == 5
assert sol.findKthLargest([5, 5, 5, 5], 2) == 5
assert sol.findKthLargest([6, 5, 4, 3, 2, 1], 3) == 4
assert sol.findKthLargest([1, 2, 3, 4, 5, 6], 3) == 4
assert sol.findKthLargest([-1, -2, 3, 0], 2) == 0
assert sol.findKthLargest([2, 2, 1, 2, 3], 3) == 2
assert sol.findKthLargest([-1, -2, -3, -4], 2) == -2
assert sol.findKthLargest([10, 20, 30, 40, 50, -10, 0], 4) == 20
assert sol.findKthLargest([99, 1, 2, 3, 4], 1) == 99
assert sol.findKthLargest([5, 2, 4, 1, 3, 6, 0], 4) == 3
