"""
EPI 18.7 Transform one string to another

Given a set D of strings of equal length and two strings s and t in D,
return the smallest number of steps that turns s into t, or -1 when no
sequence of steps does. A step changes exactly one character of the
string, and each string after a step must be in D.

Example 1:

Input: D = {"cat", "cot", "cog", "dog", "cut", "dot"}, s = "cat", t = "dog"
Output: 3
Explanation: "cat", "cot", "dot", "dog" is a sequence of 3 steps.
"cat", "cot", "cog", "dog" is another. No sequence of 2 steps exists.

    cut
     |  \\
    cat - cot - cog
           |     |
          dot - dog

Example 2:

Input: D = {"ab", "cd"}, s = "ab", t = "cd"
Output: -1

Example 3:

Input: D = {"abc"}, s = "abc", t = "abc"
Output: 0

Constraints:

    1 <= len(D) <= 5000
    1 <= len(s) <= 10, and all strings in D have the length of s.
    The strings hold lowercase English letters only.
    D may be changed.

    REQUIRED: O(26 * n * m^2) time for n strings of length m. NO loop over
    all pairs of strings.
"""


class Solution:
    def transform_string(self, D: set[str], s: str, t: str) -> int:
        pass


sol = Solution()

draw_graphviz({"cat": ["cot", "cut"], "cut": ["cot"], "cot": ["cog", "dot"], "cog": ["dog"], "dot": ["dog"]})
print(sol.transform_string({"cat", "cot", "cog", "dog", "cut", "dot"}, "cat", "dog"))  # 3

# assert sol.transform_string({"cat", "cot", "cog", "dog", "cut", "dot"}, "cat", "dog") == 3
# assert sol.transform_string({"ab", "cd"}, "ab", "cd") == -1
# assert sol.transform_string({"abc"}, "abc", "abc") == 0
# assert sol.transform_string({"cat", "cot", "cog", "dog", "cut", "dot"}, "dog", "cat") == 3
# assert sol.transform_string({"cat", "cot", "cog", "dog", "cut", "dot"}, "cut", "cot") == 1
# assert sol.transform_string({"a", "b", "c"}, "a", "c") == 1
# assert sol.transform_string({"hit", "hot", "dot", "dog", "cog", "lot", "log"}, "hit", "cog") == 4
# assert sol.transform_string({"aa", "ab", "bb"}, "aa", "bb") == 2
# assert sol.transform_string({"aa", "bb"}, "aa", "bb") == -1
# assert sol.transform_string({"aa", "ab", "bb", "zz"}, "zz", "aa") == -1
# assert sol.transform_string({"abc", "abd", "xyz"}, "abc", "abd") == 1
# assert sol.transform_string(set("".join(p) for p in product("abcdefg", repeat=4)), "aaaa", "gggg") == 4
# assert sol.transform_string({"a" * (10 - k) + "b" * k for k in range(11)}, "a" * 10, "b" * 10) == 10
# assert sol.transform_string(set("".join(p) for p in product("ab", repeat=10) if p.count("b") % 2 == 0), "a" * 10, "bb" + "a" * 8) == -1
# assert sol.transform_string(set("".join(p) for p in product("ab", repeat=10)), "a" * 10, "b" * 10) == 10
