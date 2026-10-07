"""
DRILL: Lost Update
TRAINS: version-check-update

Two requests debit the same account at the same time. The service does
this, in a database with no row locks:

    def debit(self, account, amount):
        balance = self.read(account)          # 1. read
        if balance >= amount:                 # 2. check
            self.write(account, balance - amount)   # 3. write
            return True
        return False

Both requests read 100, both check 80 <= 100, both write 20. One debit is
lost and the account paid out 160 on a balance of 100. Fix it with a
version check. Solution(balances) starts from a dict user -> balance,
every account at version 1; an account not in the dict reads as (0, 1).
Implement

    read(account) -> (balance, version)
    debit(account, amount, version) -> bool

debit succeeds, and returns True, only when version equals the account's
current version and the balance covers the amount; then it writes the new
balance and bumps the version. Otherwise it changes nothing and returns
False, and the caller must read again and retry.

Example 1:

    db = Solution({"ann": 100})
    db.read("ann")              -> (100, 1)   first request
    db.read("ann")              -> (100, 1)   second request, same time
    db.debit("ann", 80, 1)      -> True       first writes (20, 2)
    db.debit("ann", 80, 1)      -> False      second is stale
    db.read("ann")              -> (20, 2)    second reads again
    db.debit("ann", 80, 2)      -> False      funds
    db.debit("ann", 20, 2)      -> True       (0, 3)

Constraints:

    up to 10^6 calls

    REQUIRED: the version check and the balance read happen inside debit,
    before the write. NEVER take a balance from the caller.
"""


class Solution:
    def __init__(self, balances: dict):
        pass

    def read(self, account: str) -> tuple:
        pass

    def debit(self, account: str, amount: int, version: int) -> bool:
        pass


db = Solution({"ann": 100})

print(db.read("ann"))  # (100, 1)

# assert db.read("ann") == (100, 1)
# assert db.debit("ann", 80, 1) is True
# assert db.read("ann") == (20, 2)
# assert db.debit("ann", 80, 1) is False
# assert db.read("ann") == (20, 2)
# assert db.debit("ann", 80, 2) is False
# assert db.read("ann") == (20, 2)
# assert db.debit("ann", 20, 2) is True
# assert db.read("ann") == (0, 3)
# assert db.debit("ann", 0, 3) is True
# assert db.read("ann") == (0, 4)
# assert db.debit("ann", 1, 4) is False
# assert db.debit("ann", 0, 2) is False
# assert db.read("zed") == (0, 1)
# assert db.debit("zed", 5, 1) is False
# assert db.debit("zed", 0, 1) is True
# assert db.read("zed") == (0, 2)
# db2 = Solution({"bob": 10, "cat": 10})
# assert db2.debit("bob", 10, 1) is True
# assert db2.debit("cat", 10, 2) is False
# assert db2.debit("cat", 10, 1) is True
# assert db2.read("bob") == (0, 2)
# assert db2.read("cat") == (0, 2)
