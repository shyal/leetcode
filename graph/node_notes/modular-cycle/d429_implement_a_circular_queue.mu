# REFERENCE: d429 EPI 8.7 Implement a circular queue
class Solution
  def __init__(capacity: int)
    self.values = [0] * capacity
    self.head = self.count = 0

  def enqueue(x: int) -> none
    if self.count == len(self.values)
      n, h = len(self.values), self.head
      self.values = self.values[h:] + self.values[:h] + [0] * n
      self.head = 0
    self.values[(self.head + self.count) % len(self.values)] = x
    self.count += 1

  def dequeue() -> int
    x = self.values[self.head]
    self.head = (self.head + 1) % len(self.values)
    self.count -= 1
    x

  def size() -> int
    self.count
