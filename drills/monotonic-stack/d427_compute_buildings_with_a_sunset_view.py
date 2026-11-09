"""
EPI 8.5 Compute buildings with a sunset view

Given an iterator sequence over the heights of buildings in a row,
from east to west, return the indices of the buildings that can see
the sunset to the west. Building i can see the sunset when every
building after it in sequence is strictly lower. Return the indices in
decreasing order. You can read sequence only once, from the start.

Example 1:

Input: sequence = iter([4, 2, 3, 1])
Output: [3, 2, 0]
Explanation: building 1 (height 2) has building 2 (height 3) to its
west.

Example 2:

Input: sequence = iter([5, 5])
Output: [1]
Explanation: building 0 is not strictly higher than building 1.

Example 3:

Input: sequence = iter([1, 2, 3])
Output: [2]

Constraints:

    0 <= number of buildings <= 2 * 10^5
    1 <= height <= 10^9

    REQUIRED: O(n) time. NO list(sequence), NO sorting.
"""


class Solution:
    def examine_buildings_with_sunset(self, sequence: Iterator[int]) -> list[int]:
        pass


sol = Solution()

print(sol.examine_buildings_with_sunset(iter([4, 2, 3, 1])))  # [3, 2, 0]

# assert sol.examine_buildings_with_sunset(iter([4, 2, 3, 1])) == [3, 2, 0]
# assert sol.examine_buildings_with_sunset(iter([5, 5])) == [1]
# assert sol.examine_buildings_with_sunset(iter([1, 2, 3])) == [2]
# assert sol.examine_buildings_with_sunset(iter([])) == []
# assert sol.examine_buildings_with_sunset(iter([7])) == [0]
# assert sol.examine_buildings_with_sunset(iter([3, 2, 1])) == [2, 1, 0]
# assert sol.examine_buildings_with_sunset(iter([2, 2, 2, 2])) == [3]
# assert sol.examine_buildings_with_sunset(iter([1, 3, 2, 3])) == [3]
# assert sol.examine_buildings_with_sunset(iter([10, 1, 9, 2, 8])) == [4, 2, 0]
# assert sol.examine_buildings_with_sunset(iter([9, 1, 1, 1, 1])) == [4, 0]
# assert sol.examine_buildings_with_sunset(iter(range(200000, 0, -1))) == list(range(199999, -1, -1))
# assert sol.examine_buildings_with_sunset(iter(range(1, 200001))) == [199999]
# assert sol.examine_buildings_with_sunset(iter([5] * 200000)) == [199999]
# assert sol.examine_buildings_with_sunset(iter([200000 - i // 2 for i in range(200000)])) == list(range(199999, 0, -2))
