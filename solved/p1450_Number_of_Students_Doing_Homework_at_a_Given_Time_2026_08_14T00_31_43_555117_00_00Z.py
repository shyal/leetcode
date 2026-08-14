"""
URL: https://leetcode.com/problems/number-of-students-doing-homework-at-a-given-time/description/?envType=problem-list-v2&envId=vn57k9wr

1450. Number of Students Doing Homework at a Given Time

Given two integer arrays startTime and endTime and given an integer queryTime.

The ith student started doing their homework at the time startTime[i] and
finished it at time endTime[i].

Return the number of students doing their homework at time queryTime. More
formally, return the number of students where queryTime lays in the interval
[startTime[i], endTime[i]] inclusive.


Example 1:

Input: startTime = [1,2,3], endTime = [3,2,7], queryTime = 4
Output: 1
Explanation: We have 3 students where:
The first student started doing homework at time 1 and finished at time 3 and wasn't doing anything at time 4.
The second student started doing homework at time 2 and finished at time 2 and also wasn't doing anything at time 4.
The third student started doing homework at time 3 and finished at time 7 and was the only student doing homework at time 4.

Example 2:

Input: startTime = [4], endTime = [4], queryTime = 4
Output: 1
Explanation: The only student was doing their homework at the queryTime.


Constraints:

    startTime.length == endTime.length
    1 <= startTime.length <= 100
    1 <= startTime[i] <= endTime[i] <= 1000
    1 <= queryTime <= 1000
"""


class Solution:
    def busyStudent(self, startTime: List[int], endTime: List[int], queryTime: int) -> int:
        return sum(start <= queryTime <= end for start, end in zip(startTime, endTime))


sol = Solution()

assert sol.busyStudent([1, 2, 3], [3, 2, 7], 4) == 1
assert sol.busyStudent([4], [4], 4) == 1
assert sol.busyStudent([1, 2], [2, 3], 5) == 0
assert sol.busyStudent([2, 3], [4, 5], 1) == 0
assert sol.busyStudent([1, 1, 1], [5, 5, 5], 3) == 3
assert sol.busyStudent([5], [10], 5) == 1
assert sol.busyStudent([1], [5], 5) == 1
assert sol.busyStudent([5], [10], 4) == 0
assert sol.busyStudent([1], [5], 6) == 0
assert sol.busyStudent([1], [1], 1) == 1
assert sol.busyStudent([1000], [1000], 1000) == 1
assert sol.busyStudent([1], [1000], 500) == 1
assert sol.busyStudent([1, 2, 3, 4, 5], [10, 10, 10, 10, 10], 3) == 3
assert sol.busyStudent([1, 3, 5, 7], [2, 4, 6, 8], 4) == 1
assert sol.busyStudent([1] * 100, [1000] * 100, 500) == 100
assert sol.busyStudent([2] * 100, [999] * 100, 1) == 0
assert sol.busyStudent([1, 5, 1, 5], [4, 8, 4, 8], 4) == 2