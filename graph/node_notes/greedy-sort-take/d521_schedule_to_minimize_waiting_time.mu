# REFERENCE: d521 EPI 17.2 Schedule to minimize waiting time
class Solution
  def minimum_total_waiting_time(service_times: [int]) -> int
    sum for >behind, t in sort(service_times, reverse=true): t * behind
