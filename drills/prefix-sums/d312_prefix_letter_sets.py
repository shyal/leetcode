"""
Given a string s, return a list with one set per index: the set at
index i holds the letters of s[:i + 1]. Walk s from the left and add
each letter to the set of letters seen so far. For example with
s = "abbcbc", after "a" the set is {a}, after "ab" it is {a, b}, after
"abb" it is still {a, b}, after "abbc" it is {a, b, c}, and it stays
{a, b, c} to the end.

Example 1:

Input: s = "abbcbc"
Output: [{'a'}, {'a', 'b'}, {'a', 'b'}, {'a', 'b', 'c'}, {'a', 'b', 'c'}, {'a', 'b', 'c'}]

Example 2:

Input: s = "zqq"
Output: [{'z'}, {'q', 'z'}, {'q', 'z'}]

Example 3:

Input: s = "a"
Output: [{'a'}]

Constraints:

    1 <= len(s) <= 2000
    s contains lowercase English letters.

    REQUIRED: one pass over s. The entry at index i is the entry at
    index i - 1 united with s[i]. NO set(s[:i + 1]) per index: rebuilding
    each prefix from scratch is quadratic and is the failure mode this
    drill exists to kill. Every entry is its own set object.

This is a scan with set.union.
"""


class Solution:
    def prefixLetterSets(self, s: str) -> list[set[str]]:
        pass


sol = Solution()

print(sol.prefixLetterSets("abbcbc"))  # [{'a'}, {'a', 'b'}, {'a', 'b'}, {'a', 'b', 'c'}, {'a', 'b', 'c'}, {'a', 'b', 'c'}]

# assert sol.prefixLetterSets("abbcbc") == [{"a"}, {"a", "b"}, {"a", "b"}, {"a", "b", "c"}, {"a", "b", "c"}, {"a", "b", "c"}]
# assert sol.prefixLetterSets("zqq") == [{"z"}, {"q", "z"}, {"q", "z"}]
# assert sol.prefixLetterSets("a") == [{"a"}]
# assert sol.prefixLetterSets("aaaa") == [{"a"}, {"a"}, {"a"}, {"a"}]
# assert sol.prefixLetterSets("abcd") == [{"a"}, {"a", "b"}, {"a", "b", "c"}, {"a", "b", "c", "d"}]
# assert len(sol.prefixLetterSets("ab" * 1000)) == 2000
# assert sol.prefixLetterSets("ab" * 1000)[-1] == {"a", "b"}
