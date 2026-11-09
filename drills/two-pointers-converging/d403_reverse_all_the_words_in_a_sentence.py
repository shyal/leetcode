"""
EPI 6.6 Reverse all the words in a sentence

Given a list s of single characters, split it into maximal runs of
non-space characters (words) and maximal runs of spaces. Change s in
place so that these runs appear in reverse order, each run unchanged.
Return nothing.

Example 1:

Input: s = list("ram is costly")
Output: s == list("costly is ram")

Example 2:

Input: s = list("  hello world")
Output: s == list("world hello  ")
Explanation: the runs are "  ", "hello", " ", "world". In reverse
order they are "world", " ", "hello", "  ".

Example 3:

Input: s = list("a")
Output: s == list("a")

Constraints:

    0 <= len(s) <= 2 * 10^5
    Each s[i] is a letter or ' '.

    REQUIRED: O(n) time, O(1) extra space. NO new list or string, NO
    split(), NO join(), NO slicing, NO reverse() or reversed().
"""


class Solution:
    def reverse_words(self, s: list[str]) -> None:
        pass


sol = Solution()

s = list("ram is costly")
sol.reverse_words(s)
print("".join(s))  # costly is ram

# s = list("ram is costly")
# sol.reverse_words(s)
# assert s == list("costly is ram")
# s = list("  hello world")
# sol.reverse_words(s)
# assert s == list("world hello  ")
# s = list("a")
# sol.reverse_words(s)
# assert s == list("a")
# s = []
# sol.reverse_words(s)
# assert s == []
# s = list(" ")
# sol.reverse_words(s)
# assert s == list(" ")
# s = list("Alice likes Bob")
# sol.reverse_words(s)
# assert s == list("Bob likes Alice")
# s = list("ab cd")
# sol.reverse_words(s)
# assert s == list("cd ab")
# s = list("word ")
# sol.reverse_words(s)
# assert s == list(" word")
# s = list("a  b   c")
# sol.reverse_words(s)
# assert s == list("c   b  a")
# s = list("abc")
# sol.reverse_words(s)
# assert s == list("abc")
# s = list("x" * 200000)
# sol.reverse_words(s)
# assert s == list("x" * 200000)
# s = list("ab cde " * 25000)
# sol.reverse_words(s)
# assert s == list(" " + "cde ab " * 24999 + "cde ab")
# s = list("a " * 100000)
# sol.reverse_words(s)
# assert s == list(" a" * 100000)
