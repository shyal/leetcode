"""
EPI 5.10 Permute the elements of an array

Given a permutation perm of the indices of a list A, move each element
A[i] to index perm[i], in place. You can change perm.

Example 1:

Input: perm = [2, 0, 1, 3], A = ["a", "b", "c", "d"]
Output: A = ["b", "c", "a", "d"]
Explanation: "a" moves to index 2, "b" to index 0, "c" to index 1, and
"d" stays at index 3.

Example 2:

Input: perm = [1, 0], A = [7, 8]
Output: A = [8, 7]

Example 3:

Input: perm = [0], A = [5]
Output: A = [5]

Constraints:

    1 <= len(A) <= 10^5
    len(perm) == len(A)
    perm holds each integer from 0 to len(A) - 1 once.

    REQUIRED: O(n) time, O(1) extra space. NO second list, NO sort.
"""


class Solution:
    def apply_permutation(self, perm: list[int], A: list) -> None:
        pass


sol = Solution()

A = ["a", "b", "c", "d"]
sol.apply_permutation([2, 0, 1, 3], A)
print(A)  # ['b', 'c', 'a', 'd']

# A = ["a", "b", "c", "d"]
# sol.apply_permutation([2, 0, 1, 3], A)
# assert A == ["b", "c", "a", "d"]
# A = [7, 8]
# sol.apply_permutation([1, 0], A)
# assert A == [8, 7]
# A = [5]
# sol.apply_permutation([0], A)
# assert A == [5]
# A = [1, 2, 3]
# sol.apply_permutation([0, 1, 2], A)
# assert A == [1, 2, 3]
# A = [1, 2, 3]
# sol.apply_permutation([1, 2, 0], A)
# assert A == [3, 1, 2]
# A = [1, 2, 3]
# sol.apply_permutation([2, 0, 1], A)
# assert A == [2, 3, 1]
# A = ["a", "b", "c", "d", "e", "f"]
# sol.apply_permutation([1, 0, 3, 2, 5, 4], A)
# assert A == ["b", "a", "d", "c", "f", "e"]
# A = ["a", "b", "c", "d", "e"]
# sol.apply_permutation([4, 3, 2, 1, 0], A)
# assert A == ["e", "d", "c", "b", "a"]
# A = [10, 20, 30, 40, 50]
# sol.apply_permutation([3, 4, 0, 2, 1], A)
# assert A == [30, 50, 40, 10, 20]
# A = list(range(10 ** 5))
# sol.apply_permutation(list(range(1, 10 ** 5)) + [0], A)
# assert A == [10 ** 5 - 1] + list(range(10 ** 5 - 1))
# A = list(range(10 ** 5))
# sol.apply_permutation(list(range(10 ** 5 - 1, -1, -1)), A)
# assert A == list(range(10 ** 5 - 1, -1, -1))
# perm = sample(range(1000), 1000)
# p = perm[:]
# A = [2 * x for x in range(1000)]
# sol.apply_permutation(perm, A)
# assert all(A[p[i]] == 2 * i for i in range(1000))
