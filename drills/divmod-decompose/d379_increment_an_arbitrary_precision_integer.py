"""
EPI 5.2 Increment an arbitrary-precision integer

Given a list of decimal digits A that represents a non-negative integer,
most significant digit first, return the list of digits of that integer
plus 1, in the same form.

Example 1:

Input: A = [1, 2, 9]
Output: [1, 3, 0]
Explanation: 129 + 1 = 130.

Example 2:

Input: A = [9, 9]
Output: [1, 0, 0]
Explanation: 99 + 1 = 100. The result has one more digit than A.

Example 3:

Input: A = [0]
Output: [1]

Constraints:

    1 <= len(A) <= 10^5
    0 <= A[i] <= 9
    A[0] != 0 unless A == [0]

    REQUIRED: O(n) time. NO int(), NO str().
"""


class Solution:
    def plus_one(self, A: list[int]) -> list[int]:
        pass


sol = Solution()

print(sol.plus_one([1, 2, 9]))  # [1, 3, 0]

# assert sol.plus_one([1, 2, 9]) == [1, 3, 0]
# assert sol.plus_one([9, 9]) == [1, 0, 0]
# assert sol.plus_one([0]) == [1]
# assert sol.plus_one([8]) == [9]
# assert sol.plus_one([9]) == [1, 0]
# assert sol.plus_one([1, 0]) == [1, 1]
# assert sol.plus_one([1, 9]) == [2, 0]
# assert sol.plus_one([1, 0, 0]) == [1, 0, 1]
# assert sol.plus_one([1, 9, 9]) == [2, 0, 0]
# assert sol.plus_one([9, 8, 9]) == [9, 9, 0]
# assert sol.plus_one([4, 9, 9, 9]) == [5, 0, 0, 0]
# assert sol.plus_one([9, 9, 9, 9]) == [1, 0, 0, 0, 0]
# assert sol.plus_one([3, 0, 9, 0]) == [3, 0, 9, 1]
# assert sol.plus_one([9] * 10 ** 5) == [1] + [0] * 10 ** 5
# assert sol.plus_one([1] + [0] * 99999) == [1] + [0] * 99998 + [1]
# assert sol.plus_one([5] + [9] * 99999) == [6] + [0] * 99999
