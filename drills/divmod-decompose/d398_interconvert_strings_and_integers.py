"""
EPI 6.1 Interconvert strings and integers

Given an integer x, int_to_string(x) returns the decimal string of x.
Given a decimal string s, string_to_int(s) returns the integer that s
represents. A negative number starts with '-'. The string s may also
start with '+'.

Example 1:

Input: x = -314
Output: "-314"

Example 2:

Input: s = "+42"
Output: 42

Example 3:

Input: x = 0
Output: "0"

Constraints:

    -10^1000 <= x <= 10^1000
    1 <= len(s) <= 1000
    s is an optional '+' or '-' and then at least one digit.

    REQUIRED: O(n) time per call, where n is the number of digits. NO
    int(), NO str(), NO repr(), NO format() or f-strings.
"""


class Solution:
    def int_to_string(self, x: int) -> str:
        pass

    def string_to_int(self, s: str) -> int:
        pass


sol = Solution()

print(sol.int_to_string(-314))  # -314

# assert sol.int_to_string(-314) == "-314"
# assert sol.string_to_int("+42") == 42
# assert sol.int_to_string(0) == "0"
# assert sol.int_to_string(7) == "7"
# assert sol.int_to_string(-7) == "-7"
# assert sol.int_to_string(10) == "10"
# assert sol.int_to_string(-1000) == "-1000"
# assert sol.int_to_string(1234567890) == "1234567890"
# assert sol.int_to_string(10 ** 999) == "1" + "0" * 999
# assert sol.int_to_string(-(10 ** 999 - 1)) == "-" + "9" * 999
# assert sol.string_to_int("0") == 0
# assert sol.string_to_int("-0") == 0
# assert sol.string_to_int("5") == 5
# assert sol.string_to_int("-314") == -314
# assert sol.string_to_int("007") == 7
# assert sol.string_to_int("1234567890") == 1234567890
# assert sol.string_to_int("9" * 1000) == 10 ** 1000 - 1
# assert sol.string_to_int("-1" + "0" * 998) == -(10 ** 998)
