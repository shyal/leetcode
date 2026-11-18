"""
Given a string `name`, return "Hi, " followed by the name without its
leading and trailing spaces. When the name has no character other than
a space, raise a ValueError whose message is "empty name". The empty
string and a string of one or more spaces are such names.

Example 1:

Input: name = "Ann"
Output: "Hi, Ann"

Example 2:

Input: name = "   "
Output: raises ValueError("empty name")
Explanation: The name is three spaces.

Example 3:

Input: name = " Bo "
Output: "Hi, Bo"
Explanation: The space before "Bo" and the space after it are not in
the output.

Example 4:

Input: name = ""
Output: raises ValueError("empty name")

Constraints:

    0 <= len(name) <= 100

    REQUIRED: NO return of None, NO return of an error string, NO print.
"""


def caught(call, exc):
    """The exception `call()` raises, or None when it returns."""
    try:
        call()
    except exc as e:
        return e
    return None


class Solution:

    def greet(self, name: str) -> str:
        if not name or len(set(name)) == 1 and name[0] == " ":
            raise ValueError("empty name")
        return f"Hi, {name.strip()}"


sol = Solution()

print(sol.greet("Ann"))  # Hi, Ann

assert sol.greet("Ann") == "Hi, Ann"
assert str(caught(lambda: sol.greet("   "), ValueError)) == "empty name"
assert sol.greet(" Bo ") == "Hi, Bo"
assert str(caught(lambda: sol.greet(""), ValueError)) == "empty name"
assert caught(lambda: sol.greet("Cy"), ValueError) is None
