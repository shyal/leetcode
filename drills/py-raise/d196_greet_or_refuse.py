"""
DRILL: Greet Or Refuse
TRAINS: py-raise

Given a string `name`, return "Hi, " followed by the name. When the
name is empty or only spaces, raise a ValueError whose message is
"empty name".

Example 1:

Input: name = "Ann"
Output: "Hi, Ann"

Example 2:

Input: name = "   "
Output: raises ValueError("empty name")

Example 3:

Input: name = " Bo "
Output: "Hi, Bo"

Constraints:

    0 <= len(name) <= 100

    REQUIRED: raise ValueError with the exact message; the caller gets
    the exception, not a return value. NO return of None, NO return of
    an error string, NO print.
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
        pass


sol = Solution()

print(sol.greet("Ann"))  # Hi, Ann

# assert sol.greet("Ann") == "Hi, Ann"
# assert str(caught(lambda: sol.greet("   "), ValueError)) == "empty name"
# assert sol.greet(" Bo ") == "Hi, Bo"
# assert str(caught(lambda: sol.greet(""), ValueError)) == "empty name"
# assert caught(lambda: sol.greet("Cy"), ValueError) is None
