# REFERENCE: d294 Lost Update
class Solution:
    def __init__(self, balances):
        self.balances = dict(balances)
        self.versions = {}

    def read(self, account):
        return (self.balances.get(account, 0), self.versions.get(account, 1))

    def debit(self, account, amount, version):
        balance, current = self.read(account)
        if version != current or balance < amount:
            return False
        self.balances[account] = balance - amount
        self.versions[account] = current + 1
        return True
