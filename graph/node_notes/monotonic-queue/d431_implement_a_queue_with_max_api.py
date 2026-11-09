# REFERENCE: d431 EPI 8.9 Implement a queue with max API
class Solution:
    def __init__(self):
        self.values, self.candidates = deque(), deque()  # candidates never increase

    def enqueue(self, x):
        self.values.append(x)
        while self.candidates and self.candidates[-1] < x:
            self.candidates.pop()
        self.candidates.append(x)

    def dequeue(self):
        x = self.values.popleft()
        if x == self.candidates[0]:
            self.candidates.popleft()
        return x

    def max(self):
        return self.candidates[0]
