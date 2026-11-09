"""
EPI 17.2 Schedule to minimize waiting time

Given a list service_times, where service_times[i] is the time customer i
needs, return the smallest total waiting time over all orders of service.
A customer waits for the sum of the service times of the customers served
before it. The total waiting time is the sum of the waits of all customers.

Example 1:

Input: service_times = [4, 1, 3, 2]
Output: 10
Explanation: in the order 1, 2, 3, 4 the waits are 0, 1, 3 and 6. The
order 4, 3, 2, 1 gives the waits 0, 4, 7 and 9, a total of 20.

Example 2:

Input: service_times = [5]
Output: 0

Example 3:

Input: service_times = []
Output: 0

Constraints:

    0 <= len(service_times) <= 10^5
    1 <= service_times[i] <= 10^5

    REQUIRED: O(n log n) time for n customers.
"""


class Solution:
    def minimum_total_waiting_time(self, service_times: list[int]) -> int:
        pass


sol = Solution()

print(sol.minimum_total_waiting_time([4, 1, 3, 2]))  # 10

# assert sol.minimum_total_waiting_time([4, 1, 3, 2]) == 10
# assert sol.minimum_total_waiting_time([5]) == 0
# assert sol.minimum_total_waiting_time([]) == 0
# assert sol.minimum_total_waiting_time([3, 3, 3]) == 9
# assert sol.minimum_total_waiting_time([9, 1]) == 1
# assert sol.minimum_total_waiting_time([1, 9]) == 1
# assert sol.minimum_total_waiting_time([2, 6, 1, 8, 3]) == 22
# assert sol.minimum_total_waiting_time([5, 4, 3, 2, 1]) == 20
# assert sol.minimum_total_waiting_time([1, 2, 3, 4, 5]) == 20
# assert sol.minimum_total_waiting_time([100000, 1]) == 1
# assert sol.minimum_total_waiting_time([1] * 100000) == 4999950000
# assert sol.minimum_total_waiting_time(list(range(100000, 0, -1))) == 166666666650000
