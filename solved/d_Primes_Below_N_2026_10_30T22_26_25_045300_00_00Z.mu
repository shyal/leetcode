# Given an integer n, return the primes less than n in increasing order.
# Make a table of n flags, all true. Set the flags at 0 and 1 to false.
# For each i from 2 upward whose flag is true, set the flag of every
# multiple of i below n to false, starting at 2i. For example with n = 20,
# i = 2 sets 4, 6, 8, 10, 12, 14, 16, 18 to false, then i = 3 sets 9 and
# 15 to false, and no later i changes a flag. The indices whose flag is
# true are the primes: [2, 3, 5, 7, 11, 13, 17, 19].
#
# Example 1:
#
# Input: n = 20
# Output: [2, 3, 5, 7, 11, 13, 17, 19]
#
# Example 2:
#
# Input: n = 5
# Output: [2, 3]
# Explanation: 4 is below 5 and is a multiple of 2.
#
# Example 3:
#
# Input: n = 2
# Output: []
# Explanation: no prime is less than 2.
#
# Constraints:
#
#     0 <= n <= 5 * 10^6
#
#     REQUIRED: O(n log log n). NO trial division per integer: testing
#     each of 5 * 10^6 integers against its own divisors is the failure
#     mode this drill exists to kill. NO call to the primes helper: this
#     drill is where you write it.
#
# This is the sieve of Eratosthenes.
#
# ---

# mu 0.14

class Solution
  def generatePrimes(n: int) -> [int]
    primes = table(2, fill=0) + table(n - 2, fill=1)
    for i in 2..<n
      if i * i < n and primes[i]
        for j in i * i..<n by i
          primes[j] = 0
    filter(0..n-1, by=primes)

sol = Solution()

print(sol.generatePrimes(20))  # [2, 3, 5, 7, 11, 13, 17, 19]

assert sol.generatePrimes(20) == [2, 3, 5, 7, 11, 13, 17, 19]
assert sol.generatePrimes(5) == [2, 3]
assert sol.generatePrimes(2) == []
assert sol.generatePrimes(0) == []
assert sol.generatePrimes(1) == []
assert sol.generatePrimes(3) == [2]
assert sol.generatePrimes(4) == [2, 3]
assert sol.generatePrimes(10) == [2, 3, 5, 7]
assert sol.generatePrimes(30) == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
assert sol.generatePrimes(100) == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
assert len(sol.generatePrimes(5 * 10 ** 6)) == 348513
