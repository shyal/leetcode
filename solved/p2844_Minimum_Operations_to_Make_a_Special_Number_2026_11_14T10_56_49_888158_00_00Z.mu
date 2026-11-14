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
# STAGE 1 of 3 - the approach. Write it in plain English under this line. Then run make solved.
#
# LEETCODE: Accepted (4 ms, 19 MB)

# mu 0.18

# 2245047
# 0123456
#    xx

class Solution
  def from_end(suffix, num)
    ret indices = []
    for <i, c in num
      if not indices
        if c == suffix[1]
          indices <- i
      elif c == suffix[0]
        indices <- i
        break
  
  def count_deletions(ind, num)
    n = len num
    if len ind == 2
      rem = n - 1 - ind[0]
      rem += ind[0] - ind[1] - 1
      return rem
    inf
    
  def minimumOperations(num: str) -> int
    n = len num
    res = inf
    for cand in ['50', '00', '25', '75']
      ind = self.from_end(cand, num)
      rem = self.count_deletions(ind, num)
      res = min(res, rem)
    # special case, if there's a 0:
    if res == inf
      if num.count('0') == 1
        return n - 1
    res or n if inf

sol = Solution()

assert sol.from_end('50', '5050505050') == [9, 8]
assert sol.count_deletions([9, 8], '5050505050') == 0
assert sol.minimumOperations('10') == 1
assert sol.minimumOperations('0') == 0
assert sol.minimumOperations('1' + '0' * 99) == 0
assert sol.minimumOperations('9876543125') == 0
assert sol.minimumOperations('5555555') == 7
assert sol.minimumOperations('7000001') == 1
assert sol.minimumOperations('7') == 1
assert sol.minimumOperations('52') == 2
assert sol.minimumOperations('1' * 10) == 10
assert sol.minimumOperations('-25') == 0
assert sol.minimumOperations('25') == 0
assert sol.minimumOperations('5050505050') == 0
assert sol.minimumOperations('100') == 0
assert sol.from_end('50', '2245047') == [4, 3]
assert sol.count_deletions([4, 3], '2245047') == 2
assert sol.from_end('00', '2908305') == [5, 2]
assert sol.count_deletions([5, 2], '2908305') == 3
assert sol.minimumOperations('2245047') == 2
assert sol.minimumOperations('2908305') == 3
