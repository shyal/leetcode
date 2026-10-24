# URL: https://leetcode.com/problems/count-of-substrings-containing-every-vowel-and-k-consonants-i/description/?envType=problem-list-v2&envId=vn57k9wr
#
# 3305. Count of Substrings Containing Every Vowel and K Consonants I
#
# You are given a string word and a non-negative integer k.
#
# Return the total number of substrings of word that contain every vowel ('a', 'e', 'i', 'o', and 'u') at least once and exactly k consonants.
#
# Example 1:
#
# Input: word = "aeioqq", k = 1
# Output: 0
# Explanation:
# There is no substring with every vowel.
#
# Example 2:
#
# Input: word = "aeiou", k = 0
# Output: 1
# Explanation:
# The only substring with every vowel and zero consonants is word[0..4], which is "aeiou".
#
# Example 3:
#
# Input: word = "ieaouqqieaouqq", k = 1
# Output: 3
# Explanation:
# The substrings with every vowel and one consonant are:
# - word[0..5], which is "ieaouq".
# - word[6..11], which is "qieaou".
# - word[7..12], which is "ieaouq".
#
# Constraints:
#
#     5 <= word.length <= 250
#     word consists only of lowercase English letters.
#     0 <= k <= word.length - 5
#
# ---
# 
# 
# aeioqq
# 
# 
# 

# mu 0.12

class Solution
  def countOfSubstrings(word: str, k: int) -> int
    vowels = set(['a', 'e', 'i', 'o','u']) 
    ret count = 0
    for i in 0..<len(word)
      vowels_so_far = set([])
      consonants = 0
      for j in i..<len(word)
        if word[j] in vowels
          vowels_so_far.add(word[j])
        if word[j] not in vowels
          consonants += 1
        count += len vowels_so_far == len vowels and consonants == k
        if consonants > k
          break





sol = Solution()

# print(sol.countOfSubstrings('aeioqq', 1))  # 0
assert sol.countOfSubstrings('aeioqq', 1) == 0
assert sol.countOfSubstrings('aeiou', 0) == 1
assert sol.countOfSubstrings('ieaouqqieaouqq', 1) == 3
assert sol.countOfSubstrings('aeiou', 5) == 0
assert sol.countOfSubstrings('bcdfghjklmnpqrstvwxyz', 0) == 0
assert sol.countOfSubstrings('aeiouaeiouaeiou', 0) == 66
assert sol.countOfSubstrings('aeioubcdfg', 4) == 1
assert sol.countOfSubstrings('aeioubcdfg', 5) == 1
assert sol.countOfSubstrings('aeiou' * 50, 0) == 30381
assert sol.countOfSubstrings('aeioubcdfg' * 25, 5) == 601
