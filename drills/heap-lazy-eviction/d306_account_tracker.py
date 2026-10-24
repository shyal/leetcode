"""
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

1. Applying a transaction adds its amount to the account's balance.
2. Querying an account's balance should be efficient.
3. Finding the richest account should be efficient.
4. Accounts with no transactions should have a balance of zero.

Each test case starts with no transactions applied. `apply` adds `amount` to the account's current balance and returns `none`. `balance` returns the account's current balance without changing any state.

`richest_account` returns the name of the account with the greatest current balance among accounts that have received at least one transaction, including transactions of amount zero. If multiple accounts have that balance, return the lexicographically smallest name. Names are compared alphabetically, with a shorter name ordered before any longer name having it as a prefix. Accounts with no transactions are not candidates, even if all candidate balances are negative. `richest_account` is never called before the first `apply` call.

Constraints

- There are at most 1,000,000 method calls per test case.
- At most 200,000 distinct accounts receive transactions.
- The number of `richest_account` calls is at least the number of `apply` calls.
- Account names contain between 1 and 20 lowercase English letters.
- Each amount is an integer between -1,000,000,000 and 1,000,000,000, inclusive.
- Balances must be returned exactly, without integer overflow.

Example

Starting with a new `Solution` instance, the following calls produce exactly these results:

| Call | Result |
|---|---|
| `balance("carol")` | `0` |
| `apply("bob", -5)` | `none` |
| `richest_account()` | `"bob"` |
| `apply("alice", -5)` | `none` |
| `richest_account()` | `"alice"` |
| `apply("bob", 10)` | `none` |
| `richest_account()` | `"bob"` |
| `balance("bob")` | `5` |
| `balance("alice")` | `-5` |
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
# sol = Solution()
# assert sol.balance("carol") == 0
# sol.apply("bob", -5)
# assert sol.richest_account() == "bob"
# sol.apply("alice", -5)
# assert sol.richest_account() == "alice"
# sol.apply("bob", 10)
# assert sol.richest_account() == "bob"
# assert sol.balance("bob") == 5
# assert sol.balance("alice") == -5
# sol = Solution()
# sol.apply("zed", 0)
# sol.apply("amy", -1)
# assert sol.richest_account() == "zed"
# sol.apply("amy", 1)
# assert sol.richest_account() == "amy"
# sol.apply("am", 0)
# assert sol.richest_account() == "am"
