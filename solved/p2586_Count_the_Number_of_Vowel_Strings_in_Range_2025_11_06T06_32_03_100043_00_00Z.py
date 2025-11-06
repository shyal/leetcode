"""
URL: https://leetcode.com/problems/count-the-number-of-vowel-strings-in-range/description/?envType=problem-list-v2&envId=vn57k9wr

2586. Count the Number of Vowel Strings in Range

You are given a 0-indexed array of string words and two integers left and right.

A string is called a vowel string if it starts with a vowel character and ends with a vowel character where vowel characters are 'a', 'e', 'i', 'o', and 'u'.

Return the number of vowel strings words[i] where i belongs to the inclusive range [left, right].


Example 1:

Input: words = ["are","amy","u"], left = 0, right = 2
Output: 2
Explanation:
- "are" is a vowel string because it starts with 'a' and ends with 'e'.
- "amy" is not a vowel string because it does not end with a vowel.
- "u" is a vowel string because it starts with 'u' and ends with 'u'.
The number of vowel strings in the mentioned range is 2.

Example 2:

Input: words = ["hey","aeo","mu","ooo","artro"], left = 1, right = 4
Output: 3
Explanation:
- "aeo" is a vowel string because it starts with 'a' and ends with 'o'.
- "mu" is not a vowel string because it does not start with a vowel.
- "ooo" is a vowel string because it starts with 'o' and ends with 'o'.
- "artro" is a vowel string because it starts with 'a' and ends with 'o'.
The number of vowel strings in the mentioned range is 3.


Constraints:

    1 <= words.length <= 1000
    1 <= words[i].length <= 10
    words[i] consists of only lowercase English letters.
    0 <= left <= right < words.length
"""


class Solution:
    def vowelStrings(self, words: List[str], left: int, right: int) -> int:
        vowels = set("aeiou")
        count = 0
        for x in words[left : right + 1]:
            count += x[0] in vowels and x[-1] in vowels
        return count


sol = Solution()

print(sol.vowelStrings(["are", "amy", "u"], 0, 2))

assert sol.vowelStrings(["are", "amy", "u"], 0, 2) == 2
assert sol.vowelStrings(["hey", "aeo", "mu", "ooo", "artro"], 1, 4) == 3
assert sol.vowelStrings(["a"], 0, 0) == 1
assert sol.vowelStrings(["b"], 0, 0) == 0
assert sol.vowelStrings(["aa"], 0, 0) == 1
assert sol.vowelStrings(["ab"], 0, 0) == 0
assert sol.vowelStrings(["ba"], 0, 0) == 0
assert sol.vowelStrings(["bb"], 0, 0) == 0
assert sol.vowelStrings(["aeiou"], 0, 0) == 1
assert sol.vowelStrings(["abcde"], 0, 0) == 1
assert sol.vowelStrings(["bcd"], 0, 0) == 0
assert sol.vowelStrings(["a", "b", "u", "x"], 0, 3) == 2
assert sol.vowelStrings(["aaaaaaaaaa"], 0, 0) == 1
assert sol.vowelStrings(["aaaaaaaab"], 0, 0) == 0
assert sol.vowelStrings(["hey", "mu"], 0, 1) == 0
assert sol.vowelStrings(["u", "o", "i", "e", "a"], 0, 4) == 5
assert sol.vowelStrings(["xyz", "abc", "def"], 1, 2) == 0
assert sol.vowelStrings(["ae", "eo", "iu", "oa", "ui"], 0, 4) == 5
assert sol.vowelStrings(["a"], 0, 0) == 1
assert sol.vowelStrings(["z"], 0, 0) == 0
assert sol.vowelStrings(["are", "amy", "u"], 2, 2) == 1
assert sol.vowelStrings(["are", "amy", "u"], 1, 1) == 0
