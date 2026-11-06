# URL: https://leetcode.com/problems/find-all-anagrams-in-a-string/description/?envType=problem-list-v2&envId=vn57k9wr
#
# 438. Find All Anagrams in a String
#
# Given two strings s and p, return an array of all the start indices of p's anagrams in s. You may return the answer in any order.
#
# Example 1:
#
# Input: s = "cbaebabacd", p = "abc"
# Output: [0,6]
# Explanation:
# The substring with start index = 0 is "cba", which is an anagram of "abc".
# The substring with start index = 6 is "bac", which is an anagram of "abc".
#
# Example 2:
#
# Input: s = "abab", p = "ab"
# Output: [0,1,2]
# Explanation:
# The substring with start index = 0 is "ab", which is an anagram of "ab".
# The substring with start index = 1 is "ba", which is an anagram of "ab".
# The substring with start index = 2 is "ab", which is an anagram of "ab".
#
# Constraints:
#
#     1 <= s.length, p.length <= 3 * 10^4
#     s and p consist of lowercase English letters.
#
# ---
# LEETCODE: Accepted (1042 ms, 19.8 MB)

# mu 0.16

class Solution
  def findAnagrams(s: str, p: str) -> [int]
    if not s and not p
      return [0]
    ret res = []
    left = 0
    orig = Counter(p)
    count = Counter()
    for >i, c in s
      count[c] += 1
      while count > orig
        count[s[left]] -= 1
        if count[s[left]] == 0
          del count[s[left]]
        left += 1
      if count == orig
        res <- left


sol = Solution()

print(sol.findAnagrams('cbaebabacd', 'abc'))  # [0,6]

assert sol.findAnagrams('cbaebabacd', 'abc') == [0, 6]
assert sol.findAnagrams('abab', 'ab') == [0, 1, 2]
assert Solution().findAnagrams('', '') == [0]
assert Solution().findAnagrams('a', 'a') == [0]
assert Solution().findAnagrams('a', 'b') == []
assert Solution().findAnagrams('aaaaa', 'aa') == [0, 1, 2, 3]
assert Solution().findAnagrams('abcde', 'edcba') == [0]
assert Solution().findAnagrams('abcabcabc', 'abc') == [0, 1, 2, 3, 4, 5, 6]
assert Solution().findAnagrams('ababababab', 'aab') == [0, 2, 4, 6]
assert Solution().findAnagrams('zzzzzzzzzz', 'zz') == [0, 1, 2, 3, 4, 5, 6, 7, 8]
assert Solution().findAnagrams('a' * 30000, 'a' * 30000) == [0]
assert Solution().findAnagrams('a' * 29999 + 'b', 'a' * 30000) == []
