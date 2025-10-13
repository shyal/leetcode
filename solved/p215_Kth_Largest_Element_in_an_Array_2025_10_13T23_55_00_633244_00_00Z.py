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

---

I was able to solve this quickly. I still find it unintiuitive for some reason
that i can use a minheap to track the k largest elements.

[1]


[1]
 /
[2]
n: 3 is larger than the top of the heap (1) so popping 1, and pushing 3


[2]
 /
[3]
n: 4 is larger than the top of the heap (2) so popping 2, and pushing 4


[3]
 /
[4]
n: 5 is larger than the top of the heap (3) so popping 3, and pushing 5


[4]
 /
[5]
n: 6 is larger than the top of the heap (4) so popping 4, and pushing 6


[5]
 /
[6]
5

Printing out what's happening does help a bit. The min propery of the heap is useful
because we can efficiently pop the min element. We're efficiently clearing the smallest
elements, so all that's left are the largest elements.

"""

from rich import print


class Solution:
    def findKthLargest(self, nums: List[int], k: int) -> int:
        heap = []
        verbose = False
        for n in nums:
            if len(heap) < k:
                heappush(heap, n)
                # draw_heap(heap)
                continue
            else:
                if n > heap[0]:
                    # print(
                    #     f"n: {n} is larger than the top of the heap ({heap[0]}) ",
                    #     end="",
                    # )
                    pop = heappop(heap)
                    # print(f"so popping {pop}, and pushing {n}")
                    heappush(heap, n)
                    # draw_heap(heap)
        return heap[0]


sol = Solution()

res = sol.findKthLargest([1, 2, 3, 4, 5, 6], 2)
# print(res)


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
