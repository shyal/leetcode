"""
DRILL: Reserve Liability
TRAINS: liability-reserve

Stop a user placing orders they cannot pay for. A back order risks its
stake; a lay order risks stake * (odds - 1). Solution(balances) starts
from a dict user -> balance. The balance itself does not change here;
money moves at settlement. Implement

    place(order_id, user, side, stake, odds) -> bool
    cancel(order_id) -> bool
    available(user) -> int or float

available is the user's balance minus the liability reserved on the
user's open orders, 0 for a user never seen. place reserves the order's
liability and returns True. It returns False and changes nothing when
the liability is more than available or order_id is already an open
order. cancel releases the order's liability and returns True; it returns
False when order_id is not an open order. side is "BACK" or "LAY".

Example 1:

    acct = Solution({"ann": 50})
    acct.place("o1", "ann", "BACK", 10, 2.0)   -> True    (risks 10)
    acct.available("ann")                      -> 40
    acct.place("o2", "ann", "LAY", 10, 3.0)    -> True    (risks 20)
    acct.available("ann")                      -> 20
    acct.place("o3", "ann", "LAY", 10, 4.0)    -> False   (risks 30)
    acct.cancel("o1")                          -> True
    acct.place("o3", "ann", "LAY", 10, 4.0)    -> True
    acct.available("ann")                      -> 0
    acct.cancel("o1")                          -> False

Constraints:

    1 <= stake <= 10^6
    1.01 <= odds <= 1000
    up to 10^5 calls

    REQUIRED: O(1) per call. NO scan of a user's orders to answer
    available.
"""


class Solution:
    def __init__(self, balances: dict):
        pass

    def place(self, order_id: str, user: str, side: str, stake: int, odds: float) -> bool:
        pass

    def cancel(self, order_id: str) -> bool:
        pass

    def available(self, user: str):
        pass


acct = Solution({"ann": 50})

acct.place("o1", "ann", "BACK", 10, 2.0)
print(acct.available("ann"))  # 40

# assert acct.place("o2", "ann", "LAY", 10, 3.0) is True
# assert acct.available("ann") == 20
# assert acct.place("o3", "ann", "LAY", 10, 4.0) is False
# assert acct.available("ann") == 20
# assert acct.cancel("o1") is True
# assert acct.available("ann") == 30
# assert acct.place("o3", "ann", "LAY", 10, 4.0) is True
# assert acct.available("ann") == 0
# assert acct.cancel("o1") is False
# assert acct.place("o2", "ann", "BACK", 1, 2.0) is False  # o2 is open
# assert acct.place("o4", "ann", "BACK", 1, 2.0) is False  # nothing left
# assert acct.cancel("o2") is True
# assert acct.available("ann") == 20
# assert acct.place("o4", "ann", "BACK", 20, 2.0) is True
# assert acct.available("ann") == 0
# assert acct.available("zed") == 0
# assert acct.place("o5", "zed", "BACK", 1, 2.0) is False
# acct2 = Solution({"bob": 100})
# assert acct2.place("p1", "bob", "LAY", 50, 1.5) is True  # risks 25
# assert acct2.available("bob") == 75
# assert acct2.place("p2", "bob", "LAY", 25, 4.0) is True  # risks 75
# assert acct2.available("bob") == 0
# assert acct2.cancel("p2") is True
# assert acct2.cancel("p1") is True
# assert acct2.available("bob") == 100
