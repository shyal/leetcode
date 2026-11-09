"""
EPI 6.11 Implement run-length encoding

Write two methods. The method encoding(s) returns the run-length
encoding of the string s: each maximal run of equal letters becomes the
length of the run in decimal and then the letter. The method
decoding(s) returns the string that the run-length encoding s stands
for.

Example 1:

Input: encoding("eeeffffee")
Output: "3e4f2e"

Example 2:

Input: decoding("12a1b")
Output: "aaaaaaaaaaaab"
Explanation: a run length can have more than one digit.

Example 3:

Input: encoding("")
Output: ""

Constraints:

    0 <= len(s) <= 10^5
    The input of encoding consists of letters only.
    The input of decoding is a valid encoding: a run length of at
    least 1, then a letter, repeated. Its decoded length is at most
    10^5.

    REQUIRED: O(n) time per call, where n is the length of the input
    plus the length of the output. NO itertools.groupby(), NO regex.
"""


class Solution:
    def encoding(self, s: str) -> str:
        pass

    def decoding(self, s: str) -> str:
        pass


sol = Solution()

print(sol.encoding("eeeffffee"))  # 3e4f2e

# assert sol.encoding("eeeffffee") == "3e4f2e"
# assert sol.decoding("12a1b") == "a" * 12 + "b"
# assert sol.encoding("") == ""
# assert sol.decoding("") == ""
# assert sol.encoding("a") == "1a"
# assert sol.decoding("1a") == "a"
# assert sol.encoding("abc") == "1a1b1c"
# assert sol.decoding("3e4f2e") == "eeeffffee"
# assert sol.encoding("aaaabcccaa") == "4a1b3c2a"
# assert sol.encoding("a" * 12 + "b") == "12a1b"
# assert sol.encoding("aA") == "1a1A"
# assert sol.decoding("10x10y") == "x" * 10 + "y" * 10
# assert sol.encoding("z" * 100000) == "100000z"
# assert sol.decoding("100000z") == "z" * 100000
# assert sol.encoding("ab" * 50000) == "1a1b" * 50000
# assert sol.decoding("1a1b" * 25000) == "ab" * 25000
