"""
EPI 6.10 Write a string sinusoidally

Given a string s, write its characters on three rows in a wave that
starts in the middle row and goes up, down, down, up, and so on:
s[0] is in the middle row, s[1] in the top row, s[2] in the middle
row, s[3] in the bottom row, s[4] in the middle row, s[5] in the top
row, and the pattern repeats. Return the top row read left to right,
then the middle row, then the bottom row.

Example 1:

Input: s = "abcdefghij"
Output: "bfjacegidh"
Explanation:

      b       f       j
    a   c   e   g   i
          d       h

Example 2:

Input: s = "a"
Output: "a"

Example 3:

Input: s = "ab"
Output: "ba"

Constraints:

    0 <= len(s) <= 10^5

    REQUIRED: O(n) time. NO 2-D list.
"""


class Solution:
    def snake_string(self, s: str) -> str:
        pass


sol = Solution()

print(sol.snake_string("abcdefghij"))  # bfjacegidh

# assert sol.snake_string("abcdefghij") == "bfjacegidh"
# assert sol.snake_string("a") == "a"
# assert sol.snake_string("ab") == "ba"
# assert sol.snake_string("") == ""
# assert sol.snake_string("abc") == "bac"
# assert sol.snake_string("abcd") == "bacd"
# assert sol.snake_string("abcde") == "baced"
# assert sol.snake_string("abcdef") == "bfaced"
# assert sol.snake_string("Hi there") == "ieH hrte"
# assert sol.snake_string("0123456789ab") == "15902468a37b"
# assert sol.snake_string("x" * 100000) == "x" * 100000
# assert sol.snake_string("0123" * 25000) == "1" * 25000 + "02" * 25000 + "3" * 25000
