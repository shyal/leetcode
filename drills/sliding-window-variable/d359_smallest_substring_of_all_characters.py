"""
Given a list arr of distinct characters and a string s, return the
shortest substring of s that contains every character of arr. If no
substring contains them all, return "". If several shortest substrings
exist, return the one that starts first.

Example 1:

Input: arr = ['x', 'y', 'z'], s = "xyyzyzyx"
Output: "zyx"
Explanation: "xyyz" also contains all three characters, and is longer.

Example 2:

Input: arr = ['A', 'B', 'C'], s = "ADOBECODEBANCDDD"
Output: "BANC"

Example 3:

Input: arr = ['x', 'y', 'z', 'r'], s = "xyyzyzyx"
Output: ""

Constraints:

    1 <= len(arr) <= 30
    0 <= len(s) <= 500
    The characters of arr are distinct.

    REQUIRED: O(len(s) + len(arr)) time. NO enumeration of all
    substrings.
"""


class Solution:
    def get_shortest_unique_substring(self, arr: list[str], s: str) -> str:
        pass


sol = Solution()

print(sol.get_shortest_unique_substring(['x', 'y', 'z'], "xyyzyzyx"))  # zyx

# assert sol.get_shortest_unique_substring(['x', 'y', 'z'], "xyyzyzyx") == "zyx"
# assert sol.get_shortest_unique_substring(['A', 'B', 'C'], "ADOBECODEBANCDDD") == "BANC"
# assert sol.get_shortest_unique_substring(['x', 'y', 'z', 'r'], "xyyzyzyx") == ""
# assert sol.get_shortest_unique_substring(['A'], "") == ""
# assert sol.get_shortest_unique_substring(['A'], "B") == ""
# assert sol.get_shortest_unique_substring(['A'], "A") == "A"
# assert sol.get_shortest_unique_substring(['A', 'B', 'C', 'E', 'K', 'I'], "KADOBECODEBANCDDDEI") == "KADOBECODEBANCDDDEI"
# assert sol.get_shortest_unique_substring(['a', 'b'], "abxab") == "ab"
# assert sol.get_shortest_unique_substring(['a', 'b'], "baxab") == "ba"
# assert sol.get_shortest_unique_substring(['a', 'b'], "aaaab") == "ab"
# assert sol.get_shortest_unique_substring(['a', 'b'], "baaaa") == "ba"
# assert sol.get_shortest_unique_substring(['a'], "a" * 500) == "a"
# assert sol.get_shortest_unique_substring(['a', 'b'], "a" * 499 + "b") == "ab"
# assert sol.get_shortest_unique_substring(['a', 'b'], "b" + "a" * 499) == "ba"
# assert sol.get_shortest_unique_substring(['b', 'a'], "a" * 250 + "b" * 250) == "ab"
# assert sol.get_shortest_unique_substring(list("abcdefghijklmnopqrstuvwxyz0123"), "abcdefghijklmnopqrstuvwxyz0123" * 16) == "abcdefghijklmnopqrstuvwxyz0123"
