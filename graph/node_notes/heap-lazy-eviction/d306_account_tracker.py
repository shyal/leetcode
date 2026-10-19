# REFERENCE: d306 Account Tracker
class Solution:
    def __init__(self):
        self.balances = {}
        self.top = []

    def apply(self, account, amount):
        self.balances[account] = self.balances.get(account, 0) + amount
        heappush(self.top, (-self.balances[account], account))

    def balance(self, account):
        return self.balances.get(account, 0)

    def richest_account(self):
        while -self.top[0][0] != self.balances[self.top[0][1]]:
            heappop(self.top)
        return self.top[0][1]
