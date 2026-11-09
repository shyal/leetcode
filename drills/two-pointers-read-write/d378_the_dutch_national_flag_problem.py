"""
EPI 5.1 The Dutch national flag problem

Given an index pivot_index and a list of integers A, let pivot =
A[pivot_index]. Reorder A in place so that the elements less than pivot
come first, then the elements equal to pivot, then the elements greater
than pivot. The order inside each group does not matter.

Example 1:

Input: pivot_index = 1, A = [0, 1, 2, 0, 2, 1, 1]
Output: A = [0, 0, 1, 1, 1, 2, 2]
Explanation: pivot = 1.

Example 2:

Input: pivot_index = 3, A = [0, 1, 2, 0, 2, 1, 1]
Output: A = [0, 0, 1, 2, 2, 1, 1]
Explanation: pivot = 0. No element is less than 0. The five elements
greater than 0 can be in any order, so [0, 0, 2, 1, 1, 2, 1] is also
correct.

Example 3:

Input: pivot_index = 0, A = [5, -3, 8, 5, 1]
Output: A = [-3, 1, 5, 5, 8]
Explanation: [1, -3, 5, 5, 8] is also correct.

Constraints:

    1 <= len(A) <= 10^5
    0 <= pivot_index < len(A)
    -10^9 <= A[i] <= 10^9

    REQUIRED: O(n) time, O(1) extra space. NO sort, NO second list.
"""


class Solution:
    def dutch_flag_partition(self, pivot_index: int, A: list[int]) -> None:
        pass


sol = Solution()


def grouped(A, before, pivot):
    sides = [(x > pivot) - (x < pivot) for x in A]
    return sorted(A) == sorted(before) and sides == sorted(sides)


A = [0, 1, 2, 0, 2, 1, 1]
sol.dutch_flag_partition(1, A)
print(A)  # [0, 0, 1, 1, 1, 2, 2]

# A = [0, 1, 2, 0, 2, 1, 1]
# sol.dutch_flag_partition(1, A)
# assert A == [0, 0, 1, 1, 1, 2, 2]
# A = [0, 1, 2, 0, 2, 1, 1]
# sol.dutch_flag_partition(3, A)
# assert grouped(A, [0, 1, 2, 0, 2, 1, 1], 0)
# A = [0, 1, 2, 0, 2, 1, 1]
# sol.dutch_flag_partition(2, A)
# assert grouped(A, [0, 1, 2, 0, 2, 1, 1], 2)
# A = [5, -3, 8, 5, 1]
# sol.dutch_flag_partition(0, A)
# assert A in ([-3, 1, 5, 5, 8], [1, -3, 5, 5, 8])
# A = [7]
# sol.dutch_flag_partition(0, A)
# assert A == [7]
# A = [2, 1]
# sol.dutch_flag_partition(0, A)
# assert A == [1, 2]
# A = [2, 1]
# sol.dutch_flag_partition(1, A)
# assert A == [1, 2]
# A = [4, 4, 4]
# sol.dutch_flag_partition(2, A)
# assert A == [4, 4, 4]
# A = [9, 8, 7, 6, 5, 4, 3, 2, 1]
# sol.dutch_flag_partition(8, A)
# assert A[0] == 1 and grouped(A, [9, 8, 7, 6, 5, 4, 3, 2, 1], 1)
# A = [9, 8, 7, 6, 5, 4, 3, 2, 1]
# sol.dutch_flag_partition(0, A)
# assert A[-1] == 9 and grouped(A, [9, 8, 7, 6, 5, 4, 3, 2, 1], 9)
# A = [3, 5, 3, 1, 5, 3, 1, 3]
# sol.dutch_flag_partition(5, A)
# assert A == [1, 1, 3, 3, 3, 3, 5, 5]
# A = [k % 3 for k in range(10 ** 5)]
# sol.dutch_flag_partition(1, A)
# assert A == [0] * 33334 + [1] * 33333 + [2] * 33333
# A = list(range(10 ** 5, 0, -1))
# sol.dutch_flag_partition(50000, A)
# assert grouped(A, list(range(1, 10 ** 5 + 1)), 50000)
# A = [-10 ** 9, 10 ** 9] * 50000
# sol.dutch_flag_partition(1, A)
# assert A == [-10 ** 9] * 50000 + [10 ** 9] * 50000
