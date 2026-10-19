# REFERENCE: d305 Settle Matched Bets
class Solution:
    def settle_market(self, operations):
        pnl = {}
        won = operations[-1][1]
        for _, backer, layer, odds, stake in operations[:-1]:
            amount = (stake // 100) * (odds - 100) if won else -stake
            pnl[backer] = pnl.get(backer, 0) + amount
            pnl[layer] = pnl.get(layer, 0) - amount
        return [[user, pnl[user]] for user in sorted(pnl)]
