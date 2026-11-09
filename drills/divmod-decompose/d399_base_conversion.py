"""
EPI 6.2 Base conversion

Given a string num_as_string that holds an integer in base b1, return
the same integer as a string in base b2. The digits above 9 are the
capital letters 'A' to 'F'. A negative number starts with '-'.

Example 1:

Input: num_as_string = "255", b1 = 10, b2 = 16
Output: "FF"

Example 2:

Input: num_as_string = "-1010", b1 = 2, b2 = 10
Output: "-10"

Example 3:

Input: num_as_string = "0", b1 = 10, b2 = 2
Output: "0"

Constraints:

    2 <= b1, b2 <= 16
    1 <= len(num_as_string) <= 1000
    num_as_string is an optional '-' and then digits of base b1, with
    no leading zero unless the number is 0. "-0" is never given.

    REQUIRED: O(n * (1 + log_b2(b1))) time, where n is the length of
    num_as_string. NO int() with a base argument, NO hex(), bin(), oct()
    or format().
"""


class Solution:
    def convert_base(self, num_as_string: str, b1: int, b2: int) -> str:
        pass


sol = Solution()

print(sol.convert_base("255", 10, 16))  # FF

# assert sol.convert_base("255", 10, 16) == "FF"
# assert sol.convert_base("-1010", 2, 10) == "-10"
# assert sol.convert_base("0", 10, 2) == "0"
# assert sol.convert_base("1", 2, 16) == "1"
# assert sol.convert_base("F", 16, 2) == "1111"
# assert sol.convert_base("FF", 16, 2) == "11111111"
# assert sol.convert_base("10", 16, 10) == "16"
# assert sol.convert_base("-15", 10, 16) == "-F"
# assert sol.convert_base("ABC", 16, 16) == "ABC"
# assert sol.convert_base("777", 8, 2) == "111111111"
# assert sol.convert_base("2102", 3, 7) == "122"
# assert sol.convert_base("16", 10, 15) == "11"
# assert sol.convert_base("100", 10, 9) == "121"
# assert sol.convert_base("F" * 1000, 16, 2) == "1" * 4000
# assert sol.convert_base("-1" + "0" * 999, 2, 16) == "-8" + "0" * 249
# assert sol.convert_base("9" * 1000, 10, 10) == "9" * 1000
