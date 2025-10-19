"""
URL: https://leetcode.com/problems/remove-trailing-zeros-from-a-string/description/?envType=problem-list-v2&envId=vn57k9wr

2710. Remove Trailing Zeros From a String

Given a positive integer num represented as a string, return the integer num without trailing zeros as a string.


Example 1:

Input: num = "51230100"
Output: "512301"
Explanation: Integer "51230100" has 2 trailing zeros, we remove them and return integer "512301".

Example 2:

Input: num = "123"
Output: "123"
Explanation: Integer "123" has no trailing zeros, we return integer "123".


Constraints:

        1 <= num.length <= 1000
        num consists of only digits.
        num doesn't have any leading zeros.
"""


class Solution:
    def removeTrailingZeros(self, num: str) -> str:
        return "".join(dropwhile(lambda x: x == "0", num[::-1]))[::-1]


sol = Solution()

res = sol.removeTrailingZeros(num="51230100")
assert res == "512301"

res = sol.removeTrailingZeros(num="123")
assert res == "123"
