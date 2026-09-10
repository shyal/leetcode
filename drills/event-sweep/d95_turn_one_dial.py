"""
DRILL: Turn One Dial

Given two dials showing a and b, return (lo, hi): the smallest and the
largest total the dials can show after you turn exactly one of them.
A dial can be turned to any position from 1 to limit, including the one
it already shows.

Example 1:

Input: a = 2, b = 4, limit = 4
Output: (3, 8)
Explanation: turning the 4 down to 1 gives 3; turning the 2 up to 4
gives 8.

Example 2:

Input: a = 1, b = 3, limit = 4
Output: (2, 7)

Example 3:

Input: a = 3, b = 3, limit = 3
Output: (4, 6)

Constraints:

    1 <= a, b <= limit <= 10^5

    REQUIRED: O(1). NO loop over positions, NO list of totals.
"""


class Solution:
    def afterOneTurn(self, a: int, b: int, limit: int) -> Tuple[int, int]:
        pass


sol = Solution()

print(sol.afterOneTurn(2, 4, 4))  # (3, 8)

# assert sol.afterOneTurn(2, 4, 4) == (3, 8)
# assert sol.afterOneTurn(1, 3, 4) == (2, 7)
# assert sol.afterOneTurn(3, 3, 3) == (4, 6)
# assert sol.afterOneTurn(4, 2, 4) == (3, 8)
# assert sol.afterOneTurn(1, 1, 1) == (2, 2)
# assert sol.afterOneTurn(1, 100000, 100000) == (2, 200000)
# assert sol.afterOneTurn(7, 2, 9) == (3, 16)
