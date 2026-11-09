"""
EPI 12.10 Compute all string decompositions

Given a string s and a list of strings words, all of the same length,
return the sorted list of every index i such that the substring of s
that starts at i is a concatenation of all the words, each used exactly
as many times as it appears in words, in any order.

Example 1:

Input: s = "catdogdogcat", words = ["cat", "dog"]
Output: [0, 6]
Explanation: "catdog" starts at 0 and "dogcat" starts at 6. "dogdog" at
index 3 uses "dog" twice and "cat" never.

Example 2:

Input: s = "aaaa", words = ["aa", "aa"]
Output: [0]

Example 3:

Input: s = "xabcab", words = ["ab", "ca"]
Output: [1]
Explanation: "abca" at index 1 is "ab" then "ca".

Constraints:

    1 <= len(s) <= 10^4
    1 <= len(words) <= 100
    1 <= len(words[i]) <= 10, and all the words have the same length.
    s and the words consist of lowercase letters.

    REQUIRED: O(N * m * n) time, where N is the length of s, m is the
    number of words and n is the length of each word.
"""


class Solution:
    def find_all_substrings(self, s: str, words: list[str]) -> list[int]:
        pass


sol = Solution()

print(sol.find_all_substrings("catdogdogcat", ["cat", "dog"]))  # [0, 6]

# assert sol.find_all_substrings("catdogdogcat", ["cat", "dog"]) == [0, 6]
# assert sol.find_all_substrings("aaaa", ["aa", "aa"]) == [0]
# assert sol.find_all_substrings("xabcab", ["ab", "ca"]) == [1]
# assert sol.find_all_substrings("a", ["a"]) == [0]
# assert sol.find_all_substrings("ab", ["abc"]) == []
# assert sol.find_all_substrings("aaaa", ["a", "a"]) == [0, 1, 2]
# assert sol.find_all_substrings("abab", ["ab", "ba"]) == []
# assert sol.find_all_substrings("aabba", ["ab", "ba"]) == [1]
# assert sol.find_all_substrings("abcabc", ["abc"]) == [0, 3]
# assert sol.find_all_substrings("catcat", ["cat", "cat", "cat"]) == []
# assert sol.find_all_substrings("xyzcatdog", ["dog", "cat"]) == [3]
# assert sol.find_all_substrings("ab" * 5000, ["ab", "ab"]) == list(range(0, 9997, 2))
# assert sol.find_all_substrings("a" * 10 ** 4, ["a"] * 100) == list(range(10 ** 4 - 99))
# assert sol.find_all_substrings("a" * 10 ** 4, ["a"] * 99 + ["b"]) == []
