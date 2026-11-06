"""
Given a string text of '(' and ')' characters, return the smallest
number of brackets to insert, at any positions, so that every '(' pairs
with a later ')' and every ')' pairs with an earlier '('.

Example 1:

Input: text = "())("
Output: 2
Explanation: one '(' before the third character and one ')' at the
end give "(())()". The counts of '(' and ')' are equal, and the string
is still not matched.

Example 2:

Input: text = "(()"
Output: 1

Example 3:

Input: text = "(())"
Output: 0

Constraints:

    1 <= len(text) <= 5000
    text consists of '(' and ')' only.

    REQUIRED: O(n) time, O(1) extra space. NO stack, NO list.
"""


class Solution:
    def bracket_match(self, text: str) -> int:
        pass


sol = Solution()

print(sol.bracket_match("())("))  # 2

# assert sol.bracket_match("())(") == 2
# assert sol.bracket_match("(()") == 1
# assert sol.bracket_match("(())") == 0
# assert sol.bracket_match(")") == 1
# assert sol.bracket_match("(") == 1
# assert sol.bracket_match("))))") == 4
# assert sol.bracket_match(")(") == 2
# assert sol.bracket_match("()()()()()") == 0
# assert sol.bracket_match("(((") == 3
# assert sol.bracket_match("(()))(()") == 2
# assert sol.bracket_match("(" * 5000) == 5000
# assert sol.bracket_match(")" * 5000) == 5000
# assert sol.bracket_match("()" * 2500) == 0
# assert sol.bracket_match(")(" * 2500) == 2
# assert sol.bracket_match("(" * 2500 + ")" * 2500) == 0
