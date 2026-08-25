"""
URL: https://leetcode.com/problems/gcd-of-odd-and-even-sums/description/?envType=problem-list-v2&envId=vn57k9wr

3658. GCD of Odd and Even Sums

You are given an integer n. Your task is to compute the GCD (greatest common divisor) of two values:

- sumOdd: the sum of the smallest n positive odd numbers.
- sumEven: the sum of the smallest n positive even numbers.

Return the GCD of sumOdd and sumEven.

Example 1:

Input: n = 4
Output: 4
Explanation:
- Sum of the first 4 odd numbers sumOdd = 1 + 3 + 5 + 7 = 16
- Sum of the first 4 even numbers sumEven = 2 + 4 + 6 + 8 = 20
Hence, GCD(sumOdd, sumEven) = GCD(16, 20) = 4.

Example 2:

Input: n = 5
Output: 5
Explanation:
- Sum of the first 5 odd numbers sumOdd = 1 + 3 + 5 + 7 + 9 = 25
- Sum of the first 5 even numbers sumEven = 2 + 4 + 6 + 8 + 10 = 30
Hence, GCD(sumOdd, sumEven) = GCD(25, 30) = 5.

Constraints:

    1 <= n <= 10​​​​​​​00
"""


class Solution:
    def gcdOfOddEvenSums(self, n: int) -> int:
        sumOdd, sumEven = 0, 0
        for i in range(1, n * 2):
            if i % 2 == 0:
                sumEven += i
            else:
                sumOdd += 1
        return gcd(sumEven, sumOdd)


sol = Solution()

print(sol.gcdOfOddEvenSums(4))  # 4

assert sol.gcdOfOddEvenSums(4) == 4
assert sol.gcdOfOddEvenSums(5) == 5

assert sol.gcdOfOddEvenSums(1) == 1
assert sol.gcdOfOddEvenSums(2) == 2
assert sol.gcdOfOddEvenSums(3) == 3
assert sol.gcdOfOddEvenSums(10) == 10
assert sol.gcdOfOddEvenSums(100) == 100
assert sol.gcdOfOddEvenSums(999) == 999
assert sol.gcdOfOddEvenSums(1000) == 1000
