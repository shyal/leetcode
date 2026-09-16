"""
URL: https://leetcode.com/problems/sliding-window-maximum/description/?envType=problem-list-v2&envId=vn57k9wr

239. Sliding Window Maximum

You are given an array of integers nums, there is a sliding window of size k which is moving from the very left of the array to the very right. You can only see the k numbers in the window. Each time the sliding window moves right by one position.

Return the max sliding window.

Example 1:

Input: nums = [1,3,-1,-3,5,3,6,7], k = 3
Output: [3,3,5,5,6,7]
Explanation:
Window position                Max
---------------               -----
[1  3  -1] -3  5  3  6  7       3
 1 [3  -1  -3] 5  3  6  7       3
 1  3 [-1  -3  5] 3  6  7       5
 1  3  -1 [-3  5  3] 6  7       5
 1  3  -1  -3 [5  3  6] 7       6
 1  3  -1  -3  5 [3  6  7]      7

Example 2:

Input: nums = [1], k = 1
Output: [1]

Constraints:

    1 <= nums.length <= 10^5
    -10^4 <= nums[i] <= 10^4
    1 <= k <= nums.length

LEETCODE: Accepted (399 ms, 38.2 MB)
"""

from operator import gt, lt


class MQType:
    decreasing = 0
    increasing = 1


class MonotonicQueue:

    def __init__(self, type: MQType = MQType.increasing):
        self.queue = deque([])
        self.type = type

    def push(self, val):
        op = (lt, gt)[self.type]
        res = []
        while self.queue and op(self.queue[-1][0], val[0]):
            res.append(self.queue.pop())
        self.queue.append(val)
        return res

    def pop(self):
        if self.queue:
            return self.queue.pop()

    def popleft(self):
        if self.queue:
            return self.queue.popleft()

    def peek(self):
        if self.queue:
            return self.queue[-1]

    def front(self):
        if self.queue:
            return self.queue[0]

    def __str__(self):
        return str(self.queue)


class Solution:

    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        res = []
        q = MonotonicQueue(MQType.decreasing)
        for i, v in enumerate(nums):
            q.push((v, i))
            if q.front()[1] <= i - k:
                q.popleft()
            if i >= k - 1:
                res.append(q.front()[0])
        return res


sol = Solution()

print(sol.maxSlidingWindow([1, 3, -1, -3, 5, 3, 6, 7], 3))  # [3,3,5,5,6,7]

assert sol.maxSlidingWindow([1, 3, -1, -3, 5, 3, 6, 7], 3) == [3, 3, 5, 5, 6, 7]
assert sol.maxSlidingWindow([1], 1) == [1]

assert sol.maxSlidingWindow([], 1) == []
assert sol.maxSlidingWindow([5, 5, 5, 5, 5], 3) == [5, 5, 5]
assert sol.maxSlidingWindow([-1, -3, -5, -7, -9], 2) == [-1, -3, -5, -7]
assert sol.maxSlidingWindow([1, 2, 3, 4, 5], 5) == [5]
assert sol.maxSlidingWindow([5, 4, 3, 2, 1], 1) == [5, 4, 3, 2, 1]
assert sol.maxSlidingWindow([1, 3, 1, 2, 0, 5], 3) == [3, 3, 2, 5]
assert sol.maxSlidingWindow([10**4] * 10**5, 10**5) == [10000]
assert sol.maxSlidingWindow(list(range(10**5, 0, -1)), 100000) == [100000]
assert sol.maxSlidingWindow([1, 2, 3, 4, 5], 1) == [1, 2, 3, 4, 5]
assert sol.maxSlidingWindow([1, 1, 1, 1, 1], 5) == [1]
