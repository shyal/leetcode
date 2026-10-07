"""
DRILL: Match An Order
TRAINS: order-book-match

The resting book of one market is an OrderBook from dsa/order_book.py:
add(order_id, side, price, qty) rests an order, cancel(order_id) removes
what is left of one, best(side) returns (price, qty) for the best level
on a side or None, and fill(side, qty) takes up to qty from the earliest
order at that side's best price and returns (order_id, price, taken).
Solution extends OrderBook. Add matching:

    place(order_id, side, price, qty) -> list of fills

place matches the new order against the other side under price-time
priority: the best price first, and at one price the order that rested
first. A BUY matches SELL prices at most its own; a SELL matches BUY
prices at least its own. Each fill is (buy_id, sell_id, price, qty) at
the resting order's price. What is left of the new order rests in the
book; a fully filled order is added with qty 0 so that its id is known.
place returns [] for an order_id seen before.

Example 1:

    book = Solution()
    book.place("b1", "BUY", 100, 10)   -> []
    book.place("b2", "BUY", 101, 5)    -> []
    book.best("BUY")                   -> (101, 5)
    book.place("s1", "SELL", 99, 8)    -> [("b2", "s1", 101, 5), ("b1", "s1", 100, 3)]
    book.best("BUY")                   -> (100, 7)
    book.best("SELL")                  -> None

Example 2:

    book = Solution()
    book.place("s3", "SELL", 50, 5)    -> []
    book.place("s4", "SELL", 50, 5)    -> []
    book.place("b4", "BUY", 50, 7)     -> [("b4", "s3", 50, 5), ("b4", "s4", 50, 2)]
    book.best("SELL")                  -> (50, 3)

Constraints:

    1 <= price, qty <= 10^9
    up to 10^5 calls

    REQUIRED: O(log n) per fill, amortised. NO scan of the other side's
    orders; NO second copy of the book.
"""

from dsa.order_book import OrderBook


class Solution(OrderBook):
    def place(self, order_id: str, side: str, price: int, qty: int) -> list:
        pass


book = Solution()

book.place("b1", "BUY", 100, 10)
book.place("b2", "BUY", 101, 5)
print(book.place("s1", "SELL", 99, 8))  # [('b2', 's1', 101, 5), ('b1', 's1', 100, 3)]

# assert book.best("BUY") == (100, 7)
# assert book.best("SELL") is None
# assert book.place("s2", "SELL", 105, 4) == []
# assert book.best("SELL") == (105, 4)
# assert book.place("b3", "BUY", 105, 2) == [("b3", "s2", 105, 2)]
# assert book.best("SELL") == (105, 2)
# assert book.cancel("s2") is True
# assert book.best("SELL") is None
# assert book.cancel("s2") is False
# assert book.cancel("nope") is False
# assert book.place("b1", "BUY", 100, 1) == []
# assert book.best("BUY") == (100, 7)
# assert book.cancel("b1") is True
# assert book.best("BUY") is None
# assert book.place("b3", "BUY", 100, 1) == []
# assert book.best("BUY") is None
# book2 = Solution()
# assert book2.place("s3", "SELL", 50, 5) == []
# assert book2.place("s4", "SELL", 50, 5) == []
# assert book2.place("b4", "BUY", 50, 7) == [("b4", "s3", 50, 5), ("b4", "s4", 50, 2)]
# assert book2.best("SELL") == (50, 3)
# assert book2.place("s5", "SELL", 49, 1) == []
# assert book2.best("SELL") == (49, 1)
# assert book2.place("b5", "BUY", 60, 2) == [("b5", "s5", 49, 1), ("b5", "s4", 50, 1)]
# assert book2.best("SELL") == (50, 2)
# assert book2.place("b6", "BUY", 40, 3) == []
# assert book2.best("BUY") == (40, 3)
# assert book2.place("s6", "SELL", 45, 1) == []
# assert book2.best("SELL") == (45, 1)
# assert book2.place("b7", "BUY", 45, 5) == [("b7", "s6", 45, 1)]
# assert book2.best("BUY") == (45, 4)
# assert book2.place("s7", "SELL", 45, 10) == [("b7", "s7", 45, 4)]
# assert book2.best("SELL") == (45, 6)
# assert book2.best("BUY") == (40, 3)
