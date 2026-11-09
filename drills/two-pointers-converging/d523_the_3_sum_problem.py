"""
EPI 17.4 The 3-sum problem

Given a list A of integers and an integer t, return True when there are
indices i, j and k, not necessarily distinct, such that
A[i] + A[j] + A[k] == t. Return False otherwise.

Example 1:

Input: A = [4, 9, -2, 7, 1], t = 18
Output: True
Explanation: A[0] + A[3] + A[3] = 4 + 7 + 7 = 18. An index can appear
more than once.

Example 2:

Input: A = [4, 9, -2, 7, 1], t = 13
Output: False

Example 3:

Input: A = [5], t = 15
Output: True

Constraints:

    1 <= len(A) <= 1000
    -10^6 <= A[i] <= 10^6
    -3 * 10^6 <= t <= 3 * 10^6
    A may be changed.

    REQUIRED: O(n^2) time and O(1) extra space for n entries. NO set, NO dict.
"""


class Solution:
    def has_three_sum(self, A: list[int], t: int) -> bool:
        pass


sol = Solution()

print(sol.has_three_sum([4, 9, -2, 7, 1], 18))  # True

# assert sol.has_three_sum([4, 9, -2, 7, 1], 18) is True
# assert sol.has_three_sum([4, 9, -2, 7, 1], 13) is False
# assert sol.has_three_sum([5], 15) is True
# assert sol.has_three_sum([5], 10) is False
# assert sol.has_three_sum([4, 9, -2, 7, 1], 30) is False
# assert sol.has_three_sum([4, 9, -2, 7, 1], 27) is True
# assert sol.has_three_sum([4, 9, -2, 7, 1], -6) is True
# assert sol.has_three_sum([-3, 0, 6], 0) is True
# assert sol.has_three_sum([1, 2], 7) is False
# assert sol.has_three_sum([1, 2], 6) is True
# assert sol.has_three_sum([1, 2], 3) is True
# assert sol.has_three_sum([2, 7, 11, 15], 26) is False
# assert sol.has_three_sum([2, 7, 11, 15], 33) is True
# assert sol.has_three_sum([0], 0) is True
# assert sol.has_three_sum([1000000, -1000000], 3000000) is True
# assert sol.has_three_sum([3 * i for i in range(1000)], 1) is False
# assert sol.has_three_sum([3 * i for i in range(1000)], 8991) is True
# assert sol.has_three_sum([3 * i for i in range(1000)], 8994) is False
# assert sol.has_three_sum(list(range(1000, 0, -1)), 3) is True
