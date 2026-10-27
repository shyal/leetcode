# URL: https://leetcode.com/problems/largest-palindromic-number/description/?envType=problem-list-v2&envId=vn57k9wr
#
# 2384. Largest Palindromic Number
#
# You are given a string num consisting of digits only.
#
# Return the largest palindromic integer (in the form of a string) that can be formed using digits taken from num. It should not contain leading zeroes.
#
# Notes:
#
# - You do not need to use all the digits of num, but you must use at least one digit.
# - The digits can be reordered.
#
# Example 1:
#
# Input: num = "444947137"
# Output: "7449447"
# Explanation:
# Use the digits "4449477" from "444947137" to form the palindromic integer "7449447".
# It can be shown that "7449447" is the largest palindromic integer that can be formed.
#
# Example 2:
#
# Input: num = "00009"
# Output: "9"
# Explanation:
# It can be shown that "9" is the largest palindromic integer that can be formed.
# Note that the integer returned should not contain leading zeroes.
#
# Constraints:
#
#     1 <= num.length <= 10^5
#     num consists of digits.
#
# ---
# learning

# mu 0.13

class Solution
  def largestPalindromic(num: str) -> str
    left, mid, cnt = ''.., counter(num)
    for d in '9876543210'
      has_lead = left != ''
      if has_lead or d != '0' # prevent leading zeros
        left += d * (cnt[d] // 2)
        if odd(cnt[d]) and not mid
          mid = d
    left + mid + left[::-1] or '0'


sol = Solution()

print(sol.largestPalindromic('444947137'))  # "7449447"

assert sol.largestPalindromic('444947137') == '7449447'
assert sol.largestPalindromic('00009') == '9'
assert sol.largestPalindromic('0') == '0'
assert sol.largestPalindromic('1') == '1'
assert sol.largestPalindromic('11') == '11'
assert sol.largestPalindromic('0000') == '0'
assert sol.largestPalindromic('1234567890') == '9'
assert sol.largestPalindromic('99999999999999999999') == '99999999999999999999'
assert sol.largestPalindromic('9876543210123456789') == '9876543210123456789'
assert sol.largestPalindromic('11223344556677889900') == '98765432100123456789'
assert sol.largestPalindromic('55555555555555555555') == '55555555555555555555'
assert sol.largestPalindromic('1234567890987654321') == '9876543210123456789'
assert sol.largestPalindromic('100000000000000000001') == '100000000000000000001'
assert sol.largestPalindromic('000000000000000000000') == '0'
