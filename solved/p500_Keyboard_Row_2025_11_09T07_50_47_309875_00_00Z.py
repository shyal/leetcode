"""
URL: https://leetcode.com/problems/keyboard-row/description/?envType=problem-list-v2&envId=vn57k9wr

500. Keyboard Row

Given an array of strings words, return the words that can be typed using letters of the alphabet on only one row of American keyboard like the image below.

Note that the strings are case-insensitive, both lowercased and uppercased of the same letter are treated as if they are at the same row.

In the American keyboard:

- the first row consists of the characters "qwertyuiop",

- the second row consists of the characters "asdfghjkl", and

- the third row consists of the characters "zxcvbnm".


Example 1:

Input: words = ["Hello","Alaska","Dad","Peace"]
Output: ["Alaska","Dad"]
Explanation: Both "a" and "A" are in the 2nd row of the American keyboard due to case insensitivity.

Example 2:

Input: words = ["omk"]
Output: []

Example 3:

Input: words = ["adsdf","sfd"]
Output: ["adsdf","sfd"]


Constraints:

- 1 <= words.length <= 20
- 1 <= words[i].length <= 100
- words[i] consists of English letters (both lowercase and uppercase).
"""


class Solution:
    def findWords(self, words: List[str]) -> List[str]:
        rows = [set("qwertyuiop"), set("asdfghjkl"), set("zxcvbnm")]
        res = []
        for word in words:
            for row in rows:
                rem = set(word.lower()) - row
                if not rem:
                    res.append(word)
                    break
        return res


sol = Solution()

# print(sol.findWords(["Hello", "Alaska", "Dad", "Peace"]))  # ["Alaska","Dad"]

assert sol.findWords(["Hello", "Alaska", "Dad", "Peace"]) == ["Alaska", "Dad"]
assert sol.findWords(["omk"]) == []
assert sol.findWords(["adsdf", "sfd"]) == ["adsdf", "sfd"]
assert sol.findWords([]) == []
assert sol.findWords(["a"]) == ["a"]
assert sol.findWords(["A"]) == ["A"]
assert sol.findWords(["ab"]) == []
assert sol.findWords(["qwertyuiop"]) == ["qwertyuiop"]
assert sol.findWords(["QWERTYUIOP"]) == ["QWERTYUIOP"]
assert sol.findWords(["asdfghjkl"]) == ["asdfghjkl"]
assert sol.findWords(["zxcvbnm"]) == ["zxcvbnm"]
assert sol.findWords(["qaz"]) == []
assert sol.findWords(["QaZ"]) == []
assert sol.findWords(["aaa"]) == ["aaa"]
assert sol.findWords(["AaA"]) == ["AaA"]
assert sol.findWords(["pop"]) == ["pop"]
assert sol.findWords(["bob"]) == []
assert sol.findWords(["Alaska", "ALASKA", "alasKA"]) == ["Alaska", "ALASKA", "alasKA"]
assert sol.findWords(["hello", "world", "foo", "bar"]) == []
assert sol.findWords(["q", "w", "e", "r", "t", "y", "u", "i", "o", "p"]) == [
    "q",
    "w",
    "e",
    "r",
    "t",
    "y",
    "u",
    "i",
    "o",
    "p",
]
