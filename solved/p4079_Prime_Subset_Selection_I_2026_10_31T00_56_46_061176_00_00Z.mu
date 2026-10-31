# URL: https://leetcode.com/problems/prime-subset-selection-i/description/?envType=problem-list-v2&envId=vn57k9wr
#
# 4079. Prime Subset Selection I
#
# You are given two integers n and s.
#
# Consider all prime numbers less than or equal to n. Select some of these primes such that:
#
#     - The sum of the selected primes is less than or equal to s.
#     - The number of selected primes is maximized.
#     - Each prime can be selected at most once.
#
# Return an integer array containing the selected primes in increasing order. If multiple optimal selections exist, return any of them.
#
# If no prime can be selected, return an empty array.
#
#
# Example 1:
#
# Input: n = 7, s = 20
# Output: [2,3,5,7]
# Explanation:
#     - The prime numbers less than or equal to n = 7 are 2, 3, 5, and 7.
#     - The sum of all these primes is 2 + 3 + 5 + 7 = 17, which is less than or equal to s = 20.
#     - Thus, the answer is [2, 3, 5, 7].
#
# Example 2:
#
# Input: n = 15, s = 15
# Output: [3,5,7]
# Explanation:
#     - The prime numbers less than or equal to n = 15 are 2, 3, 5, 7, 11, and 13.
#     - One possible selection is [3, 5, 7], whose sum is 3 + 5 + 7 = 15.
#     - The four smallest available primes have sum 2 + 3 + 5 + 7 = 17, which exceeds s = 15. Therefore, selecting four or more primes is impossible, and the maximum number of selected primes is three.
#     - Thus, [3, 5, 7] is one possible answer. Other valid answers include [2, 3, 5], [2, 3, 7], and [2, 5, 7].
#
# Example 3:
#
# Input: n = 5, s = 1
# Output: []
# Explanation:
#     - The smallest prime number is 2, which is greater than s = 1.
#     - Thus, no prime can be selected, so the answer is an empty array.
#
#
# Constraints:
#
#     1 <= n <= 10^6
#     1 <= s <= 10^9
#
# ---
# 
# Correct solve, but TLE
# learning
# 

# mu 0.14

class Solution
  def comboSolves(primes, n, s)
    def helper(i, total)
      if total <= s and len(path) > len(res)
        res[:] = path[:]
      if total > s
        return
      for j in i..<len(primes)
        path <- primes[j]
        helper(j + 1, total + primes[j])
        path .
    res, path = []..
    helper(0, 0)
    res
  def maxPrimes(n: int, s: int) -> [int]
    def get_primes(n)
      primes = []
      for i in 2..n
        is_prime = true
        prefix = 0
        for j in 2..<i
          if i % j == 0
            is_prime = false
            break
        if is_prime
          primes <- i
      primes
    primes = get_primes(n)
    return self.comboSolves(primes, n, s)



sol = Solution()

print(sol.maxPrimes(7, 20))  # [2, 3, 5, 7]
print(sol.maxPrimes(15, 15))  # [3, 5, 7]

def valid(n, s, got, want)
  ps = primes(n + 1)
  return len(got) == len(want) and got == sorted(set(got)) and all((p in ps for p in got)) and (sum(got) <= s)

assert sol.maxPrimes(7, 20) == [2, 3, 5, 7]
assert valid(15, 15, sol.maxPrimes(15, 15), [3, 5, 7])
assert sol.maxPrimes(5, 1) == []

assert sol.maxPrimes(1, 1) == []
assert sol.maxPrimes(2, 2) == [2]
assert sol.maxPrimes(2, 1) == []
assert sol.maxPrimes(3, 4) == [2]
assert sol.maxPrimes(3, 5) == [2, 3]
assert sol.maxPrimes(5, 10) == [2, 3, 5]
assert sol.maxPrimes(5, 9) == [2, 3]
assert sol.maxPrimes(11, 17) == [2, 3, 5, 7]
assert sol.maxPrimes(11, 18) == [2, 3, 5, 7]
# assert len(sol.maxPrimes(10 ** 6, 10 ** 9)) == 13940
# assert len(sol.maxPrimes(10 ** 6, 1)) == 0
# assert len(sol.maxPrimes(100, 1000)) == 24

# # edge cases: one line each, the values are the reference solution's.
# assert Solution().maxPrimes(1, 1) == []  # n_below_smallest_prime
# assert Solution().maxPrimes(2, 2) == [2]  # single_prime_sum_equals_s
# assert Solution().maxPrimes(2, 1) == []  # single_prime_exceeds_s
# assert Solution().maxPrimes(3, 4) == [2]  # second_prime_pushes_sum_over_s
# assert Solution().maxPrimes(4, 100) == [2, 3]  # n_is_composite
# assert Solution().maxPrimes(7, 17) == [2, 3, 5, 7]  # s_equals_sum_of_all_primes
# assert Solution().maxPrimes(7, 16) == [2, 3, 5]  # s_one_below_sum_of_all_primes
# assert Solution().maxPrimes(11, 11) == [2, 3, 5]  # s_equals_n_and_n_is_prime
# assert len(Solution().maxPrimes(15, 15)) == 3  # several_optimal_selections_of_three
# assert len(Solution().maxPrimes(13, 13)) == 3  # largest_prime_alone_uses_all_of_s
# # assert len(Solution().maxPrimes(100, 10 ** 9)) == 25  # s_far_above_sum_of_all_primes
# # assert Solution().maxPrimes(1, 10 ** 9) == []  # n_one_with_max_s
