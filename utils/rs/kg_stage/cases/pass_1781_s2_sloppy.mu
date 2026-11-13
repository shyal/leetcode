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
# two loops with a running counter
# STAGE 1: pass
# STAGE 2 of 3 - the pseudocode. Write one comment line for each step in the solve below. Then run make solved.

# mu 0.17

class Solution
  def solve(x)
    # ans == 0
    # for i in rnage(len(s)
      # cnt = Counter[]
      # for j in range(i, len(s) + 1)
        # cnt[s[j]] ++
        # ans += max(cnt) - min(cnt)
    # return
    pass

sol = Solution()
