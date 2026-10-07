# REFERENCE: d291 Settle Once
class Solution:
    def __init__(self, balances, bets):
        self.balances = balances
        self.bets = bets
        self.seen = set()
        self.winner = {}

    def settle(self, event_id, market, winner):
        if event_id in self.seen:
            return False
        self.seen.add(event_id)
        if market in self.winner:
            return False
        self.winner[market] = winner
        for user, selection, stake, odds in self.bets.get(market, []):
            if selection == winner:
                self.balances[user] += stake * odds
        return True
