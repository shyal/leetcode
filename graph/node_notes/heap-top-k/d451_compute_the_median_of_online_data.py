# REFERENCE: d451 EPI 10.5 Compute the median of online data
class Solution:
    def online_median(self, sequence):
        low, high, out = [], [], []
        for x in sequence:
            maxheappush(low, x)
            heappush(high, maxheappop(low))
            if len(high) > len(low):
                maxheappush(low, heappop(high))
            out.append(float(low[0]) if len(low) > len(high) else (low[0] + high[0]) / 2)
        return out
