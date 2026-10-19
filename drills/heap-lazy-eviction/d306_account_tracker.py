"""
DRILL: Account Tracker

Problem: Maintain account balances from transactions.

You're given a sequence of transactions:

    transactions = [
        ("alice", 100),
        ("bob", 50),
        ("alice", -30),
        ("bob", 20),
        ("alice", 10),
    ]

Each transaction contains an account name and a signed amount.

Implement:

    class Solution
      def apply(account: str, amount: int) -> none
      def balance(account: str) -> int
      def richest_account() -> str

Requirements:

1. Applying a transaction updates the account's balance.
2. Querying an account's balance should be efficient.
3. Finding the richest account should be efficient.
4. Accounts with no transactions should have a balance of zero.
5. Explain how your solution behaves when balances change frequently.
"""


class Solution:
    def __init__(self):
        pass

    def apply(self, account: str, amount: int) -> None:
        pass

    def balance(self, account: str) -> int:
        pass

    def richest_account(self) -> str:
        pass


sol = Solution()

transactions = [("alice", 100), ("bob", 50), ("alice", -30), ("bob", 20), ("alice", 10)]
for account, amount in transactions:
    sol.apply(account, amount)
print(sol.balance("alice"), sol.balance("bob"), sol.richest_account())  # 80 70 alice

# assert sol.balance("alice") == 80
# assert sol.balance("bob") == 70
# assert sol.richest_account() == "alice"
# assert sol.balance("carol") == 0
# sol.apply("bob", 20)
# assert sol.richest_account() == "bob"
# sol.apply("alice", 5)
# assert sol.richest_account() == "bob"
# sol.apply("bob", -50)
# assert sol.richest_account() == "alice"
# assert sol.balance("bob") == 40
# sol = Solution()
# sol.apply("x", -10)
# assert sol.richest_account() == "x"
# assert sol.balance("x") == -10
# sol = Solution()
# sol.apply("a", 100)
# sol.apply("b", 50)
# sol.apply("a", -60)
# assert sol.richest_account() == "b"
# sol.apply("b", -20)
# assert sol.richest_account() == "a"
