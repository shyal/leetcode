"""
DRILL: Largest Of The Last K

Given an integer array nums and an integer k, return an array res of the
same length where res[i] is the largest of nums[i] and the k - 1 values
before it. While fewer than k values have been seen, use all of them.
Keep the candidates in a monotonic queue.

Example 1:

Input: nums = [1, 3, -1, -3, 5, 3, 6, 7], k = 3
Output: [1, 3, 3, 3, 5, 5, 6, 7]
Explanation: res[3] is the largest of 3, -1, -3. res[4] is the largest
of -1, -3, 5.

Example 2:

Input: nums = [4, 4, 2, 2], k = 2
Output: [4, 4, 4, 2]
Explanation: res[2] is the largest of 4, 2. The first 4 is out of reach.

Constraints:

    1 <= k <= len(nums) <= 10^5
    -10^4 <= nums[i] <= 10^4

    REQUIRED: one pass, O(n) total. Each value enters the queue once and
    leaves at most once. NO max() over a slice, NO heap.
"""

from dsa.monotonic_queue import MonotonicQueue, Type


class Solution:
    def largestOfLastK(self, nums: list[int], k: int) -> list[int]:
        q = MonotonicQueue(Type.decreasing)
        res = []
        for i, v in enumerate(nums):
            q.push((v, i))
            if q.front()[1] <= i - k:
                q.popleft()
            res.append(q.front()[0])
        return res


sol = Solution()

print(sol.largestOfLastK([1, 3, -1, -3, 5, 3, 6, 7], 3))  # [1, 3, 3, 3, 5, 5, 6, 7]

assert sol.largestOfLastK([1, 3, -1, -3, 5, 3, 6, 7], 3) == [1, 3, 3, 3, 5, 5, 6, 7]
assert sol.largestOfLastK([4, 4, 2, 2], 2) == [4, 4, 4, 2]
assert sol.largestOfLastK([5], 1) == [5]
assert sol.largestOfLastK([5, 4, 3, 2, 1], 1) == [5, 4, 3, 2, 1]
assert sol.largestOfLastK([5, 4, 3, 2, 1], 2) == [5, 5, 4, 3, 2]
assert sol.largestOfLastK([1, 2, 3, 4, 5], 3) == [1, 2, 3, 4, 5]
assert sol.largestOfLastK([2, 2, 2, 2], 3) == [2, 2, 2, 2]
assert sol.largestOfLastK([9, 1, 1, 1, 1], 3) == [9, 9, 9, 1, 1]
assert sol.largestOfLastK([1, 3, 1, 2, 0, 5], 3) == [1, 3, 3, 3, 2, 5]
assert sol.largestOfLastK([-1, -3, -5, -7], 2) == [-1, -1, -3, -5]
assert sol.largestOfLastK([1, 2, 3, 4, 5], 5) == [1, 2, 3, 4, 5]
