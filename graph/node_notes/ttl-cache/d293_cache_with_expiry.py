# REFERENCE: d293 Cache With Expiry
class Solution:
    def __init__(self):
        self.values = {}
        self.expiry = {}
        self.heap = []

    def set(self, key, value, ttl, now):
        self.values[key] = value
        self.expiry[key] = now + ttl
        heappush(self.heap, (now + ttl, key))

    def get(self, key, now):
        if key not in self.values:
            return None
        if now >= self.expiry[key]:
            del self.values[key]
            del self.expiry[key]
            return None
        return self.values[key]

    def expire(self, now):
        removed = 0
        while self.heap and self.heap[0][0] <= now:
            at, key = heappop(self.heap)
            if self.expiry.get(key) == at:
                del self.values[key]
                del self.expiry[key]
                removed += 1
        return removed

    def size(self):
        return len(self.values)
