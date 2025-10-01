"""
URL: https://leetcode.com/problems/container-with-most-water/description/?envType=study-plan-v2&envId=leetcode-75

11. Container With Most Water

You are given an integer array height of length n. There are n vertical lines drawn such that the two endpoints of the ith line are (i, 0) and (i, height[i]).

Find two lines that together with the x-axis form a container, such that the container contains the most water.

Return the maximum amount of water a container can store.

Notice that you may not slant the container.


Example 1:

Input: height = [1,8,6,2,5,4,8,3,7]
Output: 49
Explanation: The above vertical lines are represented by array [1,8,6,2,5,4,8,3,7]. In this case, the max area of water (blue section) the container can contain is 49.

Example 2:

Input: height = [1,1]
Output: 1


Constraints:

        n == height.length
        2 <= n <= 105
        0 <= height[i] <= 104
"""


class Solution:
    def maxArea(self, height: List[int]) -> int:
        L, R = 0, len(height) - 1
        _max = 0
        while L < R:
            h = min(height[L], height[R])
            area = h * (R - L)
            _max = max(_max, area)
            if height[L] < height[R]:
                L += 1
            else:
                R -= 1
        return _max


sol = Solution()

res = sol.maxArea(height=[1, 8, 6, 2, 5, 4, 8, 3, 7])
assert res == 49

res = sol.maxArea(height=[1, 1])
assert res == 1

res = sol.maxArea(height=[1, 8, 6, 2, 5, 4, 8, 3, 7])
assert res == 49

res = sol.maxArea(height=[1, 1])
assert res == 1

res = sol.maxArea(height=[0, 0])
assert res == 0

res = sol.maxArea(height=[0, 1])
assert res == 0

res = sol.maxArea(height=[1, 0])
assert res == 0

res = sol.maxArea(height=[1, 0, 1])
assert res == 2

res = sol.maxArea(height=[4, 3, 2, 1])
assert res == 4

res = sol.maxArea(height=[1, 2, 3, 4])
assert res == 4

res = sol.maxArea(height=[5, 5, 5])
assert res == 10

res = sol.maxArea(height=[1, 100, 1])
assert res == 2

res = sol.maxArea(height=[5, 1, 1, 5])
assert res == 15

res = sol.maxArea(height=[1, 2, 4, 3])
assert res == 4

res = sol.maxArea(height=[2, 3, 10, 5, 7, 8, 9])
assert res == 36

res = sol.maxArea(height=[1, 3, 2, 5, 25, 24, 5])
assert res == 24

res = sol.maxArea(height=[10000, 10000])
assert res == 10000

res = sol.maxArea(height=[4, 0, 3])
assert res == 6
