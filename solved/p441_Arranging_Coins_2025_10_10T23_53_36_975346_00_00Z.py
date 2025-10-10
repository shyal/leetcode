"""
URL: https://leetcode.com/problems/arranging-coins/description/

441. Arranging Coins

You are given an integer n representing the total number of coins.

For example, given n = 5, the staircase looks like this:

*
* *
* *

But since the third row is incomplete (it would need 3 coins, but only 2 are left), you return 2.

Return the number of complete rows of the staircase you can build with exactly n coins. The last row of the staircase may be incomplete.

Example 1:

Input: n = 5
Output: 2
Explanation: Because the 3rd row is incomplete, we return 2.

Example 2:

Input: n = 8
Output: 3
Explanation: Because the 4th row is incomplete, we return 3.

Constraints:

    1 <= n <= 2^31 - 1

---

Hm so if we think of the number of stars for a given row, it's actually n.

So if n == 10, then the number of stars in that row is 10. The total
number of stars for t rows is `t * (t + 1) / 2`. We can use the quadratic formula
to see that therefor, given the number of stars (with the last row
complete) we can compute the row with: `int((-1 + sqrt(1 + 8 * n)) // 2)`.

I did get some help from Grok for computing `int((-1 + sqrt(1 + 8 * n)) // 2)`
so need to refresh some math, ideally involving the quadratic formula.
"""

from math import sqrt


class Solution:
    def arrangeCoins(self, n: int) -> int:
        return int((-1 + sqrt(1 + 8 * n)) // 2)


sol = Solution()

assert sol.arrangeCoins(5) == 2
assert sol.arrangeCoins(8) == 3
assert sol.arrangeCoins(1) == 1
assert sol.arrangeCoins(2) == 1
assert sol.arrangeCoins(3) == 2
assert sol.arrangeCoins(4) == 2
assert sol.arrangeCoins(6) == 3
assert sol.arrangeCoins(9) == 3
assert sol.arrangeCoins(10) == 4
assert sol.arrangeCoins(2147483647) == 65535
