# URL: https://leetcode.com/problems/short-encoding-of-words/description/?envType=problem-list-v2&envId=vn57k9wr
#
# 820. Short Encoding of Words
#
# A valid encoding of an array of words is any reference string s and array of indices indices such that:
#
# - words.length == indices.length
# - The reference string s ends with the '#' character.
# - For each index indices[i], the substring of s starting from indices[i] and up to (but not including) the next '#' character is equal to words[i].
#
# Given an array of words, return the length of the shortest reference string s possible of any valid encoding of words.
#
# Example 1:
#
# Input: words = ["time", "me", "bell"]
# Output: 10
# Explanation: A valid encoding would be s = "time#bell#" and indices = [0, 2, 5].
# words[0] = "time", the substring of s starting from indices[0] = 0 to the next '#' is underlined in "time#bell#"
# words[1] = "me", the substring of s starting from indices[1] = 2 to the next '#' is underlined in "ti(me)#bell#"
# words[2] = "bell", the substring of s starting from indices[2] = 5 to the next '#' is underlined in "time#(bell)#"
#
# Example 2:
#
# Input: words = ["t"]
# Output: 2
# Explanation: A valid encoding would be s = "t#" and indices = [0].
#
# Constraints:
#
#     1 <= words.length <= 2000
#     1 <= words[i].length <= 7
#     words[i] consists of only lowercase letters.
#
# ---
# LEETCODE: Accepted (6875 ms, 19.5 MB)

# mu 0.13

class Solution
  def minimumLengthEncoding(words: [str]) -> int
    contained = table(len(words), fill=False)
    for i, j in pairs(len(words))
      if i != j
        if (not contained[j]) and len(words[j]) <= len(words[i])
          if words[i].endswith(words[j])
            contained[j] = True
        if (not contained[j]) and len(words[i]) <= len(words[j])
          if words[j].endswith(words[i])
            contained[i] = True
    len('#'.join([x for >i, x in words if not contained[i]]) + '#')

sol = Solution()

assert sol.minimumLengthEncoding(["feipyxx","e"]) == 10
assert sol.minimumLengthEncoding(['time', 'me', 'bell']) == 10
assert sol.minimumLengthEncoding(['t']) == 2
assert sol.minimumLengthEncoding(['a'] * 2000) == 2
assert sol.minimumLengthEncoding(['abc', 'bc', 'c']) == 4 # abc#
assert sol.minimumLengthEncoding(['abc', 'def', 'ghi']) == 12
assert sol.minimumLengthEncoding(['a', 'aa', 'aaa', 'aaaa']) == 5
assert sol.minimumLengthEncoding(['xyz', 'yz', 'z', 'xyz']) == 4
assert sol.minimumLengthEncoding(['apple', 'ple', 'le', 'e']) == 6
assert sol.minimumLengthEncoding(['a' * 7, 'b' * 7, 'c' * 7]) == 24
assert sol.minimumLengthEncoding(['a' * 7, 'a' * 6, 'a' * 5]) == 8
assert sol.minimumLengthEncoding(['abcde', 'bcde', 'cde', 'de', 'e']) == 6
assert sol.minimumLengthEncoding(['z' * 7] * 2000) == 8
assert sol.minimumLengthEncoding(['a', 'b', 'c', 'd', 'e', 'f', 'g']) == 14
assert sol.minimumLengthEncoding(['abc', 'def', 'ef', 'f']) == 8
