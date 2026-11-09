"""
EPI 15.6 Generate all subsets of size k

Given integers n and k, return every subset of {1, 2, ..., n} that has
exactly k elements. Return the subsets in any order, and the entries of
each subset in any order.

Example 1:

Input: n = 4, k = 2
Output: [[1, 2], [1, 3], [1, 4], [2, 3], [2, 4], [3, 4]]

Example 2:

Input: n = 3, k = 3
Output: [[1, 2, 3]]

Example 3:

Input: n = 3, k = 0
Output: [[]]
Explanation: the empty set is the only subset with no elements.

Constraints:

    0 <= k <= n <= 20

    REQUIRED: O(k * C(n, k)) time, where C(n, k) is the number of
    subsets returned. NO itertools.combinations. NO generation of
    subsets of other sizes.
"""


class Solution:
    def combinations(self, n: int, k: int) -> list[list[int]]:
        pass


sol = Solution()

print(sol.combinations(4, 2))  # [[1, 2], [1, 3], [1, 4], [2, 3], [2, 4], [3, 4]]

# assert sorted(map(sorted, sol.combinations(4, 2))) == [[1, 2], [1, 3], [1, 4], [2, 3], [2, 4], [3, 4]]
# assert sorted(map(sorted, sol.combinations(3, 3))) == [[1, 2, 3]]
# assert sol.combinations(3, 0) == [[]]
# assert sol.combinations(0, 0) == [[]]
# assert sol.combinations(1, 1) == [[1]]
# assert sorted(map(sorted, sol.combinations(5, 1))) == [[1], [2], [3], [4], [5]]
# assert sorted(map(sorted, sol.combinations(5, 4))) == [[1, 2, 3, 4], [1, 2, 3, 5], [1, 2, 4, 5], [1, 3, 4, 5], [2, 3, 4, 5]]
# assert sorted(map(sorted, sol.combinations(5, 3))) == [[1, 2, 3], [1, 2, 4], [1, 2, 5], [1, 3, 4], [1, 3, 5], [1, 4, 5], [2, 3, 4], [2, 3, 5], [2, 4, 5], [3, 4, 5]]
# subsets = sol.combinations(16, 8)
# assert len(subsets) == 12870 and len({frozenset(s) for s in subsets}) == 12870
# assert all(len(s) == 8 and set(s) <= set(range(1, 17)) for s in subsets)
# subsets = sol.combinations(20, 3)
# assert len(subsets) == 1140 and len({frozenset(s) for s in subsets}) == 1140
# assert all(len(s) == 3 and set(s) <= set(range(1, 21)) for s in subsets)
# assert sol.combinations(20, 20) == [list(range(1, 21))]
# assert sorted(map(sorted, sol.combinations(20, 19)))[0] == list(range(1, 20))
# assert len(sol.combinations(20, 19)) == 20
