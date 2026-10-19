# REFERENCE: d304 Betting Exchange Settlement
class Solution:
    def settle_market(self, operations):
        backs, lays = [], []
        matched = []
        pnl = {}
        for seq, op in enumerate(operations):
            if op[0] == "SETTLE":
                won = op[1]
                break
            _, user, side, odds, stake = op
            pnl[user] = 0
            if side == "BACK":
                book, crosses = lays, lambda w: w >= odds
            else:
                book, crosses = backs, lambda w: w <= odds
            while stake and book and crosses(book[0][3]):
                rest = book[0]
                fill = min(stake, rest[4])
                if side == "BACK":
                    matched.append((user, rest[2], rest[3], fill))
                else:
                    matched.append((rest[2], user, rest[3], fill))
                stake -= fill
                rest[4] -= fill
                if not rest[4]:
                    heappop(book)
            if stake:
                if side == "BACK":
                    heappush(backs, [odds, seq, user, odds, stake])
                else:
                    heappush(lays, [-odds, seq, user, odds, stake])
        for backer, layer, o, s in matched:
            amount = (s // 100) * (o - 100) if won else -s
            pnl[backer] += amount
            pnl[layer] -= amount
        return [[u, pnl[u]] for u in sorted(pnl)]
