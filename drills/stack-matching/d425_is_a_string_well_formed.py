"""
EPI 8.3 Is a string well-formed?

Given a string s of the characters '(', ')', '[', ']', '{' and '}',
return True when s is well-formed and False otherwise. A string is
well-formed when each closing bracket matches the type of the nearest
earlier opening bracket that is not matched yet, and every opening
bracket is matched. The empty string is well-formed.

Example 1:

Input: s = "{[]}()"
Output: True

Example 2:

Input: s = "([)]"
Output: False
Explanation: the ')' arrives while '[' is the nearest open bracket.

Example 3:

Input: s = "(("
Output: False

Constraints:

    0 <= len(s) <= 2 * 10^5
    s consists of the six bracket characters only.

    REQUIRED: O(n) time. NO replace(), NO regex.
"""


class Solution:
    def is_well_formed(self, s: str) -> bool:
        pass


sol = Solution()

print(sol.is_well_formed("{[]}()"))  # True

# assert sol.is_well_formed("{[]}()") is True
# assert sol.is_well_formed("([)]") is False
# assert sol.is_well_formed("((") is False
# assert sol.is_well_formed("") is True
# assert sol.is_well_formed("(") is False
# assert sol.is_well_formed(")") is False
# assert sol.is_well_formed("]") is False
# assert sol.is_well_formed("()") is True
# assert sol.is_well_formed("[]{}()") is True
# assert sol.is_well_formed("{[()]}") is True
# assert sol.is_well_formed("(]") is False
# assert sol.is_well_formed("(()") is False
# assert sol.is_well_formed("())") is False
# assert sol.is_well_formed(")(") is False
# assert sol.is_well_formed("(" * 100000 + ")" * 100000) is True
# assert sol.is_well_formed("([{" * 33333 + "}])" * 33333) is True
# assert sol.is_well_formed("()" * 100000 + "(") is False
# assert sol.is_well_formed("{" + "()" * 99999 + "]") is False
