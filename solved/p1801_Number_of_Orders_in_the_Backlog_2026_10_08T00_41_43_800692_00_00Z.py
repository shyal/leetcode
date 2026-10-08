# combo chain: backend-live-coding, problem 7 of 10. Run `make combos backend-live-coding` to see
# the chain and what is done this lap; the chain is saved in graph/chains/backend-live-coding.json.
"""
URL: https://leetcode.com/problems/number-of-orders-in-the-backlog/description/?envType=problem-list-v2&envId=vn57k9wr

1801. Number of Orders in the Backlog

You are given a 2D integer array orders, where each orders[i] = [price_i, amount_i, orderType_i] denotes that amount_i orders have been placed of type orderType_i at the price price_i. The orderType_i is:

- 0 if it is a batch of buy orders, or
- 1 if it is a batch of sell orders.

Note that orders[i] represents a batch of amount_i independent orders with the same price and order type. All orders represented by orders[i] will be placed before all orders represented by orders[i+1] for all valid i.

There is a backlog that consists of orders that have not been executed. The backlog is initially empty. When an order is placed, the following happens:

- If the order is a buy order, you look at the sell order with the smallest price in the backlog. If that sell order's price is smaller than or equal to the current buy order's price, they will match and be executed, and that sell order will be removed from the backlog. Else, the buy order is added to the backlog.
- Vice versa, if the order is a sell order, you look at the buy order with the largest price in the backlog. If that buy order's price is larger than or equal to the current sell order's price, they will match and be executed, and that buy order will be removed from the backlog. Else, the sell order is added to the backlog.

Return the total amount of orders in the backlog after placing all the orders from the input. Since this number can be large, return it modulo 10^9 + 7.

Example 1:

Input: orders = [[10,5,0],[15,2,1],[25,1,1],[30,4,0]]
Output: 6
Explanation: Here is what happens with the orders:
- 5 orders of type buy with price 10 are placed. There are no sell orders, so the 5 orders are added to the backlog.
- 2 orders of type sell with price 15 are placed. There are no buy orders with prices larger than or equal to 15, so the 2 orders are added to the backlog.
- 1 order of type sell with price 25 is placed. There are no buy orders with prices larger than or equal to 25 in the backlog, so this order is added to the backlog.
- 4 orders of type buy with price 30 are placed. The first 2 orders are matched with the 2 sell orders of the least price, which is 15 and these 2 sell orders are removed from the backlog. The 3rd order is matched with the sell order of the least price, which is 25 and this sell order is removed from the backlog. Then, there are no more sell orders in the backlog, so the 4th order is added to the backlog.
Finally, the backlog has 5 buy orders with price 10, and 1 buy order with price 30. So the total number of orders in the backlog is 6.

Example 2:

Input: orders = [[7,1000000000,1],[15,3,0],[5,999999995,0],[5,1,1]]
Output: 999999984
Explanation: Here is what happens with the orders:
- 10^9 orders of type sell with price 7 are placed. There are no buy orders, so the 10^9 orders are added to the backlog.
- 3 orders of type buy with price 15 are placed. They are matched with the 3 sell orders with the least price which is 7, and those 3 sell orders are removed from the backlog.
- 999999995 orders of type buy with price 5 are placed. The least price of a sell order is 7, so the 999999995 orders are added to the backlog.
- 1 order of type sell with price 5 is placed. It is matched with the buy order of the highest price, which is 5, and that buy order is removed from the backlog.
Finally, the backlog has (1000000000-3) sell orders with price 7, and (999999995-1) buy orders with price 5. So the total number of orders = 1999999991, which is equal to 999999984 % (10^9 + 7).

Constraints:

    1 <= orders.length <= 10^5
    orders[i].length == 3
    1 <= price_i, amount_i <= 10^9
    orderType_i is either 0 or 1.

---

LEETCODE: Accepted (605 ms, 59 MB)
"""


# mu 0.7
# buy = 0
# sell = 1
#
# def getNumberOfBacklogOrders(orders: [[int]]) -> int
#   buy_orders = heap(type=max)
#   sell_orders = heap(type=min)
#   for (price_i, amount_i, orderType_i) in orders
#     if orderType_i == buy
#       while sell_orders.h and sell_orders.peek()[0] <= price_i
#         sell_price, sell_amount = sell_orders.pop()
#         can_sell = min(amount_i, sell_amount)
#         amount_i -= can_sell
#         remaining = sell_amount - can_sell
#         if remaining
#           sell_orders.push((sell_price, remaining))
#           break
#       if amount_i
#         buy_orders.push((price_i, amount_i))
#     if orderType_i == sell
#       while buy_orders.h and buy_orders.peek()[0] >= price_i
#         buy_price, buy_amount = buy_orders.pop()
#         can_buy = min(amount_i, buy_amount)
#         amount_i -= can_buy
#         remaining = buy_amount - can_buy
#         if remaining
#           buy_orders.push((buy_price, remaining))
#           break
#       if amount_i
#         sell_orders.push((price_i, amount_i))
#   return (sum(amount for (_, amount) in buy_orders) + sum(amount for (_, amount) in sell_orders)) % (10**9 + 7)

