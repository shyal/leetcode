"""
EPI 13.10 Team photo day - 1

Given two lists of player heights team0 and team1 of the same length,
return True when team0 can stand in the front row and team1 in the back
row, and False otherwise. Each front player stands directly in front of
a distinct back player, and each front player must be strictly shorter
than the back player behind.

Example 1:

Input: team0 = [3, 1, 4], team1 = [5, 2, 6]
Output: True
Explanation: 1 stands in front of 2, 3 in front of 5, and 4 in front of 6.

Example 2:

Input: team0 = [3, 1, 4], team1 = [4, 2, 4]
Output: False
Explanation: the player of height 4 in team0 needs a taller player
behind, and team1 has none.

Example 3:

Input: team0 = [5, 2, 6], team1 = [3, 1, 4]
Output: False

Constraints:

    1 <= len(team0) == len(team1) <= 10^5
    1 <= height <= 10^9

    REQUIRED: O(n log n) time, where n is the length of a team. NO
    search over the arrangements.
"""


class Solution:
    def valid_placement_exists(self, team0: list[int], team1: list[int]) -> bool:
        pass


sol = Solution()

print(sol.valid_placement_exists([3, 1, 4], [5, 2, 6]))  # True

# assert sol.valid_placement_exists([3, 1, 4], [5, 2, 6]) is True
# assert sol.valid_placement_exists([3, 1, 4], [4, 2, 4]) is False
# assert sol.valid_placement_exists([5, 2, 6], [3, 1, 4]) is False
# assert sol.valid_placement_exists([1], [2]) is True
# assert sol.valid_placement_exists([2], [1]) is False
# assert sol.valid_placement_exists([2], [2]) is False
# assert sol.valid_placement_exists([1, 5], [6, 2]) is True
# assert sol.valid_placement_exists([1, 5], [2, 5]) is False
# assert sol.valid_placement_exists([2, 2, 2], [3, 3, 3]) is True
# assert sol.valid_placement_exists([1, 2, 3], [2, 3, 3]) is False
# assert sol.valid_placement_exists([1, 1, 9], [10, 2, 2]) is True
# assert sol.valid_placement_exists(list(range(10 ** 5)), list(range(10 ** 5, 0, -1))) is True
# assert sol.valid_placement_exists(list(range(1, 10 ** 5 + 1)), list(range(1, 10 ** 5 + 1))) is False
# assert sol.valid_placement_exists([5] * 10 ** 5, [6] * (10 ** 5 - 1) + [5]) is False
