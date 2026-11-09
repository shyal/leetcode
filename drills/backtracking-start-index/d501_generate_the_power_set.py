"""
EPI 15.5 Generate the power set

Given a list input_set of distinct integers, return every subset of it.
Return the subsets in any order, and the entries of each subset in any
order.

Example 1:

Input: input_set = [1, 2, 3]
Output: [[], [1], [1, 2], [1, 2, 3], [1, 3], [2], [2, 3], [3]]

Example 2:

Input: input_set = [5, -1]
Output: [[], [5], [5, -1], [-1]]

Example 3:

Input: input_set = []
Output: [[]]
Explanation: the empty set has one subset, the empty set.

Constraints:

    0 <= len(input_set) <= 16
    -1000 <= input_set[i] <= 1000
    The entries of input_set are distinct.

    REQUIRED: O(n * 2^n) time, where n is len(input_set). NO
    itertools.combinations.
"""


class Solution:
    def generate_power_set(self, input_set: list[int]) -> list[list[int]]:
        pass


sol = Solution()

print(sol.generate_power_set([1, 2, 3]))  # [[], [1], [1, 2], [1, 2, 3], [1, 3], [2], [2, 3], [3]]

# assert sorted(map(sorted, sol.generate_power_set([1, 2, 3]))) == [[], [1], [1, 2], [1, 2, 3], [1, 3], [2], [2, 3], [3]]
# assert sorted(map(sorted, sol.generate_power_set([5, -1]))) == [[], [-1], [-1, 5], [5]]
# assert sol.generate_power_set([]) == [[]]
# assert sorted(map(sorted, sol.generate_power_set([0]))) == [[], [0]]
# assert sorted(map(sorted, sol.generate_power_set([9, 4, 7]))) == [[], [4], [4, 7], [4, 7, 9], [4, 9], [7], [7, 9], [9]]
# subsets = sol.generate_power_set([1, 2, 3, 4])
# assert len(subsets) == 16 and len({frozenset(s) for s in subsets}) == 16
# subsets = sol.generate_power_set(list(range(10)))
# assert len(subsets) == 1024 and len({frozenset(s) for s in subsets}) == 1024
# assert all(set(s) <= set(range(10)) and len(set(s)) == len(s) for s in subsets)
# subsets = sol.generate_power_set(list(range(-8, 8)))
# assert len(subsets) == 65536 and len({frozenset(s) for s in subsets}) == 65536
# assert [len(s) for s in subsets].count(8) == 12870
