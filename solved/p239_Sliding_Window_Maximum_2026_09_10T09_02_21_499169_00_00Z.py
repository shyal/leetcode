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

---


This problem rings a bell.. as it's likely a review.

At first, it seems fairly trivial: maintain a heap.. until it becomes
clear that a heap won't allow evicting any element.. only the min.

So this is likely a lazy heap eviction problem. Once elements are no
longer in the window, they need to be ignored. But then the question
becomes when can they get evicted?

And this sounds like it could also make use of a deque..

Let's start by populating and depopulating the deque.

class Solution:
    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        q = deque([])
        for right, v in enumerate(nums):
            q.append(v)
            if len(q) > k:
                q.popleft()
            if len(q) == k:
                print(list(q))

This does a good job of showing us the items in the window in question.

[1, 3, -1]
[3, -1, -3]
[-1, -3, 5]
[-3, 5, 3]
[5, 3, 6]
[3, 6, 7]

A bf solution is to simply take the max at each step.



class Solution:
    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        res = []
        q = deque([])
        for right, v in enumerate(nums):
            q.append(v)
            if len(q) > k:
                q.popleft()
            if len(q) == k:
                print(list(q))
                res.append(max(q))
        return res

This works but the time complexity is O(n^2), and would likely TLE on LC.

So this is where the heap comes in.. when an item is added to the deque, we
can add it to the heap. And when an item is popped from the deque, we
should mark it as ignored for lazy eviction.

So the final question remains, when can we actually evict the items from the heap.
The answer is likely to evict them if they're larger than the queue's max item.

Nope but this is still pretty inefficient.. if the heap has a lot of items that
cannot be popped.. we can still land in an O(n^2 scenario).

OK complete failure. But i discovered monotonic queues. Drill created and
problem gated.

Learning.

"""


class Solution:
    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        res = []
        q = deque()
        for right, v in enumerate(nums):
            while q and nums[q[-1]] <= v:
                q.pop()
            q.append(right)
            if q[0] == right - k:
                q.popleft()
            if right >= k - 1:
                res.append(nums[q[0]])
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
