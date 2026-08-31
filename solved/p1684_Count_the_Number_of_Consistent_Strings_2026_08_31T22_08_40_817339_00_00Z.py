"""
URL: https://leetcode.com/problems/count-the-number-of-consistent-strings/description/?envType=problem-list-v2&envId=vn57k9wr

1684. Count the Number of Consistent Strings

You are given a string allowed consisting of distinct characters and an array of strings words. A string is consistent if all characters in the string appear in the string allowed.

Return the number of consistent strings in the array words.

Example 1:

Input: allowed = "ab", words = ["ad","bd","aaab","baa","badab"]
Output: 2
Explanation: Strings "aaab" and "baa" are consistent since they only contain characters 'a' and 'b'.

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
        return sum(set(x) - allowed == set([]) for x in words)


sol = Solution()

print(sol.countConsistentStrings("ab", ["ad", "bd", "aaab", "baa", "badab"]))  # 2

assert sol.countConsistentStrings("ab", ["ad", "bd", "aaab", "baa", "badab"]) == 2
assert sol.countConsistentStrings("abc", ["a", "b", "c", "ab", "ac", "bc", "abc"]) == 7
assert (
    sol.countConsistentStrings("cad", ["cc", "acd", "b", "ba", "bac", "bad", "ac", "d"])
    == 4
)

assert sol.countConsistentStrings("", ["a", "b", "c"]) == 0
assert sol.countConsistentStrings("a", ["a", "aa", "aaa", "b", "ab"]) == 3
assert (
    sol.countConsistentStrings("xyz", ["x", "y", "z", "xy", "yz", "xz", "xyz", "w"])
    == 7
)
assert sol.countConsistentStrings("abc", ["", "a", "b", "c", "abc", "abcd"]) == 5
assert sol.countConsistentStrings("a", ["a" * 10, "b" * 10, "a" * 5 + "b" * 5]) == 1
assert (
    sol.countConsistentStrings(
        "abcdefghijklmnopqrstuvwxyz", ["a" * 10, "z" * 10, "m" * 10, "abcxyz"]
    )
    == 4
)
assert sol.countConsistentStrings("abc", ["abcabcabcabcabcabcabcabcabcabc"]) == 1
assert (
    sol.countConsistentStrings(
        "a",
        [
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
    == 10
)
assert (
    sol.countConsistentStrings(
        "abc", ["abc", "def", "ghi", "jkl", "mno", "pqr", "stu", "vwx", "yz"]
    )
    == 1
)
assert (
    sol.countConsistentStrings(
        "abc", ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]
    )
    == 3
)
assert (
    sol.countConsistentStrings("a", ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"])
    == 1
)
assert sol.countConsistentStrings("z", ["z" * 10, "y" * 10, "x" * 10]) == 1
