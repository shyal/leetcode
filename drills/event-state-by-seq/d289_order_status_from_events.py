"""
DRILL: Order Status From Events
TRAINS: event-state-by-seq

Order events arrive from a message queue. An event is (seq, order_id,
user, kind, qty) with kind one of "NEW", "PARTIAL", "FILLED",
"CANCELLED". The sequence number seq counts the events of one order:
1 for NEW, then one more per event. The queue delivers at least once, so
an event can arrive twice, and the events of one order can arrive out of
order. Implement

    apply(seq, order_id, user, kind, qty) -> bool
    status(order_id) -> "open", "filled", "cancelled" or None
    exposure(user) -> int

apply returns True when it applied the event and False when it ignored
it. An event whose seq is not greater than the last seq applied to its
order is ignored: it is a duplicate or it is stale. NEW opens the order
with qty open. PARTIAL takes qty off the open quantity. FILLED and
CANCELLED close the order and leave nothing open.

status is None for an order never seen. exposure is the total open
quantity over a user's orders, 0 for a user never seen.

Example 1:

    feed = Solution()
    feed.apply(1, "o1", "ann", "NEW", 10)      -> True
    feed.apply(2, "o1", "ann", "PARTIAL", 4)   -> True
    feed.apply(2, "o1", "ann", "PARTIAL", 4)   -> False (duplicate)
    feed.exposure("ann")                       -> 6
    feed.apply(3, "o1", "ann", "FILLED", 6)    -> True
    feed.status("o1")                          -> "filled"
    feed.exposure("ann")                       -> 0

Example 2:

    feed = Solution()
    feed.apply(1, "o2", "bob", "NEW", 5)       -> True
    feed.apply(3, "o2", "bob", "CANCELLED", 0) -> True
    feed.apply(2, "o2", "bob", "PARTIAL", 2)   -> False (stale)
    feed.status("o2")                          -> "cancelled"

Constraints:

    up to 10^6 events

    REQUIRED: O(1) per apply and per query. NO scan over orders to answer
    exposure.
"""


class Solution:
    def __init__(self):
        pass

    def apply(self, seq: int, order_id: str, user: str, kind: str, qty: int) -> bool:
        pass

    def status(self, order_id: str):
        pass

    def exposure(self, user: str) -> int:
        pass


feed = Solution()

feed.apply(1, "o1", "ann", "NEW", 10)
feed.apply(2, "o1", "ann", "PARTIAL", 4)
print(feed.exposure("ann"))  # 6

# assert feed.apply(2, "o1", "ann", "PARTIAL", 4) is False
# assert feed.exposure("ann") == 6
# assert feed.status("o1") == "open"
# assert feed.apply(3, "o1", "ann", "FILLED", 6) is True
# assert feed.status("o1") == "filled"
# assert feed.exposure("ann") == 0
# assert feed.apply(1, "o1", "ann", "NEW", 10) is False
# assert feed.status("o1") == "filled"
# assert feed.apply(1, "o2", "bob", "NEW", 5) is True
# assert feed.apply(3, "o2", "bob", "CANCELLED", 0) is True
# assert feed.apply(2, "o2", "bob", "PARTIAL", 2) is False
# assert feed.status("o2") == "cancelled"
# assert feed.exposure("bob") == 0
# assert feed.apply(1, "o3", "bob", "NEW", 7) is True
# assert feed.apply(1, "o4", "bob", "NEW", 3) is True
# assert feed.exposure("bob") == 10
# assert feed.apply(2, "o4", "bob", "PARTIAL", 1) is True
# assert feed.exposure("bob") == 9
# assert feed.status("o9") is None
# assert feed.exposure("nobody") == 0
