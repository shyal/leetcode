"""
URL: https://leetcode.com/problems/largest-number-after-digit-swaps-by-parity/description/?envType=problem-list-v2&envId=vn57k9wr

2231. Largest Number After Digit Swaps by Parity

You are given a positive integer num. You may swap any two digits of num that have the same parity (i.e. both odd digits or both even digits).

Return the largest possible value of num after any number of swaps.

Example 1:

Input: num = 1234
Output: 3412
Explanation: Swap the digit 3 with the digit 1, this results in the number 3214.
Swap the digit 2 with the digit 4, this results in the number 3412.
Note that there may be other sequences of swaps but it can be shown that 3412 is the largest possible number.
Also note that we may not swap the digit 4 with the digit 1 since they are of different parities.

Example 2:

Input: num = 65875
Output: 87655
Explanation: Swap the digit 8 with the digit 6, this results in the number 85675.
Swap the first digit 5 with the digit 7, this results in the number 87655.
Note that there may be other sequences of swaps but it can be shown that 87655 is the largest possible number.

Constraints:

    1 <= num <= 10^9

---


1 2 3 4
o e o e

3 4 1 2
o e o e

LEETCODE: Accepted (0 ms, 19.4 MB)
"""


class Solution:

    def getDigits(self, num):
        digits = []
        while num:
            digits.append(num % 10)
            num //= 10
        return digits[::-1]

    def largestInteger(self, num: int) -> int:
        digits = self.getDigits(num)
        even = [x for x in digits if x % 2 == 0]
        odd = [x for x in digits if x % 2 != 0]
        even.sort()
        odd.sort()
        parity = [x % 2 == 0 for x in digits]
        res = []
        for p in parity:
            if p:
                res.append(even.pop())
            else:
                res.append(odd.pop())
        return reduce(lambda acc, val: acc * 10 + val, res)


sol = Solution()

print(sol.largestInteger(1234))  # 3412

assert sol.largestInteger(1234) == 3412
assert sol.largestInteger(65875) == 87655

assert sol.largestInteger(1) == 1
assert sol.largestInteger(2) == 2
assert sol.largestInteger(111111111) == 111111111
assert sol.largestInteger(222222222) == 222222222
assert sol.largestInteger(13579) == 97531
assert sol.largestInteger(24680) == 86420
assert sol.largestInteger(102030405) == 542030001
assert sol.largestInteger(987654321) == 987654321
assert sol.largestInteger(1000000000) == 1000000000
assert sol.largestInteger(999999999) == 999999999
assert sol.largestInteger(123456789) == 987654321
assert sol.largestInteger(908172635) == 986752031
