# REFERENCE: d496 EPI 14.11 Add credits
class Solution
  def __init__() -> none
    self.offset = 0
    self.credit = {}
    self.heap = []

  def insert(client_id: str, c: int) -> none
    self.credit[client_id] = c - self.offset
    heappush(self.heap, (self.offset - c, client_id))

  def remove(client_id: str) -> bool
    self.credit.pop(client_id, none) is not none

  def lookup(client_id: str) -> int
    client_id in self.credit ? self.credit[client_id] + self.offset : -1

  def add_all(C: int) -> none
    self.offset += C

  def max() -> str
    while self.heap and self.credit.get(self.heap[0][1]) != -self.heap[0][0]
      heappop(self.heap)
    self.heap ? self.heap[0][1] : ""
