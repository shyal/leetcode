# REFERENCE: d316 Primes Below N
class Solution:
    def generatePrimes(self, n):
        primes = [0, 0] + [1] * (n - 2)
        for i in range(2, n):
            for j in range(2 * i, n * primes[i], i):
                primes[j] = 0
        return [i for i in range(n) if primes[i]]
