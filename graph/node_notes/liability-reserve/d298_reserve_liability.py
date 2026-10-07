# REFERENCE: d298 Reserve Liability
class Solution:
    def __init__(self, balances):
        self.balances = balances
        self.reserved = defaultdict(int)
        self.orders = {}

    def available(self, user):
        return self.balances.get(user, 0) - self.reserved[user]

    def place(self, order_id, user, side, stake, odds):
        risk = stake if side == "BACK" else stake * (odds - 1)
        if order_id in self.orders or risk > self.available(user):
            return False
        self.orders[order_id] = (user, risk)
        self.reserved[user] += risk
        return True

    def cancel(self, order_id):
        if order_id not in self.orders:
            return False
        user, risk = self.orders.pop(order_id)
        self.reserved[user] -= risk
        return True
