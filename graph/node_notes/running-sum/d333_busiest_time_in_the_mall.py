# REFERENCE: d333 Busiest Time in The Mall
class Solution:
    def find_busiest_period(self, data):
        count, best, best_time = 0, -inf, 0
        for i, (time, visitors, entered) in enumerate(data):
            count += visitors if entered else -visitors
            if i + 1 < len(data) and data[i + 1][0] == time:
                continue
            if count > best:
                best, best_time = count, time
        return best_time
