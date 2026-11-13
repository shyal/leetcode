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

# mu 0.17

class Solution
  def solve(x)
    pass

sol = Solution()
