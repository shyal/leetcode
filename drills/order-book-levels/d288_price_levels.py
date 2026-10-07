"""
DRILL: Price Levels
TRAINS: order-book-levels

Implement the resting order book of one market. An order is (order_id,
side, price, qty) with side "BUY" or "SELL". Solution() has

    add(order_id, side, price, qty)
    cancel(order_id) -> bool
    best(side) -> (price, qty) or None
    fill(side, qty) -> (order_id, price, taken)

add rests the order on its side; an order with qty 0 is recorded and
rests nothing. cancel removes what is left of a resting order and returns
True; it returns False when there is no such order or nothing is left of
it. best returns the best price on a side, the highest BUY or the lowest
SELL, with the total quantity resting at that price, or None when the
side is empty. fill takes up to qty from the earliest order at the best
price of side and returns that order's id, the price, and the quantity
taken; it is only called when best(side) is not None.

Example 1:

    sol = Solution()
    sol.add("b1", "BUY", 100, 10)
    sol.add("b2", "BUY", 101, 5)
    sol.add("b3", "BUY", 101, 7)
    sol.best("BUY")        -> (101, 12)
    sol.fill("BUY", 8)     -> ("b2", 101, 5)    (the earliest at 101)
    sol.fill("BUY", 8)     -> ("b3", 101, 7)
    sol.best("BUY")        -> (100, 10)
    sol.cancel("b1")       -> True
    sol.best("BUY")        -> None
    sol.cancel("b1")       -> False

Example 2:

    sol = Solution()
    sol.add("s1", "SELL", 50, 5)
    sol.add("s2", "SELL", 49, 1)
    sol.best("SELL")       -> (49, 1)
    sol.cancel("s2")       -> True
    sol.best("SELL")       -> (50, 5)
    sol.fill("SELL", 2)    -> ("s1", 50, 2)
    sol.best("SELL")       -> (50, 3)

Constraints:

    1 <= price, qty <= 10^9
    up to 10^5 calls

    REQUIRED: best, cancel and fill in O(log n) amortised, n orders. NO
    scan of every order or every price to find the best.
"""


class Solution:
    def __init__(self):
        pass

    def add(self, order_id: str, side: str, price: int, qty: int) -> None:
        pass

    def cancel(self, order_id: str) -> bool:
        pass

    def best(self, side: str):
        pass

    def fill(self, side: str, qty: int) -> tuple:
        pass


sol = Solution()

sol.add("b1", "BUY", 100, 10)
sol.add("b2", "BUY", 101, 5)
sol.add("b3", "BUY", 101, 7)
print(sol.best("BUY"))  # (101, 12)

# assert sol.fill("BUY", 8) == ("b2", 101, 5)
# assert sol.best("BUY") == (101, 7)
# assert sol.fill("BUY", 8) == ("b3", 101, 7)
# assert sol.best("BUY") == (100, 10)
# assert sol.cancel("b1") is True
# assert sol.best("BUY") is None
# assert sol.cancel("b1") is False
# assert sol.cancel("nope") is False
# assert sol.best("SELL") is None
# sol.add("s1", "SELL", 50, 5)
# sol.add("s2", "SELL", 49, 1)
# sol.add("s3", "SELL", 50, 4)
# assert sol.best("SELL") == (49, 1)
# assert sol.cancel("s2") is True
# assert sol.best("SELL") == (50, 9)
# assert sol.cancel("s1") is True  # cancelled at the head of its level
# assert sol.best("SELL") == (50, 4)
# assert sol.fill("SELL", 2) == ("s3", 50, 2)
# assert sol.best("SELL") == (50, 2)
# assert sol.fill("SELL", 9) == ("s3", 50, 2)  # takes what is there
# assert sol.best("SELL") is None
# sol.add("z", "BUY", 7, 0)
# assert sol.best("BUY") is None
# assert sol.cancel("z") is False
# sol.add("b4", "BUY", 7, 3)
# assert sol.best("BUY") == (7, 3)
