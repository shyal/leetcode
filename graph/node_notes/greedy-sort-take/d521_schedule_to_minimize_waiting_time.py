# REFERENCE: d521 EPI 17.2 Schedule to minimize waiting time
class Solution:
    def minimum_total_waiting_time(self, service_times):
        longest_first = sorted(service_times, reverse=True)
        return sum(t * behind for behind, t in enumerate(longest_first))
