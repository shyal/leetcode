# REFERENCE: d522 EPI 17.3 The interval covering problem
class Solution:
    def find_minimum_visits(self, intervals):
        visits, last = 0, -1
        for left, right in sorted(intervals, key=lambda iv: iv[1]):
            if left > last:
                visits, last = visits + 1, right
        return visits
