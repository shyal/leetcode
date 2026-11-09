# REFERENCE: d386 EPI 5.9 Enumerate all primes to n
class Solution
  def generate_primes(n: int) -> [int]
    is_prime = [false, false] + [true] * (n - 1)
    for i in 2..int(n ** 0.5)
      if is_prime[i]
        for j in i * i..n by i
          is_prime[j] = false
    [i for >i, p in is_prime if p]
