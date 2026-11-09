# REFERENCE: d386 EPI 5.9 Enumerate all primes to n
class Solution:
    def generate_primes(self, n):
        is_prime = [False, False] + [True] * (n - 1)
        for i in range(2, int(n ** 0.5) + 1):
            if is_prime[i]:
                for j in range(i * i, n + 1, i):
                    is_prime[j] = False
        return [i for i, p in enumerate(is_prime) if p]
