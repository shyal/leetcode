# URL: https://leetcode.com/problems/integer-replacement/description/?envType=problem-list-v2&envId=vn57k9wr
#
# 397. Integer Replacement
#
# Given a positive integer n, you can apply one of the following operations:
#
# 1. If n is even, replace n with n / 2.
# 2. If n is odd, replace n with either n + 1 or n - 1.
#
# Return the minimum number of operations needed for n to become 1.
#
# Example 1:
#
# Input: n = 8
# Output: 3
# Explanation: 8 -> 4 -> 2 -> 1
#
# Example 2:
#
# Input: n = 7
# Output: 4
# Explanation: 7 -> 8 -> 4 -> 2 -> 1
# or 7 -> 6 -> 3 -> 2 -> 1
#
# Example 3:
#
# Input: n = 4
# Output: 2
#
# Constraints:
#
#     1 <= n <= 2^31 - 1
#
# ---
# 15 -> 14 -> 7 -> 6 -> 3 -> 2 -> 1
#       1     2    3    4    5    6
# 15 -> 16 -> 8 -> 4 -> 2 -> 1 
#       1     2    3    4    5 
# 
# struggled a bit with anaytical approach, then the top comment in the discussion was "BFS". I tried it, and solved the problem is a minute.
# LEETCODE: Accepted (31 ms, 20.5 MB)

# mu 0.15

class Solution
  def integerReplacement(n: int) -> int
    is_power_of_two = n -> n & (n - 1) == 0
    q = deque([(n, 0)])
    while q
      num, dist = q.popleft()
      if num == 1
        return dist
      if even num
        q <- (num // 2, dist + 1)
      else
        q <- (num + 1, dist + 1)
        q <- (num - 1, dist + 1)
        

sol = Solution()

print(sol.integerReplacement(8))  # 3

assert sol.integerReplacement(8) == 3
assert sol.integerReplacement(7) == 4
assert sol.integerReplacement(4) == 2
assert sol.integerReplacement(1) == 0
assert sol.integerReplacement(2) == 1
assert sol.integerReplacement(3) == 2
assert sol.integerReplacement(15) == 5
assert sol.integerReplacement(16) == 4
assert sol.integerReplacement(1023) == 11
assert sol.integerReplacement(1024) == 10
assert sol.integerReplacement(2 ** 31 - 1) == 32
assert sol.integerReplacement(999999) == 25
assert sol.integerReplacement(1000000) == 24
assert sol.integerReplacement(6) == 3
assert sol.integerReplacement(5) == 3
