"""
DRILL: Settle Once
TRAINS: idempotent-settlement

Pay out a market when its result arrives. Solution(balances, bets) starts
from a dict user -> balance, stored as self.balances, and a dict
market -> list of (user, selection, stake, odds): the matched bets, whose
stakes have already been taken. Settlement events come from a queue that
delivers at least once, so the same event can arrive twice. Implement

    settle(event_id, market, winner) -> bool

settle pays stake * odds to every bet on the market whose selection is
winner, and returns True. It returns False and pays nothing when event_id
was seen before or the market is already settled.

Example 1:

    bets = {"m1": [("ann", "A", 10, 3.0), ("bob", "B", 20, 1.5)]}
    ex = Solution({"ann": 90, "bob": 80}, bets)
    ex.settle("e1", "m1", "A")   -> True    (ann 90 + 30)
    ex.settle("e1", "m1", "A")   -> False   (seen)
    ex.settle("e2", "m1", "B")   -> False   (m1 is settled)
    ex.balances                  -> {"ann": 120.0, "bob": 80}

Example 2:

    bets = {"m2": [("cat", "X", 50, 2.0), ("cat", "Y", 10, 5.0), ("dan", "Y", 10, 5.0)]}
    ex = Solution({"cat": 0, "dan": 0}, bets)
    ex.settle("f1", "m2", "Y")   -> True
    ex.balances                  -> {"cat": 50.0, "dan": 50.0}

Constraints:

    up to 10^5 bets and events

    REQUIRED: a replayed event changes nothing, however many times it
    arrives, and a market pays once; refusing one is O(1).
"""


class Solution:
    def __init__(self, balances: dict, bets: dict):
        pass

    def settle(self, event_id: str, market: str, winner: str) -> bool:
        pass


bets = {"m1": [("ann", "A", 10, 3.0), ("bob", "B", 20, 1.5)]}
ex = Solution({"ann": 90, "bob": 80}, bets)

print(ex.settle("e1", "m1", "A"), ex.balances)  # True {'ann': 120.0, 'bob': 80}

# assert ex.balances == {"ann": 120.0, "bob": 80}
# assert ex.settle("e1", "m1", "A") is False
# assert ex.balances == {"ann": 120.0, "bob": 80}
# assert ex.settle("e2", "m1", "B") is False
# assert ex.balances == {"ann": 120.0, "bob": 80}
# assert ex.settle("e3", "m9", "X") is True
# assert ex.settle("e4", "m9", "X") is False
# assert ex.balances == {"ann": 120.0, "bob": 80}
# bets2 = {"m2": [("cat", "X", 50, 2.0), ("cat", "Y", 10, 5.0), ("dan", "Y", 10, 5.0)]}
# ex2 = Solution({"cat": 0, "dan": 0}, bets2)
# assert ex2.settle("f1", "m2", "Y") is True
# assert ex2.balances == {"cat": 50.0, "dan": 50.0}
# assert ex2.settle("f1", "m2", "X") is False
# assert ex2.settle("f2", "m2", "X") is False
# assert ex2.balances == {"cat": 50.0, "dan": 50.0}
