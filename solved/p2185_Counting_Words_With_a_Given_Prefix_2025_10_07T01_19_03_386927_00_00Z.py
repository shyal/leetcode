"""
URL: https://leetcode.com/problems/counting-words-with-a-given-prefix/description/

2185. Counting Words With a Given Prefix

You are given an array of strings words and a string pref.

Return the number of strings in words that contain pref as a prefix.

A prefix of a string is a substring that occurs at the beginning of the string. A substring is a contiguous sequence of characters within a string.

Example 1:

Input: words = ["pay","attention","practice","attend"], pref = "at"
Output: 2
Explanation: The 2 strings that contain "at" as a prefix are: "attention" and "attend".

Example 2:

Input: words = ["leetcode","win","loops","success"], pref = "code"
Output: 0
Explanation: No string contains "code" as a prefix.

Constraints:

    1 <= words.length <= 100
    1 <= words[i].length, pref.length <= 100
    words[i] and pref consist of lowercase English letters.
"""


class Solution:
    def prefixCount(self, words: List[str], pref: str) -> int:
        return sum(x.startswith(pref) for x in words)


sol = Solution()

# print(sol.prefixCount(["pay", "attention", "practice", "attend"], "at"))  # 2

assert sol.prefixCount(["pay", "attention", "practice", "attend"], "at") == 2
assert sol.prefixCount(["leetcode", "win", "loops", "success"], "code") == 0
assert sol.prefixCount(["a"], "a") == 1
assert sol.prefixCount(["a"], "b") == 0
assert sol.prefixCount(["ab"], "a") == 1
assert sol.prefixCount(["a"], "ab") == 0
assert sol.prefixCount(["at", "at", "bat", "cat"], "at") == 2
assert sol.prefixCount(["attention", "attend", "at", "bat"], "at") == 3
assert sol.prefixCount(["attention", "attend", "at", "bat"], "att") == 2
assert sol.prefixCount(["leetcode", "win", "loops", "success"], "le") == 1
assert sol.prefixCount(["pay", "attention", "practice", "attend"], "p") == 2
assert sol.prefixCount(["hello"], "helloo") == 0
assert sol.prefixCount(["incat", "catty"], "cat") == 1
assert sol.prefixCount(["aaa", "aaa", "aaa"], "aa") == 3
assert sol.prefixCount(["abc", "def", "ghi"], "xyz") == 0
assert sol.prefixCount(["prefix", "pref", "pre", "pr", "p"], "p") == 5
