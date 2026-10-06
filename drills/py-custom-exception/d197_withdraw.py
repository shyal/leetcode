"""
DRILL: Withdraw
TRAINS: py-custom-exception

Given a `balance` and an `amount`, return the balance after the
withdrawal. When the amount is more than the balance, raise
InsufficientFunds, an exception class of your own, carrying the
shortfall in an attribute named `needed`.

Example 1:

Input: balance = 100, amount = 30
Output: 70

Example 2:

Input: balance = 100, amount = 130
Output: raises InsufficientFunds with needed = 30

Example 3:

Input: balance = 50, amount = 50
Output: 0

Constraints:

    0 <= balance, amount <= 10^9

    REQUIRED: class InsufficientFunds(Exception) defined above Solution,
    with __init__ storing needed and calling super().__init__ with a
    message; raise it with the shortfall. NO ValueError, NO return of a
    negative number, NO return of None.
"""


def caught(call, exc):
    """The exception `call()` raises, or None when it returns."""
    try:
        call()
    except exc as e:
        return e
    return None


class InsufficientFunds(Exception):
    pass


class Solution:

    def withdraw(self, balance: int, amount: int) -> int:
        pass


sol = Solution()

print(sol.withdraw(100, 30))  # 70

# assert sol.withdraw(100, 30) == 70
# assert caught(lambda: sol.withdraw(100, 130), InsufficientFunds).needed == 30
# assert sol.withdraw(50, 50) == 0
# assert caught(lambda: sol.withdraw(0, 1), InsufficientFunds).needed == 1
# assert isinstance(caught(lambda: sol.withdraw(0, 1), InsufficientFunds), Exception)
# assert caught(lambda: sol.withdraw(5, 5), InsufficientFunds) is None
