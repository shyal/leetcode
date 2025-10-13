"""
URL: https://leetcode.com/problems/sort-characters-by-frequency/description/

451. Sort Characters By Frequency

Given a string s, sort it in decreasing order based on the frequency of the characters. The frequency of a character is the number of times it appears in the string.

Return the sorted string. If there are multiple answers, return any of them.

Example 1:

Input: s = "tree"
Output: "eert"
Explanation: 'e' appears twice while 'r' and 't' both appear once.
So 'e' must appear before both 'r' and 't'. Therefore "eetr" is also a valid answer.

Example 2:

Input: s = "cccaaa"
Output: "cccaaa"
Explanation: 'c' and 'a' both appear three times.
"aaaccc" is also a valid answer.
Note that "cacaca" is incorrect, as the same characters must be together.

Example 3:

Input: s = "Aabb"
Output: "bbAa"
Explanation: "bbaA" is also a valid answer.
Note that 'A' and 'a' are treated as two different characters.

Constraints:

    1 <= s.length <= 5e5
    s consists of uppercase and lowercase English letters and digits.
"""


class Solution:
    def frequencySort(self, s: str) -> str:
        c = list(dict(Counter(s)).items())
        c.sort(key=lambda x: x[1], reverse=True)
        return "".join([x[0] * x[1] for x in c])


sol = Solution()

# print(sol.frequencySort("tree"))  # "eert"

assert sol.frequencySort("tree") == "eetr"
assert sol.frequencySort("cccaaa") == "cccaaa"
assert sol.frequencySort("Aabb") == "bbAa"
assert sol.frequencySort("a") == "a"
assert sol.frequencySort("aaa") == "aaa"
assert sol.frequencySort("abc") == "abc"
assert sol.frequencySort("cba") == "cba"
