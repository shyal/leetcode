# REFERENCE: d465 EPI 12.3 Implement an ISBN cache
class Solution:
    def __init__(self, capacity):
        self.capacity = capacity
        self.prices = {}

    def lookup(self, isbn):
        if isbn not in self.prices:
            return -1
        self.prices[isbn] = self.prices.pop(isbn)
        return self.prices[isbn]

    def insert(self, isbn, price):
        if isbn in self.prices:
            price = self.prices.pop(isbn)
        elif len(self.prices) == self.capacity:
            del self.prices[next(iter(self.prices))]
        self.prices[isbn] = price

    def erase(self, isbn):
        return self.prices.pop(isbn, None) is not None
