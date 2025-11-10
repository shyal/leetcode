"""
URL: https://leetcode.com/problems/find-words-that-can-be-formed-by-characters/description/?envType=problem-list-v2&envId=vn57k9wr

1160. Find Words That Can Be Formed by Characters

You are given an array of strings words and a string chars.

A string is good if it can be formed by characters from chars (each character can only be used once for each word in words).

Return the sum of lengths of all good strings in words.

Example 1:

Input: words = ["cat","bt","hat","tree"], chars = "atach"
Output: 6
Explanation: The strings that can be formed are "cat" and "hat" so the answer is 3 + 3 = 6.

Example 2:

Input: words = ["hello","world","leetcode"], chars = "welldonehoneyr"
Output: 10
Explanation: The strings that can be formed are "hello" and "world" so the answer is 5 + 5 = 10.

Constraints:

    1 <= words.length <= 1000
    1 <= words[i].length, chars.length <= 100
    words[i] and chars consist of lowercase English letters.
"""


class Solution:
    def canBeUsed(self, a, b):
        return all(c in b and b[c] >= a[c] for c in a)

    def countCharacters(self, words: List[str], chars: str) -> int:
        chars = Counter(chars)
        res = 0
        for word in words:
            res += len(word) if self.canBeUsed(Counter(word), chars) else 0
        return res


sol = Solution()

print(sol.countCharacters(["cat", "bt", "hat", "tree"], "atach"))  # 6

assert sol.countCharacters(["cat", "bt", "hat", "tree"], "atach") == 6
assert sol.countCharacters(["hello", "world", "leetcode"], "welldonehoneyr") == 10
assert sol.countCharacters(["a"], "a") == 1
assert sol.countCharacters(["a"], "b") == 0
assert sol.countCharacters(["aa"], "aa") == 2
assert sol.countCharacters(["aa"], "a") == 0
assert sol.countCharacters(["ab", "ab"], "ab") == 4
assert sol.countCharacters(["abc"], "ab") == 0
assert sol.countCharacters([], "abc") == 0
assert sol.countCharacters([""], "abc") == 0
assert sol.countCharacters(["abc"], "") == 0
assert sol.countCharacters(["a", "b", "c"], "abc") == 3
assert sol.countCharacters(["xyz"], "abc") == 0
assert sol.countCharacters(["atach"], "atach") == 5
