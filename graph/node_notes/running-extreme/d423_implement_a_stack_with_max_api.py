# REFERENCE: d423 EPI 8.1 Implement a stack with max API
class Solution:
    def __init__(self):
        self.items = []  # (value, largest value at or below it)

    def empty(self):
        return not self.items

    def max(self):
        return self.items[-1][1]

    def pop(self):
        return self.items.pop()[0]

    def push(self, x):
        self.items.append((x, max(x, self.items[-1][1]) if self.items else x))
