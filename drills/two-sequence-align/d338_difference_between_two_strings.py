"""
Given two strings of uppercase letters source and target, return a list
of tokens that turns source into target with the fewest edits. Read left
to right, the tokens are: "C" keeps the letter C of source, "-C" removes
the letter C of source, and "+D" inserts the letter D. A removal and an
insertion each count as one edit, a kept letter counts as none. The kept
and inserted letters, in order, spell target. When two token lists have
the fewest edits, return the one that removes from source where the other
inserts.

Example 1:

Input: source = "AABACC", target = "BABCAC"
Output: ["-A", "-A", "B", "A", "+B", "C", "+A", "C"]
Explanation: four edits. Keeping the first A, as in ["+B", "A", "-A",
"B", "-A", "C", "+A", "C"], is also four edits, but it inserts where the
answer removes.

Example 2:

Input: source = "ABCDEFG", target = "ABDFFGH"
Output: ["A", "B", "-C", "D", "-E", "F", "+F", "G", "+H"]
Explanation: four edits, the fewest possible.

Example 3:

Input: source = "CCBC", target = "CCBC"
Output: ["C", "C", "B", "C"]

Constraints:

    1 <= len(source) <= 12
    1 <= len(target) <= 12
    source and target hold uppercase letters only.

    REQUIRED: O(len(source) * len(target)) time. NO enumeration of
    token lists, NO difflib.
"""


class Solution:
    def diff_between_two_strings(self, source: str, target: str) -> list[str]:
        pass


sol = Solution()

print(sol.diff_between_two_strings("AABACC", "BABCAC"))  # ['-A', '-A', 'B', 'A', '+B', 'C', '+A', 'C']

# assert sol.diff_between_two_strings("AABACC", "BABCAC") == ["-A", "-A", "B", "A", "+B", "C", "+A", "C"]
# assert sol.diff_between_two_strings("ABCDEFG", "ABDFFGH") == ["A", "B", "-C", "D", "-E", "F", "+F", "G", "+H"]
# assert sol.diff_between_two_strings("CCBC", "CCBC") == ["C", "C", "B", "C"]
# assert sol.diff_between_two_strings("CBBC", "CABAABBC") == ["C", "+A", "B", "+A", "+A", "B", "+B", "C"]
# assert sol.diff_between_two_strings("CABAAABBC", "CBBC") == ["C", "-A", "B", "-A", "-A", "-A", "B", "-B", "C"]
# assert sol.diff_between_two_strings("HMXPHHUM", "HLZPLUPH") == ["H", "-M", "-X", "+L", "+Z", "P", "-H", "-H", "+L", "U", "-M", "+P", "+H"]
# assert sol.diff_between_two_strings("GHMXGHUGXL", "PPGGXHHULL") == ["+P", "+P", "G", "-H", "-M", "-X", "G", "+X", "H", "+H", "U", "-G", "-X", "L", "+L"]
# assert sol.diff_between_two_strings("GMMGZGGLUGUH", "HPGPPMGLLUUU") == ["+H", "+P", "G", "-M", "+P", "+P", "M", "G", "-Z", "-G", "-G", "L", "+L", "U", "-G", "U", "-H", "+U"]
# assert sol.diff_between_two_strings("A", "A") == ["A"]
# assert sol.diff_between_two_strings("A", "B") == ["-A", "+B"]
# assert sol.diff_between_two_strings("AB", "BA") == ["-A", "B", "+A"]
# assert sol.diff_between_two_strings("ABCDEFGHIJKL", "MNOPQRSTUVWX") == ["-A", "-B", "-C", "-D", "-E", "-F", "-G", "-H", "-I", "-J", "-K", "-L", "+M", "+N", "+O", "+P", "+Q", "+R", "+S", "+T", "+U", "+V", "+W", "+X"]
# assert sol.diff_between_two_strings("ABCDEFGHIJKL", "ABCDEFGHIJKL") == list("ABCDEFGHIJKL")
