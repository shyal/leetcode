"""
Given a list route of points [x, y, z] in flight order, return the
smallest amount of energy the drone must hold at the first point to
reach the last point. Rising one unit of z costs one unit of energy.
Dropping one unit of z gains one unit. A change in x or y costs
nothing. The energy must never fall below zero at any point of the
route.

Example 1:

Input: route = [[0, 2, 10], [3, 5, 0], [9, 20, 6], [10, 12, 15], [10, 10, 8]]
Output: 5
Explanation: with 5 units the energy at the five points is 5, 15, 9,
0, 7. With 4 units it is -1 at the fourth point. The total rise on the
route is 15, and the drop from the first z to the last is 2, and
neither is the answer.

Example 2:

Input: route = [[0, 2, 6], [10, 10, 20]]
Output: 14

Example 3:

Input: route = [[0, 1, 19]]
Output: 0

Constraints:

    1 <= len(route) <= 100
    len(route[i]) == 3
    0 <= x, y, z <= 10^4

    REQUIRED: O(n) time, O(1) extra space, one pass. NO list of the
    energy at every point.
"""


class Solution:
    def calc_drone_min_energy(self, route: list[list[int]]) -> int:
        pass


sol = Solution()

print(sol.calc_drone_min_energy([[0, 2, 10], [3, 5, 0], [9, 20, 6], [10, 12, 15], [10, 10, 8]]))  # 5

# assert sol.calc_drone_min_energy([[0, 2, 10], [3, 5, 0], [9, 20, 6], [10, 12, 15], [10, 10, 8]]) == 5
# assert sol.calc_drone_min_energy([[0, 2, 6], [10, 10, 20]]) == 14
# assert sol.calc_drone_min_energy([[0, 1, 19]]) == 0
# assert sol.calc_drone_min_energy([[0, 2, 10], [10, 10, 8]]) == 0
# assert sol.calc_drone_min_energy([[0, 2, 2], [3, 5, 38], [9, 20, 6], [10, 12, 15], [10, 10, 8]]) == 36
# assert sol.calc_drone_min_energy([[0, 2, 10], [3, 5, 9], [9, 20, 6], [10, 12, 2], [10, 10, 10], [10, 10, 2]]) == 0
# assert sol.calc_drone_min_energy([[0, 0, 0], [0, 0, 10000]]) == 10000
# assert sol.calc_drone_min_energy([[0, 0, 10000], [0, 0, 0], [0, 0, 10000]]) == 0
# assert sol.calc_drone_min_energy([[0, 0, 5], [0, 0, 1], [0, 0, 3]]) == 0
# assert sol.calc_drone_min_energy([[0, 0, 5], [0, 0, 1], [0, 0, 7]]) == 2
# assert sol.calc_drone_min_energy([[i, i, i] for i in range(100)]) == 99
# assert sol.calc_drone_min_energy([[i, i, 99 - i] for i in range(100)]) == 0
# assert sol.calc_drone_min_energy([[i, 0, i % 2 * 3] for i in range(100)]) == 3
