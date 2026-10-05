"""
URL: https://leetcode.com/problems/minimize-xor/description/?envType=problem-list-v2&envId=vn57k9wr

2429. Minimize XOR

Given two positive integers num1 and num2, find the positive integer x such that:

- x has the same number of set bits as num2, and
- The value x XOR num1 is minimal.

Note that XOR is the bitwise XOR operation.

Return the integer x. The test cases are generated such that x is uniquely determined.

The number of set bits of an integer is the number of 1's in its binary representation.

Example 1:

Input: num1 = 3, num2 = 5
Output: 3
Explanation:
The binary representations of num1 and num2 are 0011 and 0101, respectively.
The integer 3 has the same number of set bits as num2, and the value 3 XOR 3 = 0 is minimal.

Example 2:

Input: num1 = 1, num2 = 12
Output: 3
Explanation:
The binary representations of num1 and num2 are 0001 and 1100, respectively.
The integer 3 has the same number of set bits as num2, and the value 3 XOR 1 = 2 is minimal.

Constraints:

    1 <= num1, num2 <= 10^9
---
num1 = 11, num2 = 101
x = 11


Hmm i tried using all permuations of bits, i.e brute force, and i'm not getting
the correct results. Ok now the brute force version works.

let's take num1 = 15, num2 = 1

num1 is 0b1111, and num2 is 0b1

The problem with this question is that the examples are genuinely terrible..... really not helpful at all.



let's try 7 and 8
num1 0111
num2 1000

again... completely useless numbers... not sure how i'm supposed to solve this when i'm not even provided with examples
i can work with

Leetcode hints are:
- To arrive at a small xor, try to turn off some bits from num1
- If there are still left bits to set, try to set them from the least significant bit

which restricts the search space. Good.

num1 = 0b11001
num2 = 0b101
Solution =0b11000

ok so a solution might be to just turn the LSBs of num1
until we get the same number of bits as we do in num2..


0b110110
0b1100

solution 0b110000

can't remember how to unset the LSB though.. that definitely calls for a drill. ok i'm out of time. Dropping this.

LEETCODE: Time Limit Exceeded (3/280 cases)
"""


# mu 0.7
# def minimizeXor(num1: int, num2: int) -> int
#   print(bin(num1))
#   print(bin(num2))
#   _min = inf
#   d = [0] * len(to_digits(num1, base=2)) + to_digits(num2, base=2)
#   d.sort()
#   res = 0
#   for p in permutations(d)
#     x = to_int(p, base=2)
#     if x ^ num1 < _min
#       _min = x ^ num1
#       res = x
#   res
#
# # def minimizeXor(num1: int, num2: int) -> int
# #   num_ones = x -> sum( x == 1 for x in to_digits(x))
# #   x = num1
# #   while num_ones(x) > num_ones(num2)

from math import inf


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


def to_int(digits, reverse=False, base=10):
    out = 0
    for d in digits[::-1] if reverse else digits:
        out = out * base + d
    return out


class Solution:
    def minimizeXor(self, num1: int, num2: int) -> int:
        print(bin(num1))
        print(bin(num2))
        _min = inf
        d = [0] * len(to_digits(num1, base=2)) + to_digits(num2, base=2)
        d.sort()
        res = 0
        for p in permutations(d):
            x = to_int(p, base=2)
            if x ^ num1 < _min:
                _min = x ^ num1
                res = x
        return res


sol = Solution()
assert sol.minimizeXor(3, 5) == 3
assert sol.minimizeXor(1, 12) == 3
assert sol.minimizeXor(0, 1) == 1
assert sol.minimizeXor(1, 0) == 0
assert sol.minimizeXor(0, 0) == 0
assert sol.minimizeXor(15, 15) == 15
assert sol.minimizeXor(15, 1) == 8
assert sol.minimizeXor(1, 15) == 15
assert sol.minimizeXor(7, 8) == 4
assert sol.minimizeXor(8, 7) == 11
