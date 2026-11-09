"""
EPI 5.15 Compute a random subset

Given integers n and k, return a list of k distinct integers chosen at
random from 0 to n - 1. Every subset of k integers must be equally
likely. The order inside the list does not matter.

Example 1:

Input: n = 4, k = 2
Output: [3, 0]
Explanation: There are six subsets of 2 integers from 0 to 3. Each subset
is returned with probability 1/6, in any order.

Example 2:

Input: n = 5, k = 5
Output: [2, 4, 0, 1, 3]
Explanation: All of 0 to 4, in any order.

Example 3:

Input: n = 10^9, k = 3
Output: [512, 999999937, 70412]
Explanation: k is small and n is very large.

Constraints:

    1 <= n <= 10^9
    0 <= k <= min(n, 10^5)

    REQUIRED: O(k) time, O(k) space. NO sample(), NO list or range
    object of size n.
"""


class Solution:
    def random_subset(self, n: int, k: int) -> list[int]:
        pass


sol = Solution()


def subset_counts(n, k, trials):
    return Counter(frozenset(sol.random_subset(n, k)) for _ in range(trials))


print(sol.random_subset(4, 2))  # [3, 0], or any other 2 integers from 0 to 3

# r = sol.random_subset(4, 2)
# assert len(r) == 2 and len(set(r)) == 2 and set(r) <= {0, 1, 2, 3}
# assert sorted(sol.random_subset(5, 5)) == [0, 1, 2, 3, 4]
# assert sol.random_subset(1, 1) == [0]
# assert sol.random_subset(7, 0) == []
# c = subset_counts(4, 2, 60000)
# assert len(c) == 6 and all(9500 < v < 10500 for v in c.values())
# c = subset_counts(4, 3, 40000)
# assert len(c) == 4 and all(9500 < v < 10500 for v in c.values())
# c = subset_counts(6, 1, 60000)
# assert len(c) == 6 and all(9500 < v < 10500 for v in c.values())
# r = sol.random_subset(10 ** 9, 3)
# assert len(set(r)) == 3 and all(0 <= x < 10 ** 9 for x in r)
# r = sol.random_subset(10 ** 9, 10 ** 5)
# assert len(r) == 10 ** 5 and len(set(r)) == 10 ** 5 and all(0 <= x < 10 ** 9 for x in r)
# assert sorted(sol.random_subset(10 ** 5, 10 ** 5)) == list(range(10 ** 5))
