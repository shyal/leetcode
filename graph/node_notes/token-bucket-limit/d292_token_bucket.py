# REFERENCE: d292 Token Bucket
class Solution:
    def __init__(self, capacity, rate):
        self.capacity = capacity
        self.rate = rate
        self.tokens = {}
        self.last = {}

    def allow(self, user, now):
        if user not in self.tokens:
            self.tokens[user] = self.capacity
            self.last[user] = now
        refill = (now - self.last[user]) * self.rate
        self.tokens[user] = min(self.capacity, self.tokens[user] + refill)
        self.last[user] = now
        if self.tokens[user] >= 1:
            self.tokens[user] -= 1
            return True
        return False
