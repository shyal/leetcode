# REFERENCE: d197 Withdraw
class InsufficientFunds(Exception):
    def __init__(self, needed):
        super().__init__(f"short by {needed}")
        self.needed = needed


class Solution:
    def withdraw(self, balance, amount):
        if amount > balance:
            raise InsufficientFunds(amount - balance)
        return balance - amount
