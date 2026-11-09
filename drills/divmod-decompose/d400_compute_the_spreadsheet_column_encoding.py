"""
EPI 6.3 Compute the spreadsheet column encoding

Given a spreadsheet column id col, return its column number. The
columns are A, B, ..., Z, then AA, AB, ..., AZ, BA, ..., ZZ, then AAA,
and so on. Column A is number 1.

Example 1:

Input: col = "D"
Output: 4

Example 2:

Input: col = "AA"
Output: 27
Explanation: Z is 26, and AA is the column after Z.

Example 3:

Input: col = "ZZ"
Output: 702

Constraints:

    1 <= len(col) <= 20
    col consists of capital letters 'A' to 'Z' only.

    REQUIRED: O(n) time, O(1) extra space, where n is len(col). NO int()
    with a base argument.
"""


class Solution:
    def ss_decode_col_id(self, col: str) -> int:
        pass


sol = Solution()

print(sol.ss_decode_col_id("D"))  # 4

# assert sol.ss_decode_col_id("D") == 4
# assert sol.ss_decode_col_id("AA") == 27
# assert sol.ss_decode_col_id("ZZ") == 702
# assert sol.ss_decode_col_id("A") == 1
# assert sol.ss_decode_col_id("Z") == 26
# assert sol.ss_decode_col_id("AZ") == 52
# assert sol.ss_decode_col_id("BA") == 53
# assert sol.ss_decode_col_id("ZY") == 701
# assert sol.ss_decode_col_id("AAA") == 703
# assert sol.ss_decode_col_id("XFD") == 16384
# assert sol.ss_decode_col_id("A" * 20) == sum(26 ** k for k in range(20))
# assert sol.ss_decode_col_id("Z" * 20) == sum(26 * 26 ** k for k in range(20))
