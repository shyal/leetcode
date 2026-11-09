"""
EPI 11.7 Find the min and max simultaneously

Given a nonempty array A of integers, return the pair (smallest,
largest) of its smallest and largest values. A comparison is one use of
<, <=, > or >= on two values of A.

Example 1:

Input: A = [3, 2, 5, 1, 2, 4]
Output: (1, 5)

Example 2:

Input: A = [7]
Output: (7, 7)

Example 3:

Input: A = [4, 4]
Output: (4, 4)

Constraints:

    1 <= len(A) <= 10^5
    -10^9 <= A[i] <= 10^9

    REQUIRED: O(n) time, O(1) extra space, at most ceil(3n / 2) - 2
    comparisons. NO min(), NO max(), NO sorting.
"""


class Solution:
    def find_min_max(self, A: list[int]) -> tuple[int, int]:
        pass


sol = Solution()

print(sol.find_min_max([3, 2, 5, 1, 2, 4]))  # (1, 5)

# assert sol.find_min_max([3, 2, 5, 1, 2, 4]) == (1, 5)
# assert sol.find_min_max([7]) == (7, 7)
# assert sol.find_min_max([4, 4]) == (4, 4)
# assert sol.find_min_max([1, 2]) == (1, 2)
# assert sol.find_min_max([2, 1]) == (1, 2)
# assert sol.find_min_max([3, 1, 2]) == (1, 3)
# assert sol.find_min_max([1, 2, 3, 4, 5]) == (1, 5)
# assert sol.find_min_max([5, 4, 3, 2, 1]) == (1, 5)
# assert sol.find_min_max([2, 9, 9, 2]) == (2, 9)
# assert sol.find_min_max([-10 ** 9, 10 ** 9, 0]) == (-10 ** 9, 10 ** 9)
# assert sol.find_min_max([0, 0, 0, 0, 0, 0, 0]) == (0, 0)
# assert sol.find_min_max([5, -1, 8, 3, -7, 2, 6, 0]) == (-7, 8)
# assert sol.find_min_max(list(range(10 ** 5))) == (0, 10 ** 5 - 1)
# assert sol.find_min_max(list(range(10 ** 5 - 1, -1, -1))) == (0, 10 ** 5 - 1)
# assert sol.find_min_max([(v * 7919) % 100003 for v in range(10 ** 5 - 1)]) == (0, 100002)
