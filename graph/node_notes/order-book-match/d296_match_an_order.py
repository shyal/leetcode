# REFERENCE: d296 Match An Order
class Solution(OrderBook):
    def place(self, order_id, side, price, qty):
        if order_id in self.orders:
            return []
        other = "SELL" if side == "BUY" else "BUY"
        fills = []
        while qty > 0:
            top = self.best(other)
            if top is None:
                break
            if side == "BUY" and top[0] > price:
                break
            if side == "SELL" and top[0] < price:
                break
            rest_id, at, taken = self.fill(other, qty)
            qty -= taken
            if side == "BUY":
                fills.append((order_id, rest_id, at, taken))
            else:
                fills.append((rest_id, order_id, at, taken))
        self.add(order_id, side, price, qty)
        return fills
