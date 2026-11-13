# URL: https://leetcode.com/problems/sum-of-beauty-of-all-substrings/description/?envType=problem-list-v2&envId=vn57k9wr
#
# 1781. Sum of Beauty of All Substrings
#
# The beauty of a string is the difference in frequencies between the most frequent and least frequent characters.
#
# For example, the beauty of "abaacc" is 3 - 1 = 2.
#
# Given a string s, return the sum of beauty of all of its substrings.
#
# Example 1:
#
# Input: s = "aabcb"
# Output: 5
# Explanation: The substrings with non-zero beauty are ["aab","aabc","aabcb","abcb","bcb"], each with beauty equal to 1.
#
# Example 2:
#
# Input: s = "aabcbaa"
# Output: 17
#
# Constraints:
#
#     1 <= s.length <= 500
#     s consists of only lowercase English letters.
#
# ---
# STAGE 1 of 3 - the approach. Write it in plain English under this line. Then run make solved.
#
# the constraints are small, so we can simply generate all substrings with two nested loops
# build a counter of the substring, and sum the diff between the min and max frequencies,
# STAGE 1: pass
# STAGE 2 of 3 - the pseudocode. Write one comment line for each step in the solve below. Then run make solved.
# class Solution
#   def beautySum(s: str) -> int
#     # res = 0
#     # for i in len s
#       # cnt = counter
#       # for j in i to len s
#         # cnt[s[j]] += 1
#         # res += max(best, max(cnt.values()) - min(cnt.values()))
#     # return res
#     pass
# STAGE 2: pass
# STAGE 3 of 3 - the code. Replace each pseudocode line with code. Then run make solved.
# LEETCODE: Accepted (1552 ms, 19.2 MB)

# mu 0.17

class Solution
  def beautySum(s: str) -> int
    ret res = 0
    for >i in s
      cnt = counter()
      for j in i..<len s
        cnt[s[j]] += 1
        v = max(cnt.values()) - min(cnt.values())
        res += v

sol = Solution()

print(sol.beautySum('aabcb'))  # 5

assert sol.beautySum('aabcb') == 5
assert sol.beautySum('aabcbaa') == 17
assert sol.beautySum('a') == 0
assert sol.beautySum('aaaaa') == 0
assert sol.beautySum('abcde') == 0
assert sol.beautySum('zzzzzzzzzz') == 0
assert sol.beautySum('ababababab') == 20
assert sol.beautySum('a' * 500) == 0
assert sol.beautySum('abcdefghijklmnopqrstuvwxyz' * 19 + 'abc') == 107106
assert sol.beautySum('aabbccddeeffgghhiijj') == 126
assert sol.beautySum('abcabcabcabcabcabcabcabcabcabc') == 261
assert sol.beautySum('zxyzyx') == 6
assert sol.beautySum('a' * 250 + 'b' * 250) == 5208250
assert sol.beautySum('abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz') == 1350
