"""
URL: https://leetcode.com/problems/trapping-rain-water/description/?envType=problem-list-v2&envId=vn57k9wr

42. Trapping Rain Water

Given n non-negative integers representing an elevation map where the width of each bar is 1, compute how much water it can trap after raining.

Example 1:

Input: height = [0,1,0,2,1,0,1,3,2,1,2,1]
Output: 6
Explanation: The above elevation map (black section) is represented by array [0,1,0,2,1,0,1,3,2,1,2,1]. In this case, 6 units of rain water (blue section) are being trapped.

Example 2:

Input: height = [4,2,0,3,2,5]
Output: 9

Constraints:

    n == height.length
    1 <= n <= 2 * 10^4
    0 <= height[i] <= 10^5
---
_
         _              _      _
   _        _     _        _     _
_     _        _        
0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1

compute the max from the left and store it
compute the max from the right and store it
make the min of both and store it
accumulate the diff between that and the height

LEETCODE: Accepted (19 ms, 21.3 MB)
"""


# mu 0.6
# def trap(height: [int]) -> int
#   left_max = list scan(max, height)
#   right_max = list(scan(max, height[::-1]))[::-1]
#   min_of = [min(l, r) for (l, r) in zip(left_max, right_max)]
#   sum for i in range(len(height)): min_of[i] - height[i]

from itertools import accumulate


class Solution:
    def trap(self, height: list[int]) -> int:
        left_max = list(accumulate(height, max))
        right_max = list(accumulate(height[::-1], max))[::-1]
        min_of = [min(l, r) for (l, r) in zip(left_max, right_max)]
        return sum(min_of[i] - height[i] for i in range(len(height)))


sol = Solution()
print(sol.trap([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]))
assert sol.trap([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]) == 6
assert sol.trap([4, 2, 0, 3, 2, 5]) == 9
assert sol.trap([]) == 0
assert sol.trap([0]) == 0
assert sol.trap([1]) == 0
assert sol.trap([2, 2, 2, 2]) == 0
assert sol.trap([5, 4, 3, 2, 1]) == 0
assert sol.trap([1, 2, 3, 4, 5]) == 0
assert sol.trap([0, 0, 0, 0, 0]) == 0
assert sol.trap([3, 0, 3, 0, 3]) == 6
assert sol.trap([100000, 0, 100000]) == 100000
assert sol.trap([0, 100000, 0, 100000, 0]) == 100000
assert sol.trap([0] * 20000) == 0
assert sol.trap([1] * 10000 + [0] * 10000) == 0
