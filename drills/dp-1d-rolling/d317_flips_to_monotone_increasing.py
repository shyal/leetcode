"""
Given a binary string s, return the minimum number of flips that make s
monotone increasing. A flip changes a 0 to 1 or a 1 to 0. A binary
string is monotone increasing when it is some number of 0 followed by
some number of 1, either number possibly zero.

Iterate over s from left to right with two counts, both 0 at the start:
the number of 1 seen so far, and the minimum flips that make the prefix
monotone increasing. At each 1, add 1 to the count of 1. At each 0 there
are two ways to make the prefix monotone increasing. Flip this 0 to 1:
the flips so far plus 1. Or flip every 1 before it to 0: as many flips
as the count of 1. Take the smaller.

For example with s = "0110", the first 0 takes the smaller of 0 + 1 and
0, the two 1 raise the count of 1 to 2, and the last 0 takes the smaller
of 0 + 1 and 2. The answer is 1.

Example 1:

Input: s = "0110"
Output: 1
Explanation: flip the last 0: "0111".

Example 2:

Input: s = "11000"
Output: 2
Explanation: flip both 1: "00000".

Example 3:

Input: s = "01"
Output: 0
Explanation: s is already monotone increasing.

Constraints:

    1 <= len(s) <= 10^5
    s[i] is 0 or 1.

    REQUIRED: O(n) time, O(1) extra space, a single pass.
"""


class Solution:
    def minFlips(self, s: str) -> int:
        pass


sol = Solution()

print(sol.minFlips("0110"))  # 1

# assert sol.minFlips("0110") == 1
# assert sol.minFlips("11000") == 2
# assert sol.minFlips("01") == 0
# assert sol.minFlips("10") == 1
# assert sol.minFlips("001001") == 1
# assert sol.minFlips("0") == 0
# assert sol.minFlips("1") == 0
# assert sol.minFlips("0000") == 0
# assert sol.minFlips("1111") == 0
# assert sol.minFlips("1001") == 1
# assert sol.minFlips("00001111") == 0
# assert sol.minFlips("11110000") == 4
# assert sol.minFlips("01010101") == 3
# assert sol.minFlips("1" * 50000 + "0" * 50000) == 50000
# assert sol.minFlips("10" * 50000) == 50000
