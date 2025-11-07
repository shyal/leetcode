"""
URL: https://leetcode.com/problems/number-of-even-and-odd-bits/description/?envType=problem-list-v2&envId=vn57k9wr

2595. Number of Even and Odd 1-Bits

You are given a positive integer n.

In the binary representation of n, bits are indexed from right to left, starting at index 0.
That is, the rightmost bit is index 0 (even), the next is index 1 (odd), and so on.

Let even be the number of 1s at even-indexed positions.
Let odd be the number of 1s at odd-indexed positions.

Return an array [even, odd].

Example 1:

Input: n = 50
Binary: 110010 → indices from right:
0 (pos 5), 1 (pos 4), 0 (pos 3), 0 (pos 2), 1 (pos 1), 1 (pos 0)
1s at positions: 5, 4, 1 → even indices: 4 → count = 1
odd indices: 5, 1 → count = 2
Output: [1, 2]

Example 2:

Input: n = 2
Binary: 10 → 0 (pos 1), 1 (pos 0)
1 at position 1 (odd)
Output: [0, 1]


Constraints:

1 <= n <= 1000
"""


class Solution:
    def toBase(self, n, k):
        res = []
        while n:
            n, m = divmod(n, k)
            res = [m] + res
        return res

    def evenOddBit(self, n: int) -> List[int]:
        bits = self.toBase(n, 2)[::-1]
        even, odd = 0, 0
        for i, b in enumerate(bits):
            if i % 2 == 0 and b:
                even += 1
            elif i % 2 == 1 and b:
                odd += 1
        return [even, odd]


sol = Solution()

print(sol.evenOddBit(50))  # [1, 2]

assert sol.evenOddBit(50) == [1, 2]
assert sol.evenOddBit(2) == [0, 1]
assert sol.evenOddBit(1) == [1, 0]
assert sol.evenOddBit(3) == [1, 1]
assert sol.evenOddBit(4) == [1, 0]
assert sol.evenOddBit(5) == [2, 0]
assert sol.evenOddBit(6) == [1, 1]
assert sol.evenOddBit(7) == [2, 1]
assert sol.evenOddBit(8) == [0, 1]
assert sol.evenOddBit(15) == [2, 2]
assert sol.evenOddBit(16) == [1, 0]
assert sol.evenOddBit(17) == [2, 0]
assert sol.evenOddBit(32) == [0, 1]
assert sol.evenOddBit(512) == [0, 1]
assert sol.evenOddBit(1000) == [2, 4]
