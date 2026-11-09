# REFERENCE: d480 EPI 13.7 Merging intervals
class Solution:
    def add_interval(self, disjoint_intervals, new_interval):
        left, right = new_interval
        before = [(a, b) for a, b in disjoint_intervals if b < left]
        after = [(a, b) for a, b in disjoint_intervals if a > right]
        for a, b in disjoint_intervals:
            if a <= right and left <= b:
                left, right = min(left, a), max(right, b)
        return before + [(left, right)] + after
