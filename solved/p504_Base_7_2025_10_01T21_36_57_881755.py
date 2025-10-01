"""
504. Base 7
Easy
Topics
premium lock icon
Companies
Given an integer num, return a string of its base 7 representation.

 

Example 1:

Input: num = 100
Output: "202"
Example 2:

Input: num = -7
Output: "-10"
 

Constraints:

-107 <= num <= 107
"""


class Solution:
    def convertToBase7(self, num: int) -> str:
        if num == 0:
            return "0"
        res = ""
        sign = 1 if num >= 0 else -1
        num *= sign
        while num > 0:
            val, r = divmod(num, 7)
            res += str(r)
            num = val
        res = ("-" if sign == -1 else "") + res[::-1]
        return res


sol = Solution()
assert sol.convertToBase7(100) == "202"
assert sol.convertToBase7(-7) == "-10"
assert sol.convertToBase7(0) == "0"
assert sol.convertToBase7(1) == "1"
assert sol.convertToBase7(6) == "6"
assert sol.convertToBase7(7) == "10"
assert sol.convertToBase7(8) == "11"
assert sol.convertToBase7(48) == "66"
assert sol.convertToBase7(49) == "100"
assert sol.convertToBase7(50) == "101"
assert sol.convertToBase7(-1) == "-1"
assert sol.convertToBase7(-6) == "-6"
assert sol.convertToBase7(-8) == "-11"
assert sol.convertToBase7(343) == "1000"
assert sol.convertToBase7(-343) == "-1000"
assert sol.convertToBase7(1000000) == "11333311"
assert sol.convertToBase7(-1000000) == "-11333311"
