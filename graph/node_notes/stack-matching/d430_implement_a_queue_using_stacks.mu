# REFERENCE: d430 EPI 8.8 Implement a queue using stacks
class Solution
  def __init__()
    self.inbox, self.outbox = [], []

  def enqueue(x: int) -> none
    self.inbox <- x

  def dequeue() -> int
    if not self.outbox
      while self.inbox
        self.outbox <- self.inbox.pop()
    self.outbox.pop()
