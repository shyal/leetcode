"""
URL: https://leetcode.com/problems/sliding-window-maximum/description/?envType=problem-list-v2&envId=vn57k9wr

239. Sliding Window Maximum

You are given an array of integers nums, there is a sliding window of size k
which is moving from the very left of the array to the very right. You can
only see the k numbers in the window. Each time the sliding window moves
right by one position.

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

Had a pretty good intuition on how to solve this problem. I immediately thought
of the brute force solution (obviously). Then thought of the heap. I was a little
unsure how to "evict" items from the heap that were no longer in the window,
and i did get hinted that they can get evicted lazily.

"""


class Solution:
    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        if k == 1:
            return nums
        h = [(-v, i) for i, v in enumerate(nums[:k])]
        heapify(h)
        res = [-h[0][0]]
        for i, v in enumerate(nums[k:], start=k):
            heappush(h, (-v, i))
            while True:
                _max = h[0]
                if _max[1] <= i -k:
                    heappop(h)
                else:
                    break
            res.append(-_max[0])
        return res



sol = Solution()


assert sol.maxSlidingWindow([1, 3, -1, -3, 5, 3, 6, 7], 3) == [3, 3, 5, 5, 6, 7]
assert sol.maxSlidingWindow([1], 1) == [1]
assert sol.maxSlidingWindow([-10000], 1) == [-10000]
assert sol.maxSlidingWindow([5, 3, 8], 1) == [5, 3, 8]
assert sol.maxSlidingWindow([4, 2, 1, 5], 4) == [5]
assert sol.maxSlidingWindow([1, 2, 3, 4], 2) == [2, 3, 4]
assert sol.maxSlidingWindow([9, 7, 5, 3], 2) == [9, 7, 5]
assert sol.maxSlidingWindow([9, 7, 5, 3], 3) == [9, 7]
assert sol.maxSlidingWindow([2, 2, 2, 2], 2) == [2, 2, 2]
assert sol.maxSlidingWindow([4, 3, 2, 1, 5], 2) == [4, 3, 2, 5]
assert sol.maxSlidingWindow([-1, -3, -5, -2], 3) == [-1, -2]
assert sol.maxSlidingWindow([1, 3, 1, 2, 0, 5], 3) == [3, 3, 2, 5]
assert sol.maxSlidingWindow([7, 2, 4], 2) == [7, 4]
assert sol.maxSlidingWindow([-7, -8, 7, 5, 7, 1, 6, 0], 4) == [7, 7, 7, 7, 7]
assert sol.maxSlidingWindow([10000, -10000, 10000], 2) == [10000, 10000]
assert sol.maxSlidingWindow([1, -1], 1) == [1, -1]