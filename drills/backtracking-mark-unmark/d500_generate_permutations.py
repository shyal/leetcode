"""
EPI 15.4 Generate permutations

Given a list A of distinct integers, return every ordering of A. Return
the orderings in any order.

Example 1:

Input: A = [1, 2, 3]
Output: [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]

Example 2:

Input: A = [7]
Output: [[7]]

Example 3:

Input: A = [4, -2]
Output: [[4, -2], [-2, 4]]

Constraints:

    1 <= len(A) <= 8
    -100 <= A[i] <= 100
    The entries of A are distinct.

    REQUIRED: O(len(A) * len(A)!) time. NO itertools.permutations.
"""


class Solution:
    def permutations(self, A: list[int]) -> list[list[int]]:
        pass


sol = Solution()

print(sol.permutations([1, 2, 3]))  # [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]

# assert sorted(sol.permutations([1, 2, 3])) == [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]
# assert sol.permutations([7]) == [[7]]
# assert sorted(sol.permutations([4, -2])) == [[-2, 4], [4, -2]]
# assert sorted(sol.permutations([0, 9, 5])) == [[0, 5, 9], [0, 9, 5], [5, 0, 9], [5, 9, 0], [9, 0, 5], [9, 5, 0]]
# A = [1, 2, 3, 4]
# perms = sol.permutations(A)
# assert len(perms) == 24 and len(set(map(tuple, perms))) == 24
# assert all(sorted(p) == A for p in perms)
# A = [3, -1, 8, 0, 5, 2]
# perms = sol.permutations(A)
# assert len(perms) == 720 and len(set(map(tuple, perms))) == 720
# assert all(sorted(p) == [-1, 0, 2, 3, 5, 8] for p in perms)
# assert [3, -1, 8, 0, 5, 2] in perms and [2, 5, 0, 8, -1, 3] in perms
# A = list(range(8))
# perms = sol.permutations(A)
# assert len(perms) == 40320 and len(set(map(tuple, perms))) == 40320
# assert all(sorted(p) == list(range(8)) for p in perms)
