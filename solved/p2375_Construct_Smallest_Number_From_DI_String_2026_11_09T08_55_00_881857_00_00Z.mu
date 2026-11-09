# URL: https://leetcode.com/problems/construct-smallest-number-from-di-string/description/?envType=problem-list-v2&envId=vn57k9wr
#
# 2375. Construct Smallest Number From DI String
#
# You are given a 0-indexed string pattern of length n consisting of the characters 'I' meaning increasing and 'D' meaning decreasing.
#
# A 0-indexed string num of length n + 1 is created using the following conditions:
#
# - num consists of the digits '1' to '9', where each digit is used at most once.
# - If pattern[i] == 'I', then num[i] < num[i + 1].
# - If pattern[i] == 'D', then num[i] > num[i + 1].
#
# Return the lexicographically smallest possible string num that meets the conditions.
#
# Example 1:
#
# Input: pattern = "IIIDIDDD"
# Output: "123549876"
# Explanation:
# At indices 0, 1, 2, and 4 we must have that num[i] < num[i+1].
# At indices 3, 5, 6, and 7 we must have that num[i] > num[i+1].
# Some possible values of num are "245639871", "135749862", and "123849765".
# It can be proven that "123549876" is the smallest possible num that meets the conditions.
# Note that "123414321" is not possible because the digit '1' is used more than once.
#
# Example 2:
#
# Input: pattern = "DDD"
# Output: "4321"
# Explanation:
# Some possible values of num are "9876", "7321", and "8742".
# It can be proven that "4321" is the smallest possible num that meets the conditions.
#
# Constraints:
#
#     1 <= pattern.length <= 8
#     pattern consists of only the letters 'I' and 'D'.
#
# ---
# LEETCODE: Accepted (1 ms, 19.4 MB)

# mu 0.16

class Solution
  def smallestNumber(pattern: str) -> str
    remaining = set(1..9)
    ret res = ''
    path = []
    seen = set([])
    {
      i ->
        if len path == len(pattern) + 1
          res = ''.join([str(x) for x in path])
          return true
        for n in 1..9
          if i == 0 or (i > 0 and (pattern[i-1] == 'I' and n > path[-1] or pattern[i-1] == 'D' and n < path[-1])) and n not in seen
            seen.add(n)
            path <- n
            if mu(i + 1)
              return true
            path .
            seen.discard(n)
    }(0)

sol = Solution()

print(sol.smallestNumber('IIIDIDDD'))  # "123549876"

assert sol.smallestNumber('IIIDIDDD') == '123549876'
assert sol.smallestNumber('DDD') == '4321'
assert sol.smallestNumber('I') == '12'
assert sol.smallestNumber('D') == '21'
assert sol.smallestNumber('IIIIIIII') == '123456789'
assert sol.smallestNumber('DDDDDDDD') == '987654321'
assert sol.smallestNumber('IDIDIDID') == '132547698'
assert sol.smallestNumber('DIDIDIDI') == '214365879'
assert sol.smallestNumber('IIIIIDDD') == '123459876'
assert sol.smallestNumber('DDDDDIID') == '654321798'
assert sol.smallestNumber('IIDDDIII') == '126543789'
assert sol.smallestNumber('DIDDDIII') == '216543789'
assert sol.smallestNumber('IDDDDDDD') == '198765432'
assert sol.smallestNumber('IIIIIIII') == '123456789'
