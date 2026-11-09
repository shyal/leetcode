"""
EPI 15.8 Generate palindromic decompositions

Given a string text, return every way to cut text into pieces that are
all palindromes. Write each way as the list of its pieces, from left to
right. A palindrome reads the same forwards and backwards. Return the
ways in any order.

Example 1:

Input: text = "aab"
Output: [["a", "a", "b"], ["aa", "b"]]

Example 2:

Input: text = "abba"
Output: [["a", "b", "b", "a"], ["a", "bb", "a"], ["abba"]]

Example 3:

Input: text = "ab"
Output: [["a", "b"]]
Explanation: "ab" is not a palindrome, so it must be cut.

Constraints:

    1 <= len(text) <= 15
    text holds only lowercase letters and digits.

    REQUIRED: O(n * 2^n) time, where n is len(text). NO regex.
"""


class Solution:
    def palindrome_decompositions(self, text: str) -> list[list[str]]:
        pass


sol = Solution()

print(sol.palindrome_decompositions("aab"))  # [['a', 'a', 'b'], ['aa', 'b']]

# assert sorted(sol.palindrome_decompositions("aab")) == [["a", "a", "b"], ["aa", "b"]]
# assert sorted(sol.palindrome_decompositions("abba")) == [["a", "b", "b", "a"], ["a", "bb", "a"], ["abba"]]
# assert sol.palindrome_decompositions("ab") == [["a", "b"]]
# assert sol.palindrome_decompositions("z") == [["z"]]
# assert sorted(sol.palindrome_decompositions("aaa")) == [["a", "a", "a"], ["a", "aa"], ["aa", "a"], ["aaa"]]
# assert sorted(sol.palindrome_decompositions("abcba")) == [["a", "b", "c", "b", "a"], ["a", "bcb", "a"], ["abcba"]]
# assert sorted(sol.palindrome_decompositions("racecar")) == [["r", "a", "c", "e", "c", "a", "r"], ["r", "a", "cec", "a", "r"], ["r", "aceca", "r"], ["racecar"]]
# assert sorted(sol.palindrome_decompositions("abc")) == [["a", "b", "c"]]
# assert sorted(sol.palindrome_decompositions("1221")) == [["1", "2", "2", "1"], ["1", "22", "1"], ["1221"]]
# ways = sol.palindrome_decompositions("a" * 15)
# assert len(ways) == 16384 and len(set(map(tuple, ways))) == 16384
# assert all("".join(w) == "a" * 15 for w in ways)
# ways = sol.palindrome_decompositions("abcdefghijklmno")
# assert ways == [list("abcdefghijklmno")]
