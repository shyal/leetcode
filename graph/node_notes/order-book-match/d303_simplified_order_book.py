# REFERENCE: d303 Simplified Order Book
class Solution:
    def process_orders(self, operations):
        buys, sells = [], []
        left, price_of = {}, {}
        out = []
        for op in operations:
            if op[0] == "ADD":
                _, side, price, quantity = op
                order_id = len(price_of) + 1
                left[order_id] = quantity
                price_of[order_id] = price
                if side == "BUY":
                    heappush(buys, (-price, order_id))
                else:
                    heappush(sells, (price, order_id))
                out.append(order_id)
            elif op[0] == "CANCEL":
                left.pop(op[1], None)
                out.append(None)
            else:
                trades = []
                while True:
                    while buys and buys[0][1] not in left:
                        heappop(buys)
                    while sells and sells[0][1] not in left:
                        heappop(sells)
                    if not buys or not sells or -buys[0][0] < sells[0][0]:
                        break
                    b, s = buys[0][1], sells[0][1]
                    q = min(left[b], left[s])
                    trades.append([b, s, price_of[min(b, s)], q])
                    for i in (b, s):
                        left[i] -= q
                        if not left[i]:
                            del left[i]
                out.append(trades)
        return out
