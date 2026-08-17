"""
URL: https://leetcode.com/problems/count-the-number-of-consistent-strings/description/?envType=problem-list-v2&envId=vn57k9wr

1684. Count the Number of Consistent Strings

You are given a string allowed consisting of distinct characters and an array
of strings words. A string is consistent if all characters in the string
appear in the string allowed.

Return the number of consistent strings in the array words.


Example 1:

Input: allowed = "ab", words = ["ad","bd","aaab","baa","badab"]
Output: 2
Explanation: Strings "aaab" and "baa" are consistent since they only contain
characters 'a' and 'b'.

Example 2:

Input: allowed = "abc", words = ["a","b","c","ab","ac","bc","abc"]
Output: 7
Explanation: All strings are consistent.

Example 3:

Input: allowed = "cad", words = ["cc","acd","b","ba","bac","bad","ac","d"]
Output: 4
Explanation: Strings "cc", "acd", "ac", and "d" are consistent.


Constraints:

    1 <= words.length <= 10^4
    1 <= allowed.length <= 26
    1 <= words[i].length <= 10
    The characters in allowed are distinct.
    words[i] and allowed contain only lowercase English letters.
"""


class Solution:
    def countConsistentStrings(self, allowed: str, words: List[str]) -> int:
        allowed = set(allowed)
        return sum(all(c in allowed for c in word) for word in words)


sol = Solution()

print(sol.countConsistentStrings("ab", ["ad", "bd", "aaab", "baa", "badab"]))  # 2

assert sol.countConsistentStrings("ab", ["ad", "bd", "aaab", "baa", "badab"]) == 2
assert sol.countConsistentStrings("abc", ["a", "b", "c", "ab", "ac", "bc", "abc"]) == 7
assert sol.countConsistentStrings("cad", ["cc", "acd", "b", "ba", "bac", "bad", "ac", "d"]) == 4
assert sol.countConsistentStrings("a", ["a"]) == 1
assert sol.countConsistentStrings("a", ["b"]) == 0
assert sol.countConsistentStrings("a", ["a", "aa", "aaa", "b", "ab"]) == 3
assert sol.countConsistentStrings("a", ["aaaaaaaaaa"]) == 1
assert sol.countConsistentStrings("ab", ["ab"]) == 1
assert sol.countConsistentStrings("ab", ["c", "cc", "cd"]) == 0
assert sol.countConsistentStrings("ab", ["ba", "abababab", "aabb", "abc"]) == 3
assert sol.countConsistentStrings("xyz", ["zyx", "xxyyzz", "zzz", "yx", "w"]) == 4
assert sol.countConsistentStrings("abcdefghijklmnopqrstuvwxyz", ["zzz", "xyz", "hello", "quick"]) == 4
assert sol.countConsistentStrings("abcde", ["fgh", "af", "ea"]) == 1
assert sol.countConsistentStrings("k", ["k", "kk", "kj", "j"]) == 2