"""
EPI 5.14 Compute a random permutation

Given an integer n, return a random permutation of the integers from 0
to n - 1. Each of the n! permutations must be equally likely.

Example 1:

Input: n = 3
Output: [2, 0, 1]
Explanation: Each of the six permutations of [0, 1, 2] is returned with
probability 1/6.

Example 2:

Input: n = 1
Output: [0]

Example 3:

Input: n = 0
Output: []

Constraints:

    0 <= n <= 10^5

    REQUIRED: O(n) time. NO shuffle(), NO sample(), NO sort.
"""


class Solution:
    def compute_random_permutation(self, n: int) -> list[int]:
        pass


sol = Solution()


def perm_counts(n, trials):
    return Counter(tuple(sol.compute_random_permutation(n)) for _ in range(trials))


print(sol.compute_random_permutation(3))  # [2, 0, 1], or any other permutation of [0, 1, 2]

# assert sorted(sol.compute_random_permutation(3)) == [0, 1, 2]
# assert sol.compute_random_permutation(1) == [0]
# assert sol.compute_random_permutation(0) == []
# assert sorted(sol.compute_random_permutation(2)) == [0, 1]
# c = perm_counts(2, 20000)
# assert len(c) == 2 and all(9500 < v < 10500 for v in c.values())
# c = perm_counts(3, 60000)
# assert len(c) == 6 and all(9500 < v < 10500 for v in c.values())
# c = perm_counts(4, 240000)
# assert len(c) == 24 and all(9500 < v < 10500 for v in c.values())
# assert sorted(sol.compute_random_permutation(10 ** 5)) == list(range(10 ** 5))
# assert sol.compute_random_permutation(10 ** 5) != list(range(10 ** 5))
