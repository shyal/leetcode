"""
URL: https://leetcode.com/problems/largest-palindromic-number/description/?envType=problem-list-v2&envId=vn57k9wr

2384. Largest Palindromic Number

You are given a string num consisting of digits only.

Return the largest palindromic integer (in the form of a string) that can be formed using digits taken from num. It should not contain leading zeroes.

Notes:

- You do not need to use all the digits of num, but you must use at least one digit.
- The digits can be reordered.

Example 1:

Input: num = "444947137"
Output: "7449447"
Explanation:
Use the digits "4449477" from "444947137" to form the palindromic integer "7449447".
It can be shown that "7449447" is the largest palindromic integer that can be formed.

Example 2:

Input: num = "00009"
Output: "9"
Explanation:
It can be shown that "9" is the largest palindromic integer that can be formed.
Note that the integer returned should not contain leading zeroes.

Constraints:

    1 <= num.length <= 10^5
    num consists of digits.
---
asc

9: 1
1: 1
3: 1
7: 2
4: 4

for the 1 counts, keep the largest number, it will go in the middle

9: 1
4: 4
7: 2

so 9

then add the even numbers from smallest to largest

     7449447


but let's add some odd counts to the mix


'4': 4
'8': 3
'7': 2
'1': 1
'3': 1

    874484478
"""


# mu 0.12
# class Solution
#   def largestPalindromic(num: str) -> str
#     num = [int(x) for x in num]
#     counts = counter(num)
#     ones = []
#     for n in set(num)
#       if odd(counts[n])
#         ones.append(n)
#     ones.sort(reverse=True)
#     odd_numbers = [x for x in set(num) if odd(counts[x]) and counts[x] > 1]
#     for o in odd_numbers
#       counts[0] -= 1
#     numbers = [x for x in set(num) if even(counts[x])]
#     numbers.extend(odd_numbers)
#     numbers.sort()
#     res = []
#     for n in numbers
#       res.extend([n] * (counts[n] // 2))
#     res = ''.join(str(x) for x in (res[::-1] + ([ones[0]] if ones else []) + res))
#     first_non_zero = 0
#     for >i, c in res
#       if c == '0'
#         pass
#       else
#         first_non_zero = i
#         break
#     if first_non_zero != 0
#       return res[first_non_zero:-first_non_zero]
#     return res
#

from collections import Counter


def odd(n):
    return n % 2 == 1


def even(n):
    return n % 2 == 0


class Solution:
    def largestPalindromic(self, num: str) -> str:
        num = [int(x) for x in num]
        counts = Counter(num)
        ones = []
        for n in set(num):
            if odd(counts[n]):
                ones.append(n)
        ones.sort(reverse=True)
        odd_numbers = [x for x in set(num) if odd(counts[x]) and counts[x] > 1]
        for o in odd_numbers:
            counts[0] -= 1
        numbers = [x for x in set(num) if even(counts[x])]
        numbers.extend(odd_numbers)
        numbers.sort()
        res = []
        for n in numbers:
            res.extend([n] * (counts[n] // 2))
        res = ''.join(str(x) for x in (res[::-1] + ([ones[0]] if ones else []) + res))
        first_non_zero = 0
        for i, c in enumerate(res):
            if c == '0':
                pass
            else:
                first_non_zero = i
                break
        if first_non_zero != 0:
            return res[first_non_zero:-first_non_zero]
        return res


sol = Solution()
print(sol.largestPalindromic('00009'))
_l, _r = sol.largestPalindromic('00009'), '9'
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.largestPalindromic('100000000000000000001'), '100000000000000000001'
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.largestPalindromic('0000'), '0'
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
print(sol.largestPalindromic('444947137'))
_l, _r = sol.largestPalindromic('444947137'), '7449447'
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.largestPalindromic('0'), '0'
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.largestPalindromic('1'), '1'
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.largestPalindromic('11'), '11'
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.largestPalindromic('1234567890'), '9'
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.largestPalindromic('99999999999999999999'), '99999999999999999999'
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.largestPalindromic('9876543210123456789'), '9876543210123456789'
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.largestPalindromic('11223344556677889900'), '98765432100123456789'
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.largestPalindromic('55555555555555555555'), '55555555555555555555'
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.largestPalindromic('1234567890987654321'), '9876543210123456789'
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"


# FAILED: walked away after 29m 18s; no working solution.
# Judge the move the defect is in as struggled, not clean. A move the code never reached gets no verdict.
