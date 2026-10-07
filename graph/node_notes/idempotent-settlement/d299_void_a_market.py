# REFERENCE: d299 Void A Market
class Solution:
    def __init__(self, balances, bets, winners):
        self.balances = balances
        self.bets = bets
        self.winners = winners
        self.seen = set()
        self.void_markets = set()

    def void(self, event_id, market):
        if event_id in self.seen:
            return False
        self.seen.add(event_id)
        if market in self.void_markets:
            return False
        self.void_markets.add(market)
        winner = self.winners.pop(market, None)
        for user, selection, stake, odds in self.bets.get(market, []):
            if selection == winner:
                self.balances[user] -= stake * odds
            self.balances[user] += stake
        return True
