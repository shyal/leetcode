"""
DRILL: Void A Market
TRAINS: idempotent-settlement

Undo a market: every stake goes back and any payout is taken back.
Solution(balances, bets, winners) starts from a dict user -> balance,
stored as self.balances; a dict market -> list of (user,
selection, stake, odds): the matched bets, whose stakes have already been
taken; and a dict market -> winner for the markets already settled, whose
payouts of stake * odds are already in the balances. Void events come
from a queue that delivers at least once. Implement

    void(event_id, market) -> bool

void returns every stake on the market, takes back the payout of each
winning bet when the market was settled, and returns True. It returns
False and changes nothing when event_id was seen before or the market is
already void.

Example 1:

    bets = {"m1": [("ann", "A", 10, 3.0), ("bob", "B", 20, 1.5)]}
    ex = Solution({"ann": 120, "bob": 80}, bets, {"m1": "A"})
    ex.void("e1", "m1")   -> True    (ann 120 - 30 + 10, bob 80 + 20)
    ex.void("e1", "m1")   -> False   (seen)
    ex.void("e2", "m1")   -> False   (m1 is void)
    ex.balances           -> {"ann": 100.0, "bob": 100}

Example 2:

    bets = {"m2": [("cat", "X", 50, 2.0)]}
    ex = Solution({"cat": 0}, bets, {})
    ex.void("f1", "m2")   -> True    (not settled: only the stake comes back)
    ex.balances           -> {"cat": 50}

Constraints:

    up to 10^5 bets and events

    REQUIRED: a replayed event changes nothing, however many times it
    arrives, and a market is undone once; refusing one is O(1).
"""


class Solution:
    def __init__(self, balances: dict, bets: dict, winners: dict):
        pass

    def void(self, event_id: str, market: str) -> bool:
        pass


bets = {"m1": [("ann", "A", 10, 3.0), ("bob", "B", 20, 1.5)]}
ex = Solution({"ann": 120, "bob": 80}, bets, {"m1": "A"})

print(ex.void("e1", "m1"), ex.balances)  # True {'ann': 100.0, 'bob': 100}

# assert ex.balances == {"ann": 100.0, "bob": 100}
# assert ex.void("e1", "m1") is False
# assert ex.balances == {"ann": 100.0, "bob": 100}
# assert ex.void("e2", "m1") is False
# assert ex.balances == {"ann": 100.0, "bob": 100}
# bets2 = {"m2": [("cat", "X", 50, 2.0)]}
# ex2 = Solution({"cat": 0}, bets2, {})
# assert ex2.void("f1", "m2") is True
# assert ex2.balances == {"cat": 50}
# assert ex2.void("f2", "m2") is False
# assert ex2.balances == {"cat": 50}
# assert ex2.void("f3", "m3") is True
# assert ex2.balances == {"cat": 50}
