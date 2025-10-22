"""
URL: https://leetcode.com/problems/word-break/description/

139. Word Break

Given a string s and a dictionary of strings wordDict, return true if s can be segmented into a space-separated sequence of one or more dictionary words.

Note that the same word in the dictionary may be reused multiple times in the segmentation.


Example 1:

Input: s = "leetcode", wordDict = ["leet","code"]
Output: true
Explanation: Return true because "leetcode" can be segmented as "leet code".

Example 2:

Input: s = "applepenapple", wordDict = ["apple","pen"]
Output: true
Explanation: Return true because "applepenapple" can be segmented as "apple pen apple".
Note that you are allowed to reuse a dictionary word.

Example 3:

Input: s = "catsandog", wordDict = ["cats","dog","sand","and","cat"]
Output: false


Constraints:

        1 <= s.length <= 300
        1 <= wordDict.length <= 1000
        1 <= wordDict[i].length <= 20
        s and wordDict[i] consist of only lowercase English letters.
        All the strings of wordDict are unique.

---

This is likely a backtracking problem.
We iterate over all the words, and check if s starts
with the word. If it does, we explore the rest of the string
(doing the same). If no words match we backtrack.

Ok this seems to work, but i've hit a TLE. So a couple of optimizations
are:

- use indices instead of substrings
- sort wordDict by reverse length

Solved!

"""


class Solution:
    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        @cache
        def dp(i):
            if len(s) == i:
                return True
            for w in wordDict:
                if s[i:].startswith(w):
                    if dp(i + len(w)):
                        return True
            return False

        s_letters = set(s)
        words_letters = set(chain(*wordDict))
        if s_letters - words_letters != set([]):
            return False

        wordDict.sort(key=len, reverse=True)

        return dp(0)


sol = Solution()

res = sol.wordBreak(s="leetcode", wordDict=["leet", "code"])
assert res == True

res = sol.wordBreak(s="applepenapple", wordDict=["apple", "pen"])
assert res == True

res = sol.wordBreak(s="catsandog", wordDict=["cats", "dog", "sand", "and", "cat"])
assert res == False

res = sol.wordBreak(
    s="aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaab",
    wordDict=[
        "a",
        "aa",
        "aaa",
        "aaaa",
        "aaaaa",
        "aaaaaa",
        "aaaaaaa",
        "aaaaaaaa",
        "aaaaaaaaa",
        "aaaaaaaaaa",
    ],
)
assert res == False

assert sol.wordBreak("bb", ["a", "b", "bbb", "bbbb"]) == True
