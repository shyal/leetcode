# URL: https://leetcode.com/problems/longest-common-prefix-between-adjacent-strings-after-removals/description/?envType=problem-list-v2&envId=vn57k9wr
#
# 3598. Longest Common Prefix Between Adjacent Strings After Removals
#
# You are given an array of strings words. For each index i in the range [0, words.length - 1], perform the following steps:
#
# - Remove the element at index i from the words array.
# - Compute the length of the longest common prefix among all adjacent pairs in the modified array.
#
# Return an array answer, where answer[i] is the length of the longest common prefix between the adjacent pairs after removing the element at index i. If no adjacent pairs remain or if none share a common prefix, then answer[i] should be 0.
#
# Example 1:
#
# Input: words = ["jump","run","run","jump","run"]
# Output: [3,0,0,3,3]
#
# Explanation:
# - Removing index 0:
#   words becomes ["run", "run", "jump", "run"]
#   Longest adjacent pair is ["run", "run"] having a common prefix "run" (length 3)
# - Removing index 1:
#   words becomes ["jump", "run", "jump", "run"]
#   No adjacent pairs share a common prefix (length 0)
# - Removing index 2:
#   words becomes ["jump", "run", "jump", "run"]
#   No adjacent pairs share a common prefix (length 0)
# - Removing index 3:
#   words becomes ["jump", "run", "run", "run"]
#   Longest adjacent pair is ["run", "run"] having a common prefix "run" (length 3)
# - Removing index 4:
#   words becomes ["jump", "run", "run", "jump"]
#   Longest adjacent pair is ["run", "run"] having a common prefix "run" (length 3)
#
# Example 2:
#
# Input: words = ["dog","racer","car"]
# Output: [0,0,0]
#
# Explanation:
# - Removing any index results in an answer of 0.
#
# Constraints:
#
#     1 <= words.length <= 10^5
#     1 <= words[i].length <= 10^4
#     words[i] consists of lowercase English letters.
#     The sum of words[i].length is smaller than or equal 10^5.
#
# ---
# learning

# mu 0.17

class Solution
  def longestCommonPrefix(words: [str]) -> [int]
    n = len(words)
    adj = [len(commonprefix(pair)) for pair in zip(words, words[1:])]
    left = [0] + scan(max, adj, initial=0, type=list)
    right = scan(max, adj, reverse=true, initial=0, type=list) + [0]
    ret result = []
    for >i in words
      bridge = 0 < i < n - 1 ? len(commonprefix([words[i - 1], words[i + 1]])) : 0
      result.append(max(left[i], right[i + 1], bridge))


          
sol = Solution()

print(sol.longestCommonPrefix(['jump', 'run', 'run', 'jump', 'run']))  # [3,0,0,3,3]

assert sol.longestCommonPrefix(['jump', 'run', 'run', 'jump', 'run']) == [3, 0, 0, 3, 3]
assert sol.longestCommonPrefix(['dog', 'racer', 'car']) == [0, 0, 0]
assert sol.longestCommonPrefix(['a']) == [0]
assert sol.longestCommonPrefix(['ab', 'a']) == [0, 0]
assert sol.longestCommonPrefix(['test', 'test', 'test', 'test', 'test']) == [4, 4, 4, 4, 4]
assert sol.longestCommonPrefix(['a', 'ab', 'a', 'ab', 'a']) == [1, 1, 2, 1, 1]
assert sol.longestCommonPrefix(['x' * 10000, 'x' * 10000, 'x' * 10000]) == [10000, 10000, 10000]
assert sol.longestCommonPrefix(['abcde', 'abcdef', 'abxyz', 'abcmno']) == [2, 2, 5, 5]
assert sol.longestCommonPrefix(['a', 'b', 'c', 'd', 'e']) == [0, 0, 0, 0, 0]
assert sol.longestCommonPrefix(['flower', 'flow', 'flight']) == [2, 2, 4]
assert sol.longestCommonPrefix(['abc', 'abc']) == [0, 0]
assert sol.longestCommonPrefix(['abx', 'yz', 'aby']) == [0, 2, 0]
assert sol.longestCommonPrefix(['aa', 'aa', 'a', 'aa']) == [1, 1, 2, 2]
