"""
DRILL: Simplified Order Book
TRAINS: order-book-match

Implement an order book that processes the following operations:

- `ADD side price quantity`: Add a limit order (side is BUY or SELL)
- `CANCEL order_id`: Cancel an order
- `MATCH`: Execute matching when highest buy price >= lowest sell price

The order book is initially empty. Process operations in the order they appear.

Rules

Adding orders

Each `ADD` creates an order with the given side, limit price, and quantity.

- Order IDs are consecutive integers starting at `1`, assigned in the order of `ADD` operations.
- IDs are never reused, even after an order is canceled or fully filled.
- `ADD` returns the new order's ID.
- Adding an order does not execute trades. Trades occur only during `MATCH`.

Canceling orders

`CANCEL` removes the order's entire remaining quantity from the book.

If the ID is unknown, already canceled, or fully filled, the operation does nothing. In every case, `CANCEL` returns `none`.

Matching orders

`MATCH` repeatedly selects:

- The active BUY order with the highest price.
- The active SELL order with the lowest price.

For orders on the same side at the same price, the order with the smaller order ID has priority.

If both selected orders exist and the buy price is greater than or equal to the sell price, execute a trade:

- The trade quantity is the smaller of the two orders' remaining quantities.
- The trade price is the limit price of whichever selected order has the smaller order ID.
- Subtract the trade quantity from both orders. Remove any order whose remaining quantity becomes zero. A partially filled order retains its original ID, price, and priority.

Continue matching until one side is empty or the highest buy price is less than the lowest sell price.

`MATCH` returns all trades executed by that operation, in execution order. Each trade is represented as:

    [buy_order_id, sell_order_id, trade_price, trade_quantity]

If no trades execute, it returns an empty list.

mu Function Signature

    class Solution
      def process_orders(operations: [list]) -> list

Input Format

`operations` is a list in which each element has exactly one of these forms:

    ["ADD", side, price, quantity]
    ["CANCEL", order_id]
    ["MATCH"]

Here, `side` is either `"BUY"` or `"SELL"`, and all numeric arguments are integers.

Output Format

Return a list containing one result for each input operation, in the same order:

- For `ADD`: the assigned order ID.
- For `CANCEL`: `none`.
- For `MATCH`: a list of trade records.

Example 1: Partial Fills and Trade Prices

Input:

    operations = [
        ["ADD", "BUY", 100, 5],
        ["ADD", "SELL", 95, 3],
        ["MATCH"],
        ["ADD", "SELL", 99, 4],
        ["MATCH"]
    ]

Output:

    [
        1,
        2,
        [[1, 2, 100, 3]],
        3,
        [[1, 3, 100, 2]]
    ]

Explanation:

The first match trades 3 units between orders `1` and `2`. The trade price is `100` because order `1` was added earlier. Order `1` has 2 units remaining.

The second match trades those 2 units against order `3`, again at `100`. Order `3` remains active with 2 units.

Example 2: Price-Time Priority

Input:

    operations = [
        ["ADD", "BUY", 100, 2],
        ["ADD", "BUY", 101, 1],
        ["ADD", "BUY", 101, 3],
        ["ADD", "SELL", 99, 3],
        ["MATCH"]
    ]

Output:

    [
        1,
        2,
        3,
        4,
        [[2, 4, 101, 1], [3, 4, 101, 2]]
    ]

Explanation:

Orders `2` and `3` have higher buy prices than order `1`. Between them, order `2` has priority because its ID is smaller.

Order `2` trades 1 unit, followed by 2 units from order `3`. Both trades execute at `101` because each selected buy order was added before sell order `4`.

Example 3: Cancellation and Empty Matches

Input:

    operations = [
        ["ADD", "SELL", 100, 2],
        ["ADD", "BUY", 100, 2],
        ["CANCEL", 1],
        ["CANCEL", 1],
        ["CANCEL", 99],
        ["MATCH"]
    ]

Output:

    [1, 2, none, none, none, []]

Explanation:

No trade occurs when order `2` is added. The first cancellation removes order `1`. Canceling it again, or canceling unknown ID `99`, has no effect. `MATCH` returns an empty list because no sell orders remain.

Constraints:

- `1 <= len(operations) <= 100_000`
- Every operation has one of the specified forms.
- `side` is `"BUY"` or `"SELL"`.
- `1 <= price, quantity <= 10^9`
- `1 <= order_id <= 10^9` for `CANCEL` operations; the ID need not refer to an existing order.
"""


class Solution:
    def process_orders(self, operations: list) -> list:
        pass


sol = Solution()

operations = [
    ["ADD", "BUY", 100, 5],
    ["ADD", "SELL", 95, 3],
    ["MATCH"],
    ["ADD", "SELL", 99, 4],
    ["MATCH"],
]
print(operations)
print(sol.process_orders(operations))  # [1, 2, [[1, 2, 100, 3]], 3, [[1, 3, 100, 2]]]

# assert sol.process_orders(operations) == [1, 2, [[1, 2, 100, 3]], 3, [[1, 3, 100, 2]]]
# assert sol.process_orders([["ADD", "BUY", 100, 2], ["ADD", "BUY", 101, 1], ["ADD", "BUY", 101, 3], ["ADD", "SELL", 99, 3], ["MATCH"]]) == [1, 2, 3, 4, [[2, 4, 101, 1], [3, 4, 101, 2]]]
# assert sol.process_orders([["ADD", "SELL", 100, 2], ["ADD", "BUY", 100, 2], ["CANCEL", 1], ["CANCEL", 1], ["CANCEL", 99], ["MATCH"]]) == [1, 2, None, None, None, []]
# assert sol.process_orders([["MATCH"]]) == [[]]
# assert sol.process_orders([["ADD", "SELL", 95, 3], ["ADD", "BUY", 100, 5], ["MATCH"], ["CANCEL", 2], ["ADD", "SELL", 90, 1], ["MATCH"]]) == [1, 2, [[2, 1, 95, 3]], None, 3, []]
# assert sol.process_orders([["ADD", "BUY", 100, 4], ["ADD", "SELL", 100, 1], ["ADD", "SELL", 100, 1], ["MATCH"], ["CANCEL", 1], ["CANCEL", 2], ["MATCH"]]) == [1, 2, 3, [[1, 2, 100, 1], [1, 3, 100, 1]], None, None, []]
