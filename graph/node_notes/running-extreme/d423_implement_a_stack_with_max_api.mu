# REFERENCE: d423 EPI 8.1 Implement a stack with max API
class Solution
  def __init__()
    self.items = []  # (value, largest value at or below it)

  def empty() -> bool
    not self.items

  def max() -> int
    self.items[-1][1]

  def pop() -> int
    self.items.pop()[0]

  def push(x: int) -> none
    self.items <- (x, self.items ? max(x, self.items[-1][1]) : x)
