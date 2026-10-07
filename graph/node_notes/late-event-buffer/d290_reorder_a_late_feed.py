# REFERENCE: d290 Reorder A Late Feed
class Solution:
    def __init__(self, lateness):
        self.lateness = lateness
        self.heap = []
        self.count = 0
        self.watermark = None
        self.late = 0

    def push(self, ts, value):
        if self.watermark is not None and ts < self.watermark:
            self.late += 1
            return []
        self.count += 1
        heappush(self.heap, (ts, self.count, value))
        mark = ts - self.lateness
        if self.watermark is None or mark > self.watermark:
            self.watermark = mark
        out = []
        while self.heap and self.heap[0][0] < self.watermark:
            t, _, v = heappop(self.heap)
            out.append((t, v))
        return out

    def flush(self):
        out = []
        while self.heap:
            t, _, v = heappop(self.heap)
            out.append((t, v))
        return out

    def dropped(self):
        return self.late
