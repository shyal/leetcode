# URL: https://leetcode.com/problems/minimum-operations-to-make-a-special-number/description/?envType=problem-list-v2&envId=vn57k9wr
#
# 2844. Minimum Operations to Make a Special Number
#
# You are given a 0-indexed string num representing a non-negative integer.
#
# In one operation, you can pick any digit of num and delete it. Note that if you delete all the digits of num, num becomes 0.
#
# Return the minimum number of operations required to make num special.
#
# An integer x is considered special if it is divisible by 25.
#
# Example 1:
#
# Input: num = "2245047"
# Output: 2
# Explanation: Delete digits num[5] and num[6]. The resulting number is "22450" which is special since it is divisible by 25.
# It can be shown that 2 is the minimum number of operations required to get a special number.
#
# Example 2:
#
# Input: num = "2908305"
# Output: 3
# Explanation: Delete digits num[3], num[4], and num[6]. The resulting number is "2900" which is special since it is divisible by 25.
# It can be shown that 3 is the minimum number of operations required to get a special number.
#
# Example 3:
#
# Input: num = "10"
# Output: 1
# Explanation: Delete digit num[0]. The resulting number is "0" which is special since it is divisible by 25.
# It can be shown that 1 is the minimum number of operations required to get a special number.
#
# Constraints:
#
#     1 <= num.length <= 100
#     num only consists of digits '0' through '9'.
#     num does not contain any leading zeros.
#
# ---
# let's think of the brute force approach first.
# the bf approach is to test if num is divisible by 25
# if it is, return 0, else try removing 1 number (try all possibilities).
# if that doesn't work, then try removing two numbers (e.g using pairs)
# etc.
# The constraints are quite small, so it's doable, but not ideal.
# 
# now for a number to be divisible by 25, it's fair to say only the last 2 digits
# need to be a multiple of 25? that would be 00, 25, 50, 75
# this makes the problem much simpler: remove the least amount of numbers
# to end up with 00, 25, 50, 75 at the end of the number.
# so let's search for those numbers, from the back of the string.
# 2245047
# 0123456

# mu 0.17

def deletions(r: str, end: str) -> int
  ret count = len(r)
  j = r.find(end[1])
  if j != -1
    i = r.find(end[0], j + 1)
    if i != -1
      count = i - 1

class Solution
  def minimumOperations(num: str) -> int
    ret best = min(deletions(num[::-1], end) for end in ['00', '25', '50', '75'])
    if best == len num and '0' in num
      best = len num - 1


sol = Solution()

print(sol.minimumOperations('2245047'))  # 2

assert sol.minimumOperations('2245047') == 2
assert sol.minimumOperations('2908305') == 3
assert sol.minimumOperations('10') == 1
assert sol.minimumOperations('7') == 1
assert sol.minimumOperations('52') == 2
assert sol.minimumOperations('1' * 10) == 10
assert sol.minimumOperations('7000001') == 1
assert sol.minimumOperations('5555555') == 7
assert sol.minimumOperations('0') == 0
assert sol.minimumOperations('25') == 0
assert sol.minimumOperations('100') == 0
assert sol.minimumOperations('1' + '0' * 99) == 0
assert sol.minimumOperations('5050505050') == 0
assert sol.minimumOperations('9876543125') == 0
assert sol.minimumOperations('-25') == 0


# FAILED: walked away after 59m 26s; no working solution.
# Judge the move the defect is in as struggled, not clean. A move the code never reached gets no verdict.
