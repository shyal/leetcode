"""
URL: https://leetcode.com/problems/daily-temperatures/description/?envType=problem-list-v2&envId=vn57k9wr

739. Daily Temperatures

Given an array of integers temperatures represents the daily temperatures, return
an array answer such that answer[i] is the number of days you have to wait after
the ith day to get a warmer temperature. If there is no future day for which this
is possible, keep answer[i] == 0 instead.


Example 1:

Input: temperatures = [73,74,75,71,69,72,76,73]
Output: [1,1,4,2,1,1,0,0]

Example 2:

Input: temperatures = [30,40,50,60]
Output: [1,1,1,0]

Example 3:

Input: temperatures = [30,60,90]
Output: [1,1,0]


Constraints:

    1 <= temperatures.length <= 10^5
    30 <= temperatures[i] <= 100
"""

from dsa.monotonic_stack import MonotonicStack, Type


class Solution:
    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:
        res = [0] * len(temperatures)
        stack = MonotonicStack(Type.decreasing)
        for i, temp in enumerate(temperatures):
            for _, j in stack.push((temp, i)):
                res[j] = i - j
        return res



sol = Solution()

# print(sol.dailyTemperatures([73, 74, 75, 71, 69, 72, 76, 73]))  # [1,1,4,2,1,1,0,0]

assert sol.dailyTemperatures([73, 74, 75, 71, 69, 72, 76, 73]) == [1, 1, 4, 2, 1, 1, 0, 0]
assert sol.dailyTemperatures([30, 40, 50, 60]) == [1, 1, 1, 0]
assert sol.dailyTemperatures([30, 60, 90]) == [1, 1, 0]

assert sol.dailyTemperatures([30]) == [0]
assert sol.dailyTemperatures([100]) == [0]
assert sol.dailyTemperatures([30, 31]) == [1, 0]
assert sol.dailyTemperatures([31, 30]) == [0, 0]
assert sol.dailyTemperatures([30, 30]) == [0, 0]
assert sol.dailyTemperatures([30, 30, 30]) == [0, 0, 0]
assert sol.dailyTemperatures([30, 30, 31]) == [2, 1, 0]
assert sol.dailyTemperatures([90, 80, 70, 60]) == [0, 0, 0, 0]
assert sol.dailyTemperatures([100, 100, 100, 30]) == [0, 0, 0, 0]
assert sol.dailyTemperatures([30, 100, 30, 100]) == [1, 0, 1, 0]
assert sol.dailyTemperatures([45, 44, 45]) == [0, 1, 0]
assert sol.dailyTemperatures([70, 70, 71, 71, 72]) == [2, 1, 2, 1, 0]
assert sol.dailyTemperatures([50, 40, 30, 40, 50, 60]) == [5, 3, 1, 1, 1, 0]
assert sol.dailyTemperatures([55, 38, 53, 81, 61, 93, 97, 32, 43, 78]) == [3, 1, 1, 2, 1, 1, 0, 1, 1, 0]

assert sol.dailyTemperatures(list(range(30, 101))) == [1] * 70 + [0]
assert sol.dailyTemperatures(list(range(100, 29, -1))) == [0] * 71
assert sol.dailyTemperatures([30, 100] * 5) == [1, 0] * 5

_ramp = list(range(30, 101)) + list(range(99, 29, -1))
# assert sol.dailyTemperatures(_ramp) == [1] * 70 + [0] * 71

_original = [73, 74, 75, 71, 69, 72, 76, 73]
_copy = list(_original)
sol.dailyTemperatures(_copy)
# assert _copy == _original

_big = [30] * 99999 + [31]
# assert sol.dailyTemperatures(_big) == [99999 - i for i in range(99999)] + [0]

_flat = [100] * 100000
# assert sol.dailyTemperatures(_flat) == [0] * 100000

_alt = [30, 31] * 50000
_alt_expected = [1, 0] * 50000
# assert sol.dailyTemperatures(_alt) == _alt_expected

for _case in ([30], [30, 40, 50, 60], [50, 40, 30, 40, 50, 60], [55, 38, 53, 81, 61, 93, 97, 32, 43, 78]):
    _ans = sol.dailyTemperatures(_case)
    # assert len(_ans) == len(_case)
    for _i, _wait in enumerate(_ans or []):
        if _wait == 0:
            # assert all(_t <= _case[_i] for _t in _case[_i + 1:])
            pass
        else:
            # assert _case[_i + _wait] > _case[_i]
            # assert all(_t <= _case[_i] for _t in _case[_i + 1:_i + _wait])
            pass