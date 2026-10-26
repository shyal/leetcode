# URL: https://leetcode.com/problems/sum-of-numbers-with-units-digit-k/description/?envType=problem-list-v2&envId=vn57k9wr
#
# 2310. Sum of Numbers With Units Digit K
#
# Given two integers num and k, consider a set of positive integers with the following properties:
#
# - The units digit of each integer is k.
# - The sum of the integers is num.
#
# Return the minimum possible size of such a set, or -1 if no such set exists.
#
# Note:
#
# - The set can contain multiple instances of the same integer, and the sum of an empty set is considered 0.
# - The units digit of a number is the rightmost digit of the number.
#
# Example 1:
#
# Input: num = 58, k = 9
# Output: 2
# Explanation:
# One valid set is [9,49], as the sum is 58 and each integer has a units digit of 9.
# Another valid set is [19,39].
# It can be shown that 2 is the minimum possible size of a valid set.
#
# Example 2:
#
# Input: num = 37, k = 2
# Output: -1
# Explanation:
# It is not possible to obtain a sum of 37 using only integers that have a units digit of 2.
#
# Example 3:
#
# Input: num = 0, k = 7
# Output: 0
# Explanation:
# The sum of an empty set is considered 0.
#
# Constraints:
#
#     0 <= num <= 3000
#     0 <= k <= 9
#
# ---
# 
# Brute force gets TLE
# LEETCODE: Accepted (101 ms, 19.7 MB)

# mu 0.13

class Solution
  def minimumNumbers(num: int, k: int) -> int
    if k == 0
      if num == 0
        return 0
      last_digit = to_digits(num)[-1]
      if last_digit == k
        return 1
      return -1
    arr = []
    v = k
    while v <= num
      arr <- v
      v += 10
    def helper(i, total, count)
      if total == num
        res = count
        return
      if total > num
        return
      if count > 10
        res = -1
      for j in 0..<len(arr)
        if res is None
          count += 1
          helper(j + 1, total + arr[j], count)
          count -= 1
    arr = arr[::-1]
    res = None
    helper(0, 0, 0)
    res or -1 if None

    


sol = Solution()

assert sol.minimumNumbers(947, 2) == -1
assert sol.minimumNumbers(4, 0) == -1
assert sol.minimumNumbers(0, 0) == 0
assert sol.minimumNumbers(58, 9) == 2
assert sol.minimumNumbers(37, 2) == -1
assert sol.minimumNumbers(0, 7) == 0
assert sol.minimumNumbers(1, 1) == 1
assert sol.minimumNumbers(10, 0) == 1
assert sol.minimumNumbers(3000, 0) == 1
assert sol.minimumNumbers(3000, 9) == 10
assert sol.minimumNumbers(19, 9) == 1
assert sol.minimumNumbers(20, 5) == 2
assert sol.minimumNumbers(15, 5) == 1
assert sol.minimumNumbers(11, 1) == 1
assert sol.minimumNumbers(29, 9) == 1
assert sol.minimumNumbers(3000, 1) == 10
assert sol.minimumNumbers(3000, 5) == 2
assert sol.minimumNumbers(7, 7) == 1
