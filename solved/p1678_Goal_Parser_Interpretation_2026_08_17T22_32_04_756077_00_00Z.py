"""
URL: https://leetcode.com/problems/goal-parser-interpretation/description/?envType=problem-list-v2&envId=vn57k9wr

1678. Goal Parser Interpretation

You own a Goal Parser that can interpret a string command. The command
consists of an alphabet of "G", "()" and/or "(al)" in some order. The Goal
Parser will interpret "G" as the string "G", "()" as the string "o", and
"(al)" as the string "al". The interpreted strings are then concatenated in
the original order.

Given the string command, return the Goal Parser's interpretation of command.


Example 1:

Input: command = "G()(al)"
Output: "Goal"
Explanation: The Goal Parser interprets the command as follows:
G -> G
() -> o
(al) -> al
The final concatenated result is "Goal".

Example 2:

Input: command = "G()()()()(al)"
Output: "Gooooal"

Example 3:

Input: command = "(al)G(al)()()G"
Output: "alGalooG"


Constraints:

    1 <= command.length <= 100
    command consists of "G", "()", and/or "(al)" in some order.
"""


class Solution:
    def interpret(self, command: str) -> str:
        command = command.replace('()', 'o')
        command = command.replace('(al)', 'al')
        return command



sol = Solution()

print(sol.interpret("G()(al)"))  # "Goal"

assert sol.interpret("G()(al)") == "Goal"
assert sol.interpret("G()()()()(al)") == "Gooooal"
assert sol.interpret("(al)G(al)()()G") == "alGalooG"
assert sol.interpret("G") == "G"
assert sol.interpret("()") == "o"
assert sol.interpret("(al)") == "al"
assert sol.interpret("GGGG") == "GGGG"
assert sol.interpret("()()()") == "ooo"
assert sol.interpret("(al)(al)(al)") == "alalal"
assert sol.interpret("()(al)") == "oal"
assert sol.interpret("(al)()") == "alo"
assert sol.interpret("G()") == "Go"
assert sol.interpret("()G") == "oG"
assert sol.interpret("G(al)G") == "GalG"
assert sol.interpret("(al)()G()(al)G") == "aloGoalG"
assert sol.interpret("()()(al)G(al)()()()G()") == "ooalGaloooGo"
assert sol.interpret("G" * 100) == "G" * 100
assert sol.interpret("()" * 50) == "o" * 50
assert sol.interpret("(al)" * 25) == "al" * 25
assert sol.interpret("G()(al)" * 10) == "Goal" * 10