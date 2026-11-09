# REFERENCE: d479 EPI 13.6 Render a calendar
class Solution:
    def find_max_simultaneous_events(self, A):
        events = sorted([(s, 0) for s, _ in A] + [(f, 1) for _, f in A])
        best = count = 0
        for _, is_finish in events:
            count += -1 if is_finish else 1
            best = max(best, count)
        return best
