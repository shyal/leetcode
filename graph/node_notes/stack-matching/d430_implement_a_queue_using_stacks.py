# REFERENCE: d430 EPI 8.8 Implement a queue using stacks
class Solution:
    def __init__(self):
        self.inbox, self.outbox = [], []

    def enqueue(self, x):
        self.inbox.append(x)

    def dequeue(self):
        if not self.outbox:
            while self.inbox:
                self.outbox.append(self.inbox.pop())
        return self.outbox.pop()
