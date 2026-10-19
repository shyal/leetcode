"""
DRILL: Order Book Match Finding
TRAINS: order-book-match

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
---
didn't get the sorting requirement, and claude spoiled the problem by giving the solution
learning

from rich import print

class DataType
  price = 0
  id = 1
  quantity = 2

class Solution
  def process_orders(orders)
    sells = heap(type=min)
    buys = heap(type=max)
    executed = []
    id_to_order = {}
    order_to_id = {}
    for >i, id in sorted([order['id'] for order in orders], reverse=True)
      id_to_order[id] = i
      order_to_id[i] = id

    for order in orders
      if order['side'] == 'buy'
        while order['quantity'] and sells.h and order['price'] >= sells.peek()[DataType.price]
          maker_price, maker_id, maker_quantity = sells.pop()
          maker_id = order_to_id[maker_id]
          exec_quantity = min(maker_quantity, order['quantity'])
          if exec_quantity
            executed <- dict(maker_id=maker_id, taker_id=order['id'], price=maker_price, quantity=exec_quantity)
          remaining = maker_quantity - exec_quantity
          if remaining > 0
            sells.push([maker_price, id_to_order[maker_id], remaining])
          order['quantity'] -= exec_quantity
        if order['quantity']
          buys.push([order['price'], id_to_order[order['id']], order['quantity']])
      if order['side'] == 'sell'
        while order['quantity'] and buys.h and order['price'] <= buys.peek()[DataType.price]
          maker_price, maker_id, maker_quantity = buys.pop()
          maker_id = order_to_id[maker_id]
          exec_quantity = min(maker_quantity, order['quantity'])
          if exec_quantity
            executed <- dict(maker_id=maker_id, taker_id=order['id'], price=maker_price, quantity=exec_quantity)
          remaining = maker_quantity - exec_quantity
          if remaining > 0
            buys.push([maker_price, id_to_order[maker_id], remaining])
          order['quantity'] -= exec_quantity
        if order['quantity']
          sells.push([order['price'], id_to_order[order['id']], order['quantity']])
    print(buys.h)
    print(sells.h)
    remaining_buys = [dict(id=order_to_id[x[DataType.id]], side='buy', price=x[DataType.price], quantity=x[DataType.quantity]) for x in buys.h]
    remaining_sells = [dict(id=order_to_id[x[DataType.id]], side='sell', price=x[DataType.price], quantity=x[DataType.quantity]) for x in sells.h]
    {'trades': executed, 'remaining': remaining_buys + remaining_sells}
"""


# mu 0.12
# from rich import print
#
# class DataType
#   price = 0
#   id = 1
#   quantity = 2
#
# class Solution
#   def process_orders(orders)
#     sells = heap(type=min)
#     buys = heap(type=max)
#     executed = []
#     id_to_order = {}
#     order_to_id = {}
#     for >i, order in orders
#       id_to_order[order['id']] = i
#       order_to_id[i] = order['id']
#
#     for order in orders
#       quantity = order['quantity']
#       if order['side'] == 'buy'
#         while quantity and sells.h and order['price'] >= sells.peek()[DataType.price]
#           maker_price, maker_id, maker_quantity = sells.pop()
#           maker_id = order_to_id[maker_id]
#           exec_quantity = min(maker_quantity, quantity)
#           if exec_quantity
#             executed <- dict(maker_id=maker_id, taker_id=order['id'], price=maker_price, quantity=exec_quantity)
#           remaining = maker_quantity - exec_quantity
#           if remaining > 0
#             sells.push([maker_price, id_to_order[maker_id], remaining])
#           quantity -= exec_quantity
#         if quantity
#           buys.push([order['price'], -id_to_order[order['id']], quantity])
#       if order['side'] == 'sell'
#         while quantity and buys.h and order['price'] <= buys.peek()[DataType.price]
#           maker_price, maker_id, maker_quantity = buys.pop()
#           maker_id = order_to_id[-maker_id]
#           exec_quantity = min(maker_quantity, quantity)
#           if exec_quantity
#             executed <- dict(maker_id=maker_id, taker_id=order['id'], price=maker_price, quantity=exec_quantity)
#           remaining = maker_quantity - exec_quantity
#           if remaining > 0
#             buys.push([maker_price, -id_to_order[maker_id], remaining])
#           quantity -= exec_quantity
#         if quantity
#           sells.push([order['price'], id_to_order[order['id']], quantity])
#     print(buys.h)
#     print(sells.h)
#     remaining_buys = [dict(id=order_to_id[-x[DataType.id]], side='buy', price=x[DataType.price], quantity=x[DataType.quantity]) for x in sorted(buys.h, reverse=True)]
#     remaining_sells = [dict(id=order_to_id[x[DataType.id]], side='sell', price=x[DataType.price], quantity=x[DataType.quantity]) for x in sorted(sells.h)]
#     {'trades': executed, 'remaining': remaining_buys + remaining_sells}

from rich import print


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


class DataType:
    price = 0
    id = 1
    quantity = 2


