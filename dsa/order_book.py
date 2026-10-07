class OrderBook:
    """The resting order book of one market.

    orders     order_id -> [side, price, qty left]; a cancelled or fully
               filled order keeps its entry with qty 0, so its id is known
    levels     side -> price -> deque of order ids, earliest first
    level_qty  side -> price -> quantity resting at that price
    prices     side -> heap of prices; BUY prices are negated so the top
               of either heap is the best price

    A cancelled order is left in its queue with qty 0 and removed when it
    reaches the head; an empty level is removed when it reaches the top of
    the heap. best, cancel and fill are O(log n) amortised.
    """

    def __init__(self):
        self.orders = {}
        self.levels = {"BUY": {}, "SELL": {}}
        self.level_qty = {"BUY": {}, "SELL": {}}
        self.prices = {"BUY": [], "SELL": []}

    def add(self, order_id, side, price, qty):
        self.orders[order_id] = [side, price, qty]
        if qty == 0:
            return
        if price not in self.levels[side]:
            self.levels[side][price] = deque()
            self.level_qty[side][price] = 0
            heappush(self.prices[side], -price if side == "BUY" else price)
        self.levels[side][price].append(order_id)
        self.level_qty[side][price] += qty

    def best(self, side):
        heap, levels = self.prices[side], self.levels[side]
        while heap:
            price = -heap[0] if side == "BUY" else heap[0]
            queue = levels[price]
            while queue and self.orders[queue[0]][2] == 0:
                queue.popleft()
            if queue:
                return (price, self.level_qty[side][price])
            heappop(heap)
            del levels[price]
            del self.level_qty[side][price]
        return None

    def cancel(self, order_id):
        order = self.orders.get(order_id)
        if order is None or order[2] == 0:
            return False
        side, price, qty = order
        order[2] = 0
        self.level_qty[side][price] -= qty
        return True

    def fill(self, side, qty):
        price, _ = self.best(side)
        order_id = self.levels[side][price][0]
        order = self.orders[order_id]
        taken = min(qty, order[2])
        order[2] -= taken
        self.level_qty[side][price] -= taken
        return (order_id, price, taken)


book = OrderBook()
book.add("b1", "BUY", 100, 10)
book.add("b2", "BUY", 101, 5)
book.add("b3", "BUY", 101, 7)
assert book.best("BUY") == (101, 12)
assert book.fill("BUY", 8) == ("b2", 101, 5)  # earliest at 101 first
assert book.fill("BUY", 8) == ("b3", 101, 7)
assert book.best("BUY") == (100, 10)
assert book.cancel("b1") is True
assert book.best("BUY") is None  # the empty levels are gone
assert book.cancel("b1") is False
assert book.best("SELL") is None
