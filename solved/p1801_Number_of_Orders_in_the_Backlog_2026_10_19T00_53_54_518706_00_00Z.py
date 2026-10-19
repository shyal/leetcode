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
[price_i, amount_i, orderType_i]

LEETCODE: Accepted (882 ms, 59 MB)
"""


# mu 0.12
# class OrderType
#   buy = 0
#   sell = 1
#
# class DataType
#   price = 0
#   amount = 1
#
# class Solution
#   def getNumberOfBacklogOrders(orders: [[int]]) -> int
#     buys = heap(type=max)
#     sells = heap(type=min)
#     for price, amount, type in orders
#       if type == OrderType.buy
#         while amount and sells and sells.peek()[DataType.price] <= price
#           exec_price, available_amount = sells.pop()
#           exec_amount = min(available_amount, amount)
#           remaining_amount = available_amount - exec_amount
#           amount -= exec_amount
#           if remaining_amount
#             sells.push([exec_price, remaining_amount])
#         if amount
#           buys.push([price, amount])
#       if type == OrderType.sell
#         while amount and buys and buys.peek()[DataType.price] >= price
#           exec_price, available_amount = buys.pop()
#           exec_amount = min(available_amount, amount)
#           remaining_amount = available_amount - exec_amount
#           amount -= exec_amount
#           if remaining_amount
#             buys.push([exec_price, remaining_amount])
#         if amount
#           sells.push([price, amount])
#     (sum([x[DataType.amount] for x in buys.h]) + sum([x[DataType.amount] for x in sells.h])) % (10**9 + 7)
#
# #        price    amount
# # buy:  [10        5]
# # sell: [15        2]  2 of this <-|
# # sell: [25        1]  1 of this <-|
# # buy:  [30        4]  executes with
# #
# #                  12
# #

def _down(h, i, before):
    (n, x) = (len(h), h[i])
    while (c := (2 * i + 1)) < n:
        if c + 1 < n and before(h[c + 1], h[c]):
            c += 1
        if not before(h[c], x):
            break
        h[i] = h[c]
        i = c
    h[i] = x


def _gt(a, b):
    return b < a


def _lt(a, b):
    return a < b


def _pop(h, before):
    last = h.pop()
    if not h:
        return last
    (top, h[0]) = (h[0], last)
    _down(h, 0, before)
    return top


def _up(h, i, before):
    x = h[i]
    while i:
        p = (i - 1) // 2
        if not before(x, h[p]):
            break
        h[i] = h[p]
        i = p
    h[i] = x


class heap:

    def __init__(self, items=(), type=min):
        self.before = _gt if type is max else _lt
        self.h = list(items)
        for i in reversed(range(len(self.h) // 2)):
            _down(self.h, i, self.before)

    def push(self, x):
        self.h.append(x)
        _up(self.h, len(self.h) - 1, self.before)
    append = push

    def pop(self):
        return _pop(self.h, self.before)

    def peek(self):
        return self.h[0]

    def __len__(self):
        return len(self.h)

    def __iter__(self):
        return iter(self.h)


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


class OrderType:
    buy = 0
    sell = 1


class DataType:
    price = 0
    amount = 1


class Solution:
    def getNumberOfBacklogOrders(self, orders: list[list[int]]) -> int:
        _in_orders, orders = orders, Grid(orders)
        _w_orders = orders
        try:
            buys = heap(type=max)
            sells = heap(type=min)
            for price, amount, type in orders:
                if type == OrderType.buy:
                    while amount and sells and sells.peek()[DataType.price] <= price:
                        exec_price, available_amount = sells.pop()
                        exec_amount = min(available_amount, amount)
                        remaining_amount = available_amount - exec_amount
                        amount -= exec_amount
                        if remaining_amount:
                            sells.push([exec_price, remaining_amount])
                    if amount:
                        buys.push([price, amount])
                if type == OrderType.sell:
                    while amount and buys and buys.peek()[DataType.price] >= price:
                        exec_price, available_amount = buys.pop()
                        exec_amount = min(available_amount, amount)
                        remaining_amount = available_amount - exec_amount
                        amount -= exec_amount
                        if remaining_amount:
                            buys.push([exec_price, remaining_amount])
                    if amount:
                        sells.push([price, amount])
            return (sum([x[DataType.amount] for x in buys.h]) + sum([x[DataType.amount] for x in sells.h])) % (10 ** 9 + 7)
        finally:
            _in_orders[:] = _w_orders


sol = Solution()
print(sol.getNumberOfBacklogOrders([[10, 5, 0], [15, 2, 1], [25, 1, 1], [30, 4, 0]]))
_l, _r = sol.getNumberOfBacklogOrders([[10, 5, 0], [15, 2, 1], [25, 1, 1], [30, 4, 0]]), 6
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
