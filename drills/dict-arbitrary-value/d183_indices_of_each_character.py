"""
DRILL: Indices Of Each Character
TRAINS: dict-arbitrary-value

Given a string s, return a dict mapping each character of s to the list
of indices where it occurs, in increasing order.

Example 1:

Input: s = "level"
Output: {"l": [0, 4], "e": [1, 3], "v": [2]}
Explanation: the character "l" occurs at indices 0 and 4, "e" at 1 and
3, and "v" at 2.

Example 2:

Input: s = "zzz"
Output: {"z": [0, 1, 2]}

Constraints:

    1 <= len(s) <= 10^5
    s consists of lowercase English letters.

    REQUIRED: must run in O(n) time, in one pass over s. NO `s.index`
    and NO scan of s for each character: on 10^5 characters that is the
    fail.
"""


class Solution:

    def indices(self, s: str) -> Dict[str, List[int]]:
        pass


sol = Solution()

print(dict(sol.indices("level")))  # {'l': [0, 4], 'e': [1, 3], 'v': [2]}

# assert sol.indices("level") == {"l": [0, 4], "e": [1, 3], "v": [2]}
# assert sol.indices("zzz") == {"z": [0, 1, 2]}
# assert sol.indices("q") == {"q": [0]}
# assert sol.indices("abc") == {"a": [0], "b": [1], "c": [2]}
# assert sol.indices("abca") == {"a": [0, 3], "b": [1], "c": [2]}
# assert sol.indices("abb") == {"a": [0], "b": [1, 2]}
# assert sol.indices("ab" * 50000) == {"a": [*range(0, 100000, 2)], "b": [*range(1, 100000, 2)]}
