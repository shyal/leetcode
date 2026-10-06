"""
URL: https://leetcode.com/problems/maximum-score-after-splitting-a-string/description/?envType=problem-list-v2&envId=vn57k9wr

1422. Maximum Score After Splitting a String

Given a string s of zeros and ones, return the maximum score after splitting the string into two non-empty substrings (i.e. left substring and right substring).

The score after splitting a string is the number of zeros in the left substring plus the number of ones in the right substring.

Example 1:

Input: s = "011101"
Output: 5
Explanation:
All possible ways of splitting s into two non-empty substrings are:
left = "0" and right = "11101", score = 1 + 4 = 5
left = "01" and right = "1101", score = 1 + 3 = 4
left = "011" and right = "101", score = 1 + 2 = 3
left = "0111" and right = "01", score = 1 + 1 = 2
left = "01110" and right = "1", score = 2 + 1 = 3

Example 2:

Input: s = "00111"
Output: 5
Explanation: When left = "00" and right = "111", we get the maximum score = 2 + 3 = 5

Example 3:

Input: s = "1111"
Output: 3

Constraints:

    2 <= s.length <= 500
    The string s consists of characters '0' and '1' only.

---

LEETCODE: Accepted (69 ms, 19.3 MB)
"""


# mu 0.7
# def maxScore(s: str) -> int
#   digits = to_digits(s)
#   ret _max = 0
#   for i in 1..len(s)-1
#     score = sum(x == '0' for x in s[:i]) + sum(x == '1' for x in s[i:])
#     _max = max(score, _max)

def to_digits(num, reverse=False, base=10):
    if isinstance(num, str):
        ds = [int(c, base) for c in num.lstrip("-")]
    else:
        num = abs(num)
        ds = []
        while True:
            num, d = divmod(num, base)
            ds.append(d)
            if num == 0:
                break
        ds.reverse()
    return ds[::-1] if reverse else ds


class Solution:
    def maxScore(self, s: str) -> int:
        digits = to_digits(s)
        _max = 0
        for i in range(1, len(s) - 1 + 1):
            score = sum(x == '0' for x in s[:i]) + sum(x == '1' for x in s[i:])
            _max = max(score, _max)
        return _max


sol = Solution()
print(sol.maxScore('011101'))
assert sol.maxScore('011101') == 5
assert sol.maxScore('00111') == 5
assert sol.maxScore('1111') == 3
assert sol.maxScore('01') == 2
assert sol.maxScore('10') == 0
assert sol.maxScore('00') == 1
assert sol.maxScore('11') == 1
assert sol.maxScore('0000000000') == 9
assert sol.maxScore('1111111111') == 9
assert sol.maxScore('0101010101') == 6
assert sol.maxScore('1010101010') == 5
assert sol.maxScore('0' * 499 + '1') == 500
assert sol.maxScore('1' * 499 + '0') == 498
assert sol.maxScore('0' * 250 + '1' * 250) == 500
assert sol.maxScore('1' * 250 + '0' * 250) == 249
