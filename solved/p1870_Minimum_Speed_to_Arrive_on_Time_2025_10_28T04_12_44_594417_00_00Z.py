"""
URL: https://leetcode.com/problems/minimum-speed-to-arrive-on-time/description/?envType=problem-list-v2&envId=vn57k9wr

1870. Minimum Speed to Arrive on Time

You are given a floating-point number hour, representing the amount of time you have to reach the office. To commute to the office, you must take n trains in sequential order. You are also given an integer array dist of length n, where dist[i] describes the distance (in kilometers) of the ith train ride.

Each train can only depart at an integer hour, so you may need to wait in between each train ride.

- For example, if the 1st train ride takes 1.5 hours, you must wait for an additional 0.5 hours before you can depart on the 2nd train ride at the 2 hour mark.

Return the minimum positive integer speed (in kilometers per hour) that all the trains must travel at for you to reach the office on time, or -1 if it is impossible to be on time.

Tests are generated such that the answer will not exceed 10^7 and hour will have at most two digits after the decimal point.


Example 1:

Input: dist = [1,3,2], hour = 6
Output: 1
Explanation: At speed 1:
- The first train ride takes 1/1 = 1 hour.
- Since we are already at an integer hour, we depart immediately at the 1 hour mark. The second train takes 3/1 = 3 hours.
- Since we are already at an integer hour, we depart immediately at the 4 hour mark. The third train takes 2/1 = 2 hours.
- You will arrive at exactly the 6 hour mark.

Example 2:

Input: dist = [1,3,2], hour = 2.7
Output: 3
Explanation: At speed 3:
- The first train ride takes 1/3 = 0.33333 hours.
- Since we are not at an integer hour, we wait until the 1 hour mark to depart. The second train ride takes 3/3 = 1 hour.
- Since we are already at an integer hour, we depart immediately at the 2 hour mark. The third train takes 2/3 = 0.66667 hours.
- You will arrive at the 2.66667 hour mark.

Example 3:

Input: dist = [1,3,2], hour = 1.9
Output: -1
Explanation: It is impossible because the earliest the third train can depart is at the 2 hour mark.


Constraints:

    n == dist.length
    1 <= n <= 10^5
    1 <= dist[i] <= 10^5
    1 <= hour <= 10^9
    There will be at most two digits after the decimal point in hour.

---

This question is beating the life out of me. I want to read the solution.
This is not my solution.

I was able to come up with the travelTime check, for example, computing
`high` was above and beyond me.

"""


class Solution:

    def travelTime(self, dist, speed):
        ceil = lambda a, b: (a + b - 1) // b
        return sum(
            ceil(d, speed) if i < len(dist) - 1 else d / speed
            for i, d in enumerate(dist)
        )

    def minSpeedOnTime(self, dist: List[int], hour: float) -> int:
        n = len(dist)
        if hour <= n - 1:
            return -1
        high = max(10**7, int(dist[-1] / (hour - (n - 1))) + 1)
        low = 1
        result = -1
        while low <= high:
            speed = low + (high - low) // 2
            if self.travelTime(dist, speed) <= hour:
                result = speed
                high = speed - 1
            else:
                low = speed + 1
        return result


sol = Solution()
assert sol.minSpeedOnTime(dist=[1, 3, 2], hour=6) == 1
assert sol.minSpeedOnTime(dist=[1, 3, 2], hour=2.7) == 3
assert sol.minSpeedOnTime(dist=[1, 3, 2], hour=1.9) == -1
assert sol.minSpeedOnTime(dist=[1], hour=1.0) == 1
assert sol.minSpeedOnTime(dist=[5], hour=2.0) == 3
assert sol.minSpeedOnTime(dist=[1, 1], hour=1.0) == -1
assert sol.minSpeedOnTime(dist=[1, 1], hour=1.1) == 10
assert sol.minSpeedOnTime(dist=[1, 1], hour=1.01) == 100
assert sol.minSpeedOnTime(dist=[1, 1], hour=1.001) == 1000
assert sol.minSpeedOnTime(dist=[1, 100], hour=1.01) == 10000
assert sol.minSpeedOnTime(dist=[1, 1, 1], hour=2.0001) == 10000
assert sol.minSpeedOnTime(dist=[1, 1, 1, 1, 1], hour=4.001) == 1000
assert sol.minSpeedOnTime([1, 3, 2], 6) == 1
assert sol.minSpeedOnTime([1, 3, 2], 2.7) == 3
assert sol.minSpeedOnTime([1, 3, 2], 1.9) == -1
assert sol.minSpeedOnTime([1], 1) == 1
assert sol.minSpeedOnTime([1], 0.5) == 2
assert sol.minSpeedOnTime([1, 1, 1, 1, 1], 5) == 1
assert sol.minSpeedOnTime([1, 1, 1, 1, 1], 1.1) == -1

# commented as some of these are slow

# assert sol.minSpeedOnTime([10000, 10000], 20000) == 1
# assert sol.minSpeedOnTime([10000, 10000], 1.5) == 20000
# assert sol.minSpeedOnTime([1, 1, 100000], 100002) == 1
assert sol.minSpeedOnTime([1, 2, 3, 4, 5], 7.9) == 3
# assert sol.minSpeedOnTime([1] * 100000, 100000) == 1
# assert sol.minSpeedOnTime([1, 100000], 100000.0) == 2
# assert sol.minSpeedOnTime(dist=[1, 100000], hour=1.00001) == 10000000000
