"""
URL: https://leetcode.com/problems/trapping-rain-water/description/?envType=problem-list-v2&envId=vn57k9wr

42. Trapping Rain Water

Given n non-negative integers representing an elevation map where the width of
each bar is 1, compute how much water it can trap after raining.


Example 1:

Input: height = [0,1,0,2,1,0,1,3,2,1,2,1]
Output: 6
Explanation: The above elevation map (black section) is represented by array
[0,1,0,2,1,0,1,3,2,1,2,1]. In this case, 6 units of rain water (blue section)
are being trapped.

Example 2:

Input: height = [4,2,0,3,2,5]
Output: 9


Constraints:

    n == height.length
    1 <= n <= 2 * 10^4
    0 <= height[i] <= 10^5

---

Clean solve, no hints. Wish it were one pass, but this is fine for now.

"""

class Solution:
    def trap(self, height: List[int]) -> int:
        left_max = 0
        right_max = 0
        wheight = [0] * len(height)
        total = 0
        for i in range(len(height)):
            left_max = max(left_max, height[i])
            wheight[i] = left_max
        for i in range(len(height)):
            right_max = max(right_max, height[~i])
            wheight[~i] = min(wheight[~i], right_max)
            total += wheight[~i] - height[~i]
        return total


sol = Solution()

print(sol.trap([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]))  # 6

assert sol.trap([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]) == 6
assert sol.trap([4, 2, 0, 3, 2, 5]) == 9
assert sol.trap([0]) == 0
assert sol.trap([5]) == 0
assert sol.trap([1, 2]) == 0
assert sol.trap([2, 1]) == 0
assert sol.trap([3, 3, 3, 3]) == 0
assert sol.trap([0, 0, 0]) == 0
assert sol.trap([1, 2, 3, 4, 5]) == 0
assert sol.trap([5, 4, 3, 2, 1]) == 0
assert sol.trap([1, 2, 1]) == 0
assert sol.trap([3, 0, 3]) == 3
assert sol.trap([2, 0, 2]) == 2
assert sol.trap([5, 0, 0, 5]) == 10
assert sol.trap([3, 0, 1, 0, 3]) == 8
assert sol.trap([1, 0, 1, 0, 1]) == 2
assert sol.trap([5, 4, 1, 2]) == 1
assert sol.trap([2, 1, 0, 1, 3]) == 4
assert sol.trap([9, 6, 8, 8, 5, 6, 3]) == 3
assert sol.trap([100000, 0, 100000]) == 100000