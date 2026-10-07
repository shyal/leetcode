# REFERENCE: d297 Hits In The Last Minute
class Solution:
    def __init__(self, window):
        self.window = window
        self.hits = defaultdict(deque)

    def hit(self, user, now):
        q = self.hits[user]
        while q and q[0] <= now - self.window:
            q.popleft()
        q.append(now)
        return len(q)
