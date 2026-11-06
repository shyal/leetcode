"""
Given a word source, a word target and a list of words words, return the
length of the shortest chain of edits from source to target, or -1 when
there is none. An edit changes exactly one letter of the word. Every word
after an edit, the target included, is in words.

Example 1:

Input: source = "bit", target = "pog",
       words = ["but", "put", "big", "pot", "pog", "pig", "dog", "lot"]
Output: 3
Explanation: bit, big, pig, pog. The chain bit, but, put, pot, pog has
four edits.

    bit --- big --- pig
     |               |
    but --- put --- pot --- pog --- dog
                     |
                    lot

Example 2:

Input: source = "no", target = "go", words = ["to"]
Output: -1
Explanation: "go" is not in words.

Example 3:

Input: source = "abc", target = "ab", words = ["abc", "ab"]
Output: -1
Explanation: an edit never changes the length of the word.

Constraints:

    1 <= len(source) <= 20
    1 <= len(target) <= 20
    1 <= len(words) <= 20
    Every word holds lowercase letters only.

    REQUIRED: O(len(words)^2 * len(source)) time. NO recursion, NO
    enumeration of chains.
"""


class Solution:
    def shortestWordEditPath(self, source: str, target: str, words: list[str]) -> int:
        pass


sol = Solution()

draw_graphviz({"bit": ["but", "big"], "big": ["pig"], "pig": ["pog"], "but": ["put"], "put": ["pot"], "pot": ["pog", "lot"], "pog": ["dog"]})
print(sol.shortestWordEditPath("bit", "pog", ["but", "put", "big", "pot", "pog", "pig", "dog", "lot"]))  # 3

# assert sol.shortestWordEditPath("bit", "pog", ["but", "put", "big", "pot", "pog", "pig", "dog", "lot"]) == 3
# assert sol.shortestWordEditPath("no", "go", ["to"]) == -1
# assert sol.shortestWordEditPath("abc", "ab", ["abc", "ab"]) == -1
# assert sol.shortestWordEditPath("bit", "dog", ["but", "put", "big", "pot", "pog", "dog", "lot"]) == 5
# assert sol.shortestWordEditPath("aa", "bb", ["ab", "bb"]) == 2
# assert sol.shortestWordEditPath("aa", "bbb", ["ab", "bb"]) == -1
# assert sol.shortestWordEditPath("a", "b", ["b"]) == 1
# assert sol.shortestWordEditPath("a", "a", ["b"]) == 0
# assert sol.shortestWordEditPath("ab", "cd", ["ad", "cb", "cd"]) == 2
# assert sol.shortestWordEditPath("hit", "cog", ["hot", "dot", "dog", "lot", "log", "cog"]) == 4
# assert sol.shortestWordEditPath("hit", "cog", ["hot", "dot", "dog", "lot", "log"]) == -1
# assert sol.shortestWordEditPath("a" * 20, "b" * 20, ["b" * k + "a" * (20 - k) for k in range(1, 21)]) == 20
# assert sol.shortestWordEditPath("a" * 20, "b" * 20, ["b" * k + "a" * (20 - k) for k in range(2, 21)]) == -1
