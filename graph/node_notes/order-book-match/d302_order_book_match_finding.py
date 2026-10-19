# REFERENCE: d302 Order Book Match Finding
class Solution:
    def process_orders(self, orders):
        books = {"buy": [], "sell": []}
        trades = []
        for seq, o in enumerate(orders):
            side, price, qty = o["side"], o["price"], o["quantity"]
            book = books["sell" if side == "buy" else "buy"]
            while qty and book and (book[0][3] <= price if side == "buy" else book[0][3] >= price):
                rest = book[0]
                fill = min(qty, rest[4])
                trades.append({"maker_id": rest[2], "taker_id": o["id"], "price": rest[3], "quantity": fill})
                qty -= fill
                rest[4] -= fill
                if not rest[4]:
                    heappop(book)
            if qty:
                heappush(books[side], [-price if side == "buy" else price, seq, o["id"], price, qty])
        remaining = [
            {"id": e[2], "side": s, "price": e[3], "quantity": e[4]} for s in ("buy", "sell") for e in sorted(books[s])
        ]
        return {"trades": trades, "remaining": remaining}
