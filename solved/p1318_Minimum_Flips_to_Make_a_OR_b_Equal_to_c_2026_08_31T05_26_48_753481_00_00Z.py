"""
URL: https://leetcode.com/problems/minimum-flips-to-make-a-or-b-equal-to-c/description/?envType=problem-list-v2&envId=vn57k9wr

1318. Minimum Flips to Make a OR b Equal to c

Given 3 positive numbers a, b and c. Return the minimum flips required in some bits of a and b to make (a OR b == c) (bitwise OR operation).
Flip operation consists of changing any single bit 1 to 0 or changing the bit 0 to 1 in their binary representation.

Example 1:

Input: a = 2, b = 6, c = 5
Output: 3
Explanation: After flips a = 1 , b = 4 , c = 5 such that (a OR b == c)

Example 2:

Input: a = 4, b = 2, c = 7
Output: 1

Example 3:

Input: a = 1, b = 2, c = 3
Output: 0

Constraints:

    1 <= a <= 10^9
    1 <= b <= 10^9
    1 <= c <= 10^9

---

a =  10
b = 110
-------
c = 101

So the idea is we need to minimize bit flips in a and b so that | results in c.

Currently

   10
| 110
-----
  110

Let's try xoring:

 10
110 ^
---
100

Let's try flipping the lowest bit:

 10
110 |
-----
101

So it's fairly clear that:

if we have a 1 in the result and two zeros in a and b, we need to set the bit of a or b to 1.
if we have a 0 in the result we need to flip both bits to 0.

Hmm ok let's try a slightly different approach. let's just or a and b:


   10
| 110
-----
  110

110 # a | b
101 # c


a =  10
b = 110
-------
c = 101

Nope.


0100
0010

0111

Solved. Yucky solution though. Nope. Failed tests on lc.


1000
0011

0101

Phew. Solved. Yucky solution.

"""


class Solution:

    def minFlips(self, a: int, b: int, c: int) -> int:
        min_flips = 0
        while a or b or c:
            if c & 1 == 1:
                zeroes = int(a & 1 == 0) * int(a != 0) + int(b & 1 == 0) * int(b != 0)
                if (a == 0 or b == 0) and zeroes == 1:
                    min_flips += 1
                if zeroes == 2 or (a == b == 0):
                    min_flips += 1
            elif c & 1 == 0:
                ones = int(a & 1 == 1) * int(a != 0) + int(b & 1 == 1) * int(b != 0)
                min_flips += ones
            a >>= 1
            b >>= 1
            c >>= 1
        return min_flips


sol = Solution()

print(sol.minFlips(2, 6, 5))  # 3

assert sol.minFlips(8, 3, 5) == 3
assert sol.minFlips(2, 6, 5) == 3
assert sol.minFlips(4, 2, 7) == 1
assert sol.minFlips(1, 2, 3) == 0

assert Solution().minFlips(0, 0, 0) == 0
assert Solution().minFlips(0, 0, 1) == 1
assert Solution().minFlips(1, 1, 0) == 2
assert Solution().minFlips(2**30, 2**30, 0) == 2
assert Solution().minFlips(2**30, 0, 2**30) == 0
assert Solution().minFlips(2**30 - 1, 2**30 - 1, 2**30 - 1) == 0
assert Solution().minFlips(2**30 - 1, 2**30 - 1, 0) == 60
assert Solution().minFlips(0, 2**30 - 1, 2**30 - 1) == 0
assert Solution().minFlips(123456789, 987654321, 555555555) == 23
assert Solution().minFlips(10, 10, 10) == 0
assert Solution().minFlips(10, 10, 0) == 4
assert Solution().minFlips(0, 0, 2**31 - 1) == 31
