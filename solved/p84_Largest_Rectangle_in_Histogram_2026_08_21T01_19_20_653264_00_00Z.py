"""
URL: https://leetcode.com/problems/largest-rectangle-in-histogram/description/?envType=problem-list-v2&envId=vn57k9wr

84. Largest Rectangle in Histogram

Given an array of integers heights representing the histogram's bar height where
the width of each bar is 1, return the area of the largest rectangle in the
histogram.


Example 1:

Input: heights = [2,1,5,6,2,3]
Output: 10
Explanation: The above is a histogram where width of each bar is 1.
The largest rectangle is shown in the red area, which has an area = 10 units.

Example 2:

Input: heights = [2,4]
Output: 4


Constraints:

    1 <= heights.length <= 10^5
    0 <= heights[i] <= 10^4

---

Brute force passed, but TLE. Got hinted by claude that this is a monotonic stack problem.

I'll mark it as solved, as it technically passes here, but with the wrong approach .
It should get be rescheduled soon, so i can solve it using an monotonic stack.

"""


class Solution:
    def largestRectangleArea(self, heights: List[int]) -> int:
        _max = 0
        for i, v in enumerate(heights):
            h = heights[i]
            width = 1
            for j in range(i - 1, -1, -1):
                if heights[j] >= heights[i]:
                    width += 1
                    h = min(h, heights[j])
                else:
                    break
            for j in range(i + 1, len(heights)):
                if heights[j] >= heights[i]:
                    width += 1
                    h = min(h, heights[j])
                else:
                    break
            _max = max(_max, h * width)
        return _max


sol = Solution()

print(sol.largestRectangleArea([2, 1, 5, 6, 2, 3]))  # 10

assert sol.largestRectangleArea([2, 1, 5, 6, 2, 3]) == 10
assert sol.largestRectangleArea([2, 4]) == 4

assert sol.largestRectangleArea([5]) == 5
assert sol.largestRectangleArea([0]) == 0
assert sol.largestRectangleArea([10000]) == 10000
assert sol.largestRectangleArea([2, 3]) == 4
assert sol.largestRectangleArea([3, 2]) == 4
assert sol.largestRectangleArea([10000, 10000]) == 20000

assert sol.largestRectangleArea([0, 0, 0]) == 0
assert sol.largestRectangleArea([1, 0, 1]) == 1
assert sol.largestRectangleArea([0, 1, 0, 1, 0]) == 1
assert sol.largestRectangleArea([0, 2, 0]) == 2
assert sol.largestRectangleArea([3, 3, 0, 3, 3]) == 6

assert sol.largestRectangleArea([1, 1, 1, 1]) == 4
assert sol.largestRectangleArea([4, 4, 4, 4]) == 16
assert sol.largestRectangleArea([2, 2, 2, 1, 1, 1]) == 6

assert sol.largestRectangleArea([1, 2, 3, 4, 5]) == 9
assert sol.largestRectangleArea([5, 4, 3, 2, 1]) == 9
assert sol.largestRectangleArea([1, 2, 3, 0]) == 4
assert sol.largestRectangleArea([5, 4, 1, 2]) == 8

assert sol.largestRectangleArea([2, 1, 2]) == 3
assert sol.largestRectangleArea([1, 2, 2, 1]) == 4
assert sol.largestRectangleArea([1, 3, 2, 3, 1]) == 6
assert sol.largestRectangleArea([5, 1, 5, 1, 5]) == 5
assert sol.largestRectangleArea([4, 2, 0, 3, 2, 5]) == 6
assert sol.largestRectangleArea([2, 1, 4, 5, 1, 3, 3]) == 8
assert sol.largestRectangleArea([6, 7, 5, 2, 4, 5, 9, 3]) == 16

assert sol.largestRectangleArea([3] * 100) == 300
assert sol.largestRectangleArea([1] * 1000) == 1000
assert sol.largestRectangleArea(list(range(1, 101))) == 2550
assert sol.largestRectangleArea(list(range(100, 0, -1))) == 2550

heights = [2, 1, 5, 6, 2, 3]
assert sol.largestRectangleArea(heights) == 10
assert heights == [2, 1, 5, 6, 2, 3]
