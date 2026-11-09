"""
EPI 5.9 Enumerate all primes to n

Given an integer n, return every prime p with 2 <= p <= n, in
increasing order. Use the sieve of Eratosthenes.

Example 1:

Input: n = 18
Output: [2, 3, 5, 7, 11, 13, 17]

Example 2:

Input: n = 13
Output: [2, 3, 5, 7, 11, 13]
Explanation: n itself is in the result when n is prime.

Example 3:

Input: n = 1
Output: []

Constraints:

    0 <= n <= 10^6

    REQUIRED: O(n log log n) time, O(n) space. NO trial division,
    NO primes() helper.
"""


class Solution:
    def generate_primes(self, n: int) -> list[int]:
        pass


sol = Solution()

print(sol.generate_primes(18))  # [2, 3, 5, 7, 11, 13, 17]

# assert sol.generate_primes(18) == [2, 3, 5, 7, 11, 13, 17]
# assert sol.generate_primes(13) == [2, 3, 5, 7, 11, 13]
# assert sol.generate_primes(1) == []
# assert sol.generate_primes(0) == []
# assert sol.generate_primes(2) == [2]
# assert sol.generate_primes(3) == [2, 3]
# assert sol.generate_primes(4) == [2, 3]
# assert sol.generate_primes(25) == [2, 3, 5, 7, 11, 13, 17, 19, 23]
# assert sol.generate_primes(49) == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
# assert sol.generate_primes(100)[-3:] == [83, 89, 97] and len(sol.generate_primes(100)) == 25
# P = sol.generate_primes(10 ** 6)
# assert len(P) == 78498 and P[-1] == 999983
# assert P[:10] == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
# assert 999979 in P and 999981 not in P
