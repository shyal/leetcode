# REFERENCE: d431 EPI 8.9 Implement a queue with max API
class Solution
  def __init__()
    self.values, self.candidates = deque(), deque()  # candidates never increase

  def enqueue(x: int) -> none
    self.values <- x
    while self.candidates and self.candidates[-1] < x
      self.candidates.pop()
    self.candidates <- x

  def dequeue() -> int
    x = self.values.popleft()
    if x == self.candidates[0]
      self.candidates.popleft()
    x

  def max() -> int
    self.candidates[0]
