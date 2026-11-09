# REFERENCE: d496 EPI 14.11 Add credits
class Solution:
    def __init__(self):
        self.offset = 0
        self.credit = {}
        self.heap = []

    def insert(self, client_id, c):
        self.credit[client_id] = c - self.offset
        heappush(self.heap, (self.offset - c, client_id))

    def remove(self, client_id):
        return self.credit.pop(client_id, None) is not None

    def lookup(self, client_id):
        return self.credit[client_id] + self.offset if client_id in self.credit else -1

    def add_all(self, C):
        self.offset += C

    def max(self):
        while self.heap and self.credit.get(self.heap[0][1]) != -self.heap[0][0]:
            heappop(self.heap)
        return self.heap[0][1] if self.heap else ""
