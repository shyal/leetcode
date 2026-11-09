"""
EPI 17.8 Compute the largest rectangle under the skyline

Given a list heights, where heights[i] is the height of a building of
width 1 at position i, return the area of the largest rectangle that lies
inside the skyline. Buildings i to j, with i <= j, hold a rectangle of area
min(heights[i..j]) * (j - i + 1).

Example 1:

Input: heights = [2, 4, 3, 5, 1, 3]
Output: 9
Explanation: buildings 1 to 3 have heights 4, 3 and 5, so they hold a
rectangle of height 3 and width 3.

          #
      #   #
      # # #     #
    # # # #     #
    # # # #  #  #
    0 1 2 3  4  5

Example 2:

Input: heights = [3]
Output: 3

Example 3:

Input: heights = []
Output: 0

Constraints:

    0 <= len(heights) <= 10^5
    0 <= heights[i] <= 10^4

    REQUIRED: O(n) time for n buildings.
"""


class Solution:
    def calculate_largest_rectangle(self, heights: list[int]) -> int:
        pass


sol = Solution()

print(sol.calculate_largest_rectangle([2, 4, 3, 5, 1, 3]))  # 9

# assert sol.calculate_largest_rectangle([2, 4, 3, 5, 1, 3]) == 9
# assert sol.calculate_largest_rectangle([3]) == 3
# assert sol.calculate_largest_rectangle([]) == 0
# assert sol.calculate_largest_rectangle([0]) == 0
# assert sol.calculate_largest_rectangle([0, 0]) == 0
# assert sol.calculate_largest_rectangle([1, 2, 3, 4, 5]) == 9
# assert sol.calculate_largest_rectangle([5, 4, 3, 2, 1]) == 9
# assert sol.calculate_largest_rectangle([2, 1, 2]) == 3
# assert sol.calculate_largest_rectangle([4, 4, 4, 0, 4]) == 12
# assert sol.calculate_largest_rectangle([6, 2, 5, 4, 5, 1, 6]) == 12
# assert sol.calculate_largest_rectangle([1, 1, 1, 1]) == 4
# assert sol.calculate_largest_rectangle([10, 1, 1]) == 10
# assert sol.calculate_largest_rectangle([1, 1, 10]) == 10
# assert sol.calculate_largest_rectangle([1] * 100000) == 100000
# assert sol.calculate_largest_rectangle(list(range(1, 100001))) == 2500050000
# assert sol.calculate_largest_rectangle(list(range(100000, 0, -1))) == 2500050000
# assert sol.calculate_largest_rectangle([10000, 0] * 50000) == 10000
