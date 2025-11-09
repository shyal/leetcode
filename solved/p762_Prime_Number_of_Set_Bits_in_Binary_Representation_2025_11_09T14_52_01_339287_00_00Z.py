"""
URL: https://leetcode.com/problems/prime-number-of-set-bits-in-binary-representation/description/?envType=problem-list-v2&envId=vn57k9wr

762. Prime Number of Set Bits in Binary Representation

Given two integers left and right, return the count of numbers in the inclusive range [left, right] having a prime number of set bits in their binary representation.

Recall that the number of set bits an integer has is the number of 1's present when written in binary.

- For example, 21 written in binary is 10101, which has 3 set bits.


Example 1:

Input: left = 6, right = 10
Output: 4
Explanation:
6 -> 110 (2 set bits, 2 is prime)
7 -> 111 (3 set bits, 3 is prime)
8 -> 1000 (1 set bit, 1 is not prime)
9 -> 1001 (2 set bits, 2 is prime)
10 -> 1010 (2 set bits, 2 is prime)
4 numbers have a prime number of set bits.

Example 2:

Input: left = 10, right = 15
Output: 5
Explanation:
10 -> 1010 (2 set bits, 2 is prime)
11 -> 1011 (3 set bits, 3 is prime)
12 -> 1100 (2 set bits, 2 is prime)
13 -> 1101 (3 set bits, 3 is prime)
14 -> 1110 (3 set bits, 3 is prime)
15 -> 1111 (4 set bits, 4 is not prime)
5 numbers have a prime number of set bits.


Constraints:

    1 <= left <= right <= 10^6
    0 <= right - left <= 10^4
"""


class Solution:
    def toBase(self, n, k=2):
        res = []
        while n:
            n, m = divmod(n, k)
            res = [m] + res
        return res

    @cache
    def isPrime(self, i):
        if i == 1:
            return False
        for j in range(2, i):
            if i % j == 0:
                return False
        return True

    def countPrimeSetBits(self, left: int, right: int) -> int:
        res = 0
        for i in range(left, right + 1):
            set_bits = sum(b == 1 for b in self.toBase(i))
            if self.isPrime(set_bits):
                res += 1
        return res


sol = Solution()

assert sol.countPrimeSetBits(6, 10) == 4
assert sol.countPrimeSetBits(10, 15) == 5
assert sol.countPrimeSetBits(1, 1) == 0
assert sol.countPrimeSetBits(1, 2) == 0
assert sol.countPrimeSetBits(2, 3) == 1
assert sol.countPrimeSetBits(3, 3) == 1
assert sol.countPrimeSetBits(4, 5) == 1
assert sol.countPrimeSetBits(8, 8) == 0
assert sol.countPrimeSetBits(15, 16) == 0
assert sol.countPrimeSetBits(31, 31) == 1
assert sol.countPrimeSetBits(1000000, 1000000) == 1
assert sol.countPrimeSetBits(1, 3) == 1
assert sol.countPrimeSetBits(842, 842) == 1
