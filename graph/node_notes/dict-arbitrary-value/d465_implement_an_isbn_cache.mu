# REFERENCE: d465 EPI 12.3 Implement an ISBN cache
class Solution
  def __init__(capacity: int)
    self.capacity = capacity
    self.prices = {}

  def lookup(isbn: int) -> int
    if isbn not in self.prices
      return -1
    self.prices[isbn] = self.prices.pop(isbn)
    self.prices[isbn]

  def insert(isbn: int, price: int) -> none
    if isbn in self.prices
      price = self.prices.pop(isbn)
    elif len(self.prices) == self.capacity
      del self.prices[next(iter(self.prices))]
    self.prices[isbn] = price

  def erase(isbn: int) -> bool
    self.prices.pop(isbn, none) is not none
