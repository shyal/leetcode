"""
How would you implement a match-finding system for an order book (buy/sell)?

Implement process_orders(orders) for limit orders processed in input order. A
sell matches the highest-priced available buy when buy_price >= sell_price; a
buy matches the lowest-priced available sell when sell_price <= buy_price. At
the same price, older orders have priority. Each trade executes at the resting
order's price. Return all trades in execution order and all unfilled orders
grouped by side and priority.

Input orders contain id, side ("buy" or "sell"), price, and positive quantity.
Assume unique IDs, integer prices, no cancellations, and no market orders.

Example 1:

Input: orders = [{"id":"b1","side":"buy","price":100,"quantity":10}, {"id":"s1","side":"sell","price":99,"quantity":4}]
Output: {"trades":[{"maker_id":"b1","taker_id":"s1","price":100,"quantity":4}],"remaining":[{"id":"b1","side":"buy","price":100,"quantity":6}]}
Why: The sell crosses the buy. The buy is the resting order, so the trade executes at price 100, leaving six buy units.

Example 2:

Input: orders = [{"id":"s1","side":"sell","price":101,"quantity":5}, {"id":"b1","side":"buy","price":102,"quantity":7}]
Output: {"trades":[{"maker_id":"s1","taker_id":"b1","price":101,"quantity":5}],"remaining":[{"id":"b1","side":"buy","price":102,"quantity":2}]}
Why: The buy crosses the resting sell and consumes all five sell units. Two buy units remain.

Example 3:

Input: orders = [{"id":"b1","side":"buy","price":100,"quantity":5}, {"id":"b2","side":"buy","price":101,"quantity":3}, {"id":"s1","side":"sell","price":99,"quantity":6}]
Output: {"trades":[{"maker_id":"b2","taker_id":"s1","price":101,"quantity":3},{"maker_id":"b1","taker_id":"s1","price":100,"quantity":3}],"remaining":[{"id":"b1","side":"buy","price":100,"quantity":2}]}
Why: The highest-priced buy is matched first, then the lower-priced buy. The sell is fully filled.

Constraints:

    0 <= len(orders) <= 1000
    Each order has a unique string id
    side is either "buy" or "sell"
    price is a positive integer
    quantity is a positive integer
    Orders are processed in input order
    All orders are limit orders and no cancellations are included
"""


class Solution:
    def process_orders(self, orders):
        pass


sol = Solution()

orders = [
    {"id": "b1", "side": "buy", "price": 100, "quantity": 5},
    {"id": "b2", "side": "buy", "price": 101, "quantity": 3},
    {"id": "s1", "side": "sell", "price": 99, "quantity": 6},
]
print(orders)
print(sol.process_orders(orders))
# {'trades': [{'maker_id': 'b2', 'taker_id': 's1', 'price': 101, 'quantity': 3}, {'maker_id': 'b1', 'taker_id': 's1', 'price': 100, 'quantity': 3}], 'remaining': [{'id': 'b1', 'side': 'buy', 'price': 100, 'quantity': 2}]}

# assert sol.process_orders([{"id": "b1", "side": "buy", "price": 100, "quantity": 10}, {"id": "s1", "side": "sell", "price": 99, "quantity": 4}]) == {"trades": [{"maker_id": "b1", "taker_id": "s1", "price": 100, "quantity": 4}], "remaining": [{"id": "b1", "side": "buy", "price": 100, "quantity": 6}]}
# assert sol.process_orders([{"id": "s1", "side": "sell", "price": 101, "quantity": 5}, {"id": "b1", "side": "buy", "price": 102, "quantity": 7}]) == {"trades": [{"maker_id": "s1", "taker_id": "b1", "price": 101, "quantity": 5}], "remaining": [{"id": "b1", "side": "buy", "price": 102, "quantity": 2}]}
# assert sol.process_orders(orders) == {"trades": [{"maker_id": "b2", "taker_id": "s1", "price": 101, "quantity": 3}, {"maker_id": "b1", "taker_id": "s1", "price": 100, "quantity": 3}], "remaining": [{"id": "b1", "side": "buy", "price": 100, "quantity": 2}]}
# assert sol.process_orders([]) == {"trades": [], "remaining": []}
# assert sol.process_orders([{"id": "b1", "side": "buy", "price": 100, "quantity": 2}, {"id": "b2", "side": "buy", "price": 100, "quantity": 2}, {"id": "s1", "side": "sell", "price": 100, "quantity": 3}]) == {"trades": [{"maker_id": "b1", "taker_id": "s1", "price": 100, "quantity": 2}, {"maker_id": "b2", "taker_id": "s1", "price": 100, "quantity": 1}], "remaining": [{"id": "b2", "side": "buy", "price": 100, "quantity": 1}]}
# assert sol.process_orders([{"id": "s1", "side": "sell", "price": 100, "quantity": 2}, {"id": "b1", "side": "buy", "price": 99, "quantity": 1}]) == {"trades": [], "remaining": [{"id": "b1", "side": "buy", "price": 99, "quantity": 1}, {"id": "s1", "side": "sell", "price": 100, "quantity": 2}]}
