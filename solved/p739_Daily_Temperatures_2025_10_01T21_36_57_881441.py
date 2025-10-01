"""
URL: https://leetcode.com/problems/daily-temperatures/description/?envType=study-plan-v2&envId=leetcode-75

739. Daily Temperatures

Given an array of integers temperatures represents the daily temperatures, return an array answer such that answer[i] is the number of days you have to wait after the ith day to get a warmer temperature. If there is no future day for which this is possible, keep answer[i] == 0 instead.


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

        1 <= temperatures.length <= 105
        30 <= temperatures[i] <= 100
"""

from typing import List


class Solution:
    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:
        stack = []
        answer = [0] * len(temperatures)
        for i, temp in enumerate(temperatures):
            if not stack:
                stack.append((temp, i))
            elif stack[-1][0] < temp:
                while stack and stack[-1][0] < temp:
                    j_temp, j = stack.pop()
                    answer[j] = i - j
                stack.append((temp, i))
            else:
                stack.append((temp, i))
        return answer


sol = Solution()

res = sol.dailyTemperatures(temperatures=[73, 74, 75, 71, 69, 72, 76, 73])
assert res == [1, 1, 4, 2, 1, 1, 0, 0]


res = sol.dailyTemperatures(temperatures=[30, 40, 50, 60])
assert res == [1, 1, 1, 0]

res = sol.dailyTemperatures(temperatures=[30, 60, 90])
assert res == [1, 1, 0]

res = sol.dailyTemperatures(temperatures=[50])
assert res == [0]

res = sol.dailyTemperatures(temperatures=[70, 70, 70, 70])
assert res == [0, 0, 0, 0]

res = sol.dailyTemperatures(temperatures=[30, 40, 50, 60, 70])
assert res == [1, 1, 1, 1, 0]

res = sol.dailyTemperatures(temperatures=[100, 90, 80, 70, 60])
assert res == [0, 0, 0, 0, 0]

res = sol.dailyTemperatures(temperatures=[73, 74, 73, 74])
assert res == [1, 0, 1, 0]

res = sol.dailyTemperatures(temperatures=[80, 70, 60, 70, 80])
assert res == [0, 3, 1, 1, 0]

res = sol.dailyTemperatures(temperatures=[60, 70, 80, 70, 60])
assert res == [1, 1, 0, 0, 0]

res = sol.dailyTemperatures(temperatures=[50, 60, 50, 60, 50])
assert res == [1, 0, 1, 0, 0]

res = sol.dailyTemperatures(temperatures=[30, 100, 30])
assert res == [1, 0, 0]

res = sol.dailyTemperatures(temperatures=[90, 80])
assert res == [0, 0]
