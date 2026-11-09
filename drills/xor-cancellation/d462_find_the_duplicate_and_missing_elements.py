"""
EPI 11.10 Find the duplicate and missing elements

Given an array A of n integers, each from 0 to n - 1, where exactly one
value appears twice and exactly one value from 0 to n - 1 is absent,
return the pair (duplicate, missing). Do not change A.

Example 1:

Input: A = [5, 3, 0, 3, 1, 2]
Output: (3, 4)
Explanation: n = 6, the value 3 appears twice and the value 4 is
absent.

Example 2:

Input: A = [0, 0]
Output: (0, 1)

Example 3:

Input: A = [1, 1]
Output: (1, 0)

Constraints:

    2 <= n <= 10^5, where n = len(A)
    0 <= A[i] <= n - 1
    Exactly one value appears twice, and exactly one value is absent.

    REQUIRED: O(n) time, O(1) extra space. NO set, NO Counter, NO list
    of counts, NO sorting, NO changes to A.
"""


class Solution:
    def find_duplicate_missing(self, A: list[int]) -> tuple[int, int]:
        pass


sol = Solution()

print(sol.find_duplicate_missing([5, 3, 0, 3, 1, 2]))  # (3, 4)


def dm(A):
    before = A[:]
    got = sol.find_duplicate_missing(A)
    assert A == before, "A must not change"
    return tuple(got)


# assert dm([5, 3, 0, 3, 1, 2]) == (3, 4)
# assert dm([0, 0]) == (0, 1)
# assert dm([1, 1]) == (1, 0)
# assert dm([0, 1, 1]) == (1, 2)
# assert dm([2, 2, 1]) == (2, 0)
# assert dm([0, 0, 2]) == (0, 1)
# assert dm([3, 1, 2, 3]) == (3, 0)
# assert dm([0, 1, 2, 2]) == (2, 3)
# assert dm([4, 1, 4, 0, 2]) == (4, 3)
# assert dm([1, 2, 3, 4, 5, 6, 7, 0, 7]) == (7, 8)
# assert dm([6, 1, 2, 3, 4, 5, 6, 0]) == (6, 7)
# assert dm(list(range(1, 10 ** 5)) + [1]) == (1, 0)
# assert dm(list(range(10 ** 5 - 1)) + [0]) == (0, 10 ** 5 - 1)
# assert dm([v for v in range(10 ** 5) if v != 31415] + [27182]) == (27182, 31415)
# assert dm([v for v in range(10 ** 5) if v != 65536] + [65535]) == (65535, 65536)
