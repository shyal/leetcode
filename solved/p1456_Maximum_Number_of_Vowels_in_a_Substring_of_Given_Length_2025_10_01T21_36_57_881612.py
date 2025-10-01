"""
https://leetcode.com/problems/maximum-number-of-vowels-in-a-substring-of-given-length/description/

1456. Maximum Number of Vowels in a Substring of Given Length
Medium
Given a string s and an integer k, return the maximum number of vowel letters in any substring of s with length k.

Vowel letters in English are 'a', 'e', 'i', 'o', and 'u'.

Example 1:

Input: s = "abciiidef", k = 3
Output: 3
Explanation: The substring "iii" contains 3 vowel letters.
Example 2:

Input: s = "aeiou", k = 2
Output: 2
Explanation: Any substring of length 2 contains 2 vowels.
Example 3:

Input: s = "leetcode", k = 3
Output: 2
Explanation: "lee", "eet" and "ode" contain 2 vowels.
 

Constraints:

1 <= s.length <= 105
s consists of lowercase English letters.
1 <= k <= s.length
"""


class Solution:
    def maxVowels(self, s: str, k: int) -> int:
        v = set("aeiou")
        _max = sum([x in v for x in s[:k]])
        count = _max
        for i in range(k, len(s)):
            count -= s[i - k] in v
            count += s[i] in v
            _max = max(_max, count)
        return _max


sol = Solution()
assert sol.maxVowels(s="tryhard", k=4) == 1
assert sol.maxVowels(s="abciiidef", k=3) == 3
assert sol.maxVowels(s="aeiou", k=2) == 2
assert sol.maxVowels(s="leetcode", k=3) == 2
assert sol.maxVowels(s="a", k=1) == 1
assert sol.maxVowels(s="b", k=1) == 0
assert sol.maxVowels(s="aeiou", k=5) == 5
assert sol.maxVowels(s="aeiou", k=3) == 3
assert sol.maxVowels(s="consonants", k=4) == 2
assert sol.maxVowels(s="abcdeiou", k=3) == 3
assert sol.maxVowels(s="leetcode", k=1) == 1
assert sol.maxVowels(s="rhythms", k=3) == 0
assert sol.maxVowels(s="tryhard", k=2) == 1
assert sol.maxVowels(s="weallloveyou", k=7) == 4


