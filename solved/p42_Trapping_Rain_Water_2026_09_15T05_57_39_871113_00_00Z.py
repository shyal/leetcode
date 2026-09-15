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


From the looks of it, it's simply a matter of taking the max from the left, the max from the right
then taking the min of both combined. Then sustract the height of the towers from that number.


[0,1,0,2,1,0,1,3,2,1,2,1]

LEETCODE: Accepted (20 ms, 21.2 MB)
"""


class Solution:
    def trap(self, height: List[int]) -> int:
        max_from_left = 0
        max_from_right = 0
        water_height = [0] * len(height)

        left_max = [0] * len(height)
        right_max = [0] * len(height)

        water_height = [0] * len(height)

        for i in range(len(height)):
            max_from_left = max(max_from_left, height[i])
            max_from_right = max(max_from_right, height[~i])
            left_max[i] = max_from_left
            right_max[~i] = max_from_right

        for i in range(len(left_max)):
            water_height[i] = min(left_max[i], right_max[i])

        total = 0

        for i in range(len(water_height)):
            total += water_height[i] - height[i]

        return total


sol = Solution()

print(sol.trap([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]))  # 6

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
