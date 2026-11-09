"""
EPI 13.5 Smallest nonconstructible value

Given a list of positive integers A, return the smallest positive
integer that is not the sum of a subset of A. Each entry of A can be
used at most once in a sum, and equal entries count as separate
entries.

Example 1:

Input: A = [1, 2, 5]
Output: 4
Explanation: 1, 2, 3 = 1 + 2 are sums of subsets. No subset sums to 4.

Example 2:

Input: A = [1, 1, 1, 1]
Output: 5

Example 3:

Input: A = [2]
Output: 1

Constraints:

    0 <= len(A) <= 10^5
    1 <= A[i] <= 10^9

    REQUIRED: O(n log n) time, where n is the length of A. NO
    enumeration of subsets.
"""


class Solution:
    def smallest_nonconstructible_value(self, A: list[int]) -> int:
        pass


sol = Solution()

print(sol.smallest_nonconstructible_value([1, 2, 5]))  # 4

# assert sol.smallest_nonconstructible_value([1, 2, 5]) == 4
# assert sol.smallest_nonconstructible_value([1, 1, 1, 1]) == 5
# assert sol.smallest_nonconstructible_value([2]) == 1
# assert sol.smallest_nonconstructible_value([]) == 1
# assert sol.smallest_nonconstructible_value([1]) == 2
# assert sol.smallest_nonconstructible_value([1, 3]) == 2
# assert sol.smallest_nonconstructible_value([1, 2, 4]) == 8
# assert sol.smallest_nonconstructible_value([5, 1, 2, 1]) == 10
# assert sol.smallest_nonconstructible_value([1, 1, 3, 10]) == 6
# assert sol.smallest_nonconstructible_value([12, 2, 1, 15, 2, 4]) == 10
# assert sol.smallest_nonconstructible_value([4, 3, 2, 1]) == 11
# assert sol.smallest_nonconstructible_value([1] * 10 ** 5) == 10 ** 5 + 1
# assert sol.smallest_nonconstructible_value(list(range(10 ** 5, 0, -1))) == 5000050001
# assert sol.smallest_nonconstructible_value([10 ** 9] * 10 ** 5) == 1
# assert sol.smallest_nonconstructible_value(list(range(1, 1000)) + [10 ** 9]) == 499501
