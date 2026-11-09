"""
EPI 15.7 Generate strings of matched parens

Given num_pairs, return every string of num_pairs '(' and num_pairs ')'
in which the parentheses are matched: no prefix of the string holds
more ')' than '('. Return the strings in any order.

Example 1:

Input: num_pairs = 3
Output: ["((()))", "(()())", "(())()", "()(())", "()()()"]

Example 2:

Input: num_pairs = 1
Output: ["()"]

Example 3:

Input: num_pairs = 0
Output: [""]
Explanation: the empty string is the only string with no pairs.

Constraints:

    0 <= num_pairs <= 11

    REQUIRED: time proportional to the total length of the strings
    returned. NO generation of every string of 2 * num_pairs
    parentheses followed by a test.
"""


class Solution:
    def generate_balanced_parentheses(self, num_pairs: int) -> list[str]:
        pass


sol = Solution()

print(sol.generate_balanced_parentheses(3))  # ['((()))', '(()())', '(())()', '()(())', '()()()']


def matched(s):
    depth = 0
    for c in s:
        depth += 1 if c == "(" else -1
        if depth < 0:
            return False
    return depth == 0


# assert sorted(sol.generate_balanced_parentheses(3)) == ["((()))", "(()())", "(())()", "()(())", "()()()"]
# assert sol.generate_balanced_parentheses(1) == ["()"]
# assert sol.generate_balanced_parentheses(0) == [""]
# assert sorted(sol.generate_balanced_parentheses(2)) == ["(())", "()()"]
# strings = sol.generate_balanced_parentheses(4)
# assert len(strings) == 14 and len(set(strings)) == 14
# assert all(len(s) == 8 and matched(s) for s in strings)
# assert "(((())))" in strings and "()()()()" in strings and "(()(()))" in strings
# strings = sol.generate_balanced_parentheses(6)
# assert len(strings) == 132 and len(set(strings)) == 132
# assert all(len(s) == 12 and matched(s) for s in strings)
# strings = sol.generate_balanced_parentheses(9)
# assert len(strings) == 4862 and len(set(strings)) == 4862
# strings = sol.generate_balanced_parentheses(11)
# assert len(strings) == 58786 and len(set(strings)) == 58786
# assert all(len(s) == 22 and matched(s) for s in strings)
