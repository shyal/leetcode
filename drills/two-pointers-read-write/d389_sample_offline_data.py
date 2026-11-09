"""
EPI 5.12 Sample offline data

Given an integer k and a list of distinct integers A, reorder A in place
so that A[:k] holds k elements of A chosen at random. Every subset of k
elements must be equally likely. A must hold the same elements after
the call.

Example 1:

Input: k = 3, A = [3, 7, 5, 11]
Output: A = [7, 11, 3, 5], so A[:3] = [7, 11, 3]
Explanation: A has four subsets of 3 elements. Each subset is in A[:3]
with probability 1/4, in any order.

Example 2:

Input: k = 4, A = [3, 7, 5, 11]
Output: A = [5, 3, 11, 7]
Explanation: A[:4] holds all of A, in any order.

Example 3:

Input: k = 0, A = [3, 7, 5, 11]
Output: A[:0] = []

Constraints:

    0 <= k <= len(A) <= 10^5
    The elements of A are distinct.

    REQUIRED: O(k) time, O(1) extra space. NO sample(), NO shuffle(),
    NO choices().
"""


class Solution:
    def random_sampling(self, k: int, A: list[int]) -> None:
        pass


sol = Solution()


def subset_counts(k, A, trials):
    seen = Counter()
    for _ in range(trials):
        sol.random_sampling(k, A)
        seen[frozenset(A[:k])] += 1
    return seen


A = [3, 7, 5, 11]
sol.random_sampling(3, A)
print(A[:3])  # [7, 11, 3], or any other 3 elements of A

# A = [3, 7, 5, 11]
# sol.random_sampling(3, A)
# assert len(set(A[:3])) == 3 and sorted(A) == [3, 5, 7, 11]
# A = [3, 7, 5, 11]
# sol.random_sampling(4, A)
# assert sorted(A) == [3, 5, 7, 11]
# A = [3, 7, 5, 11]
# sol.random_sampling(0, A)
# assert sorted(A) == [3, 5, 7, 11]
# A = [42]
# sol.random_sampling(1, A)
# assert A == [42]
# A = [3, 7, 5, 11]
# c = subset_counts(2, A, 60000)
# assert len(c) == 6 and all(9500 < v < 10500 for v in c.values())
# assert sorted(A) == [3, 5, 7, 11]
# A = [3, 7, 5, 11]
# c = subset_counts(3, A, 40000)
# assert len(c) == 4 and all(9500 < v < 10500 for v in c.values())
# A = [1, 2, 3, 4, 5, 6]
# c = subset_counts(1, A, 60000)
# assert len(c) == 6 and all(9500 < v < 10500 for v in c.values())
# A = list(range(10 ** 5))
# c = subset_counts(1, A, 3000)
# assert len(c) > 2800 and sorted(A) == list(range(10 ** 5))
# A = list(range(10 ** 5))
# sol.random_sampling(10 ** 5, A)
# assert sorted(A) == list(range(10 ** 5))