from heapq import heapify, heappop, heappush


class heap:
    class _Rev:
        __slots__ = "x"

        def __init__(self, x):
            self.x = x

        def __lt__(self, o):
            return o.x < self.x

    def __init__(self, items=(), type=min):
        self.rev = type is max
        self.h = [self.wrap(x) for x in items]
        heapify(self.h)

    def wrap(self, x):
        return heap._Rev(x) if self.rev else x

    def unwrap(self, x):
        return x.x if self.rev else x

    def push(self, x):
        heappush(self.h, self.wrap(x))

    append = push

    def pop(self):
        return self.unwrap(heappop(self.h))

    def peek(self):
        return self.unwrap(self.h[0])

    def __len__(self):
        return len(self.h)

    def __iter__(self):
        return (self.unwrap(x) for x in self.h)


class Grid(list):
    """A list of rows that also takes a (row, col) pair as an index."""

    def __getitem__(self, k):
        if type(k) is tuple:
            return list.__getitem__(self, k[0])[k[1]]
        return list.__getitem__(self, k)

    def __setitem__(self, k, v):
        if type(k) is tuple:
            list.__getitem__(self, k[0])[k[1]] = v
        else:
            list.__setitem__(self, k, v)


buy = 0
sell = 1


class Solution:
    def getNumberOfBacklogOrders(self, orders: list[list[int]]) -> int:
        _in_orders, orders = orders, Grid(orders)
        _w_orders = orders
        try:
            buy_orders = heap(type=max)
            sell_orders = heap(type=min)
            for (price_i, amount_i, orderType_i) in orders:
                if orderType_i == buy:
                    while sell_orders.h and sell_orders.peek()[0] <= price_i:
                        sell_price, sell_amount = sell_orders.pop()
                        can_sell = min(amount_i, sell_amount)
                        amount_i -= can_sell
                        remaining = sell_amount - can_sell
                        if remaining:
                            sell_orders.push((sell_price, remaining))
                            break
                    if amount_i:
                        buy_orders.push((price_i, amount_i))
                if orderType_i == sell:
                    while buy_orders.h and buy_orders.peek()[0] >= price_i:
                        buy_price, buy_amount = buy_orders.pop()
                        can_buy = min(amount_i, buy_amount)
                        amount_i -= can_buy
                        remaining = buy_amount - can_buy
                        if remaining:
                            buy_orders.push((buy_price, remaining))
                            break
                    if amount_i:
                        sell_orders.push((price_i, amount_i))
            return (sum(amount for (_, amount) in buy_orders) + sum(amount for (_, amount) in sell_orders)) % (10 ** 9 + 7)
        finally:
            _in_orders[:] = _w_orders


sol = Solution()
print(sol.getNumberOfBacklogOrders([[10, 5, 0], [15, 2, 1], [25, 1, 1], [30, 4, 0]]))
_l, _r = sol.getNumberOfBacklogOrders([[10, 5, 0], [15, 2, 1], [25, 1, 1], [30, 4, 0]]), 6
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.getNumberOfBacklogOrders([[7, 1000000000, 1], [15, 3, 0], [5, 999999995, 0], [5, 1, 1]]), 999999984
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.getNumberOfBacklogOrders([[1, 1, 0]]), 1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.getNumberOfBacklogOrders([[1, 1, 1]]), 1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.getNumberOfBacklogOrders([[10 ** 9, 10 ** 9, 0], [10 ** 9, 10 ** 9, 1]]), 0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.getNumberOfBacklogOrders([[5, 10, 0], [5, 10, 0], [5, 10, 1], [5, 10, 1]]), 0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.getNumberOfBacklogOrders([[10, 1, 0], [10, 1, 1], [10, 1, 0], [10, 1, 1]]), 0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.getNumberOfBacklogOrders([[1, 10 ** 9, 0], [2, 10 ** 9, 1]]), 999999993
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.getNumberOfBacklogOrders([[10, 5, 0], [10, 5, 1], [10, 5, 0], [10, 5, 1]]), 0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.getNumberOfBacklogOrders([[1, 1, 0], [2, 1, 1], [3, 1, 0], [4, 1, 1], [5, 1, 0], [6, 1, 1]]), 2
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.getNumberOfBacklogOrders([[10, 1000000000, 0], [9, 1000000000, 1]]), 0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.getNumberOfBacklogOrders([[10, 1, 0], [9, 1, 1], [8, 1, 0], [7, 1, 1], [6, 1, 0], [5, 1, 1]]), 0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.getNumberOfBacklogOrders([[1, 1, 0], [1, 1, 1], [1, 1, 0], [1, 1, 1], [1, 1, 0], [1, 1, 1]]), 0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.getNumberOfBacklogOrders([[10 ** 9, 1, 0], [1, 10 ** 9, 1]]), 999999999
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