class Solution:
    def process_orders(self, orders):
        sells = heap(type=min)
        buys = heap(type=max)
        executed = []
        id_to_order = {}
        order_to_id = {}
        for i, order in enumerate(orders):
            id_to_order[order['id']] = i
            order_to_id[i] = order['id']
        for order in orders:
            quantity = order['quantity']
            if order['side'] == 'buy':
                while quantity and sells.h and order['price'] >= sells.peek()[DataType.price]:
                    maker_price, maker_id, maker_quantity = sells.pop()
                    maker_id = order_to_id[maker_id]
                    exec_quantity = min(maker_quantity, quantity)
                    if exec_quantity:
                        executed.append(dict(maker_id=maker_id, taker_id=order['id'], price=maker_price, quantity=exec_quantity))
                    remaining = maker_quantity - exec_quantity
                    if remaining > 0:
                        sells.push([maker_price, id_to_order[maker_id], remaining])
                    quantity -= exec_quantity
                if quantity:
                    buys.push([order['price'], -id_to_order[order['id']], quantity])
            if order['side'] == 'sell':
                while quantity and buys.h and order['price'] <= buys.peek()[DataType.price]:
                    maker_price, maker_id, maker_quantity = buys.pop()
                    maker_id = order_to_id[-maker_id]
                    exec_quantity = min(maker_quantity, quantity)
                    if exec_quantity:
                        executed.append(dict(maker_id=maker_id, taker_id=order['id'], price=maker_price, quantity=exec_quantity))
                    remaining = maker_quantity - exec_quantity
                    if remaining > 0:
                        buys.push([maker_price, -id_to_order[maker_id], remaining])
                    quantity -= exec_quantity
                if quantity:
                    sells.push([order['price'], id_to_order[order['id']], quantity])
        print(buys.h)
        print(sells.h)
        remaining_buys = [dict(id=order_to_id[-x[DataType.id]], side='buy', price=x[DataType.price], quantity=x[DataType.quantity]) for x in sorted(buys.h, reverse=True)]
        remaining_sells = [dict(id=order_to_id[x[DataType.id]], side='sell', price=x[DataType.price], quantity=x[DataType.quantity]) for x in sorted(sells.h)]
        return {'trades': executed, 'remaining': remaining_buys + remaining_sells}


sol = Solution()
orders = [{'id': 'b1', 'side': 'buy', 'price': 100, 'quantity': 2}, {'id': 'b2', 'side': 'buy', 'price': 100, 'quantity': 2}, {'id': 's1', 'side': 'sell', 'price': 100, 'quantity': 3}]
_l, _r = sol.process_orders(orders), {'trades': [{'maker_id': 'b1', 'taker_id': 's1', 'price': 100, 'quantity': 2}, {'maker_id': 'b2', 'taker_id': 's1', 'price': 100, 'quantity': 1}], 'remaining': [{'id': 'b2', 'side': 'buy', 'price': 100, 'quantity': 1}]}
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
orders = [{'id': 'b1', 'side': 'buy', 'price': 100, 'quantity': 5}, {'id': 'b2', 'side': 'buy', 'price': 101, 'quantity': 3}, {'id': 's1', 'side': 'sell', 'price': 99, 'quantity': 6}]
print(orders)
print(sol.process_orders(orders))
_l, _r = sol.process_orders(orders), {'trades': [{'maker_id': 'b2', 'taker_id': 's1', 'price': 101, 'quantity': 3}, {'maker_id': 'b1', 'taker_id': 's1', 'price': 100, 'quantity': 3}], 'remaining': [{'id': 'b1', 'side': 'buy', 'price': 100, 'quantity': 2}]}
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
_l, _r = sol.process_orders([{'id': 'b1', 'side': 'buy', 'price': 100, 'quantity': 10}, {'id': 's1', 'side': 'sell', 'price': 99, 'quantity': 4}]), {'trades': [{'maker_id': 'b1', 'taker_id': 's1', 'price': 100, 'quantity': 4}], 'remaining': [{'id': 'b1', 'side': 'buy', 'price': 100, 'quantity': 6}]}
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
_l, _r = sol.process_orders([{'id': 's1', 'side': 'sell', 'price': 101, 'quantity': 5}, {'id': 'b1', 'side': 'buy', 'price': 102, 'quantity': 7}]), {'trades': [{'maker_id': 's1', 'taker_id': 'b1', 'price': 101, 'quantity': 5}], 'remaining': [{'id': 'b1', 'side': 'buy', 'price': 102, 'quantity': 2}]}
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
_l, _r = sol.process_orders([]), {'trades': [], 'remaining': []}
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
_l, _r = sol.process_orders([{'id': 's1', 'side': 'sell', 'price': 100, 'quantity': 2}, {'id': 'b1', 'side': 'buy', 'price': 99, 'quantity': 1}]), {'trades': [], 'remaining': [{'id': 'b1', 'side': 'buy', 'price': 99, 'quantity': 1}, {'id': 's1', 'side': 'sell', 'price': 100, 'quantity': 2}]}
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
