"""
URL: https://leetcode.com/problems/check-if-all-the-integers-in-a-range-are-covered/description/?envType=problem-list-v2&envId=vn57k9wr

1893. Check if All the Integers in a Range Are Covered

You are given a 2D integer array ranges and two integers left and right. Each ranges[i] = [start_i, end_i] represents an inclusive interval between start_i and end_i.

Return true if each integer in the inclusive range [left, right] is covered by at least one interval in ranges. Return false otherwise.

An integer x is covered by an interval ranges[i] = [start_i, end_i] if start_i <= x <= end_i.

Example 1:

Input: ranges = [[1,2],[3,4],[5,6]], left = 2, right = 5
Output: true
Explanation: Every integer between 2 and 5 is covered:
- 2 is covered by the first range.
- 3 and 4 are covered by the second range.
- 5 is covered by the third range.

Example 2:

Input: ranges = [[1,10],[10,20]], left = 21, right = 21
Output: false
Explanation: 21 is not covered by any range.

Constraints:

    1 <= ranges.length <= 50
    1 <= start_i <= end_i <= 50
    1 <= left <= right <= 50
"""


class Solution:
    def isCovered(self, ranges: List[List[int]], left: int, right: int) -> bool:
        numbers = set([*range(left, right + 1)])
        for start, end in ranges:
            rnums = set([*range(start, end + 1)])
            numbers -= rnums
        return len(numbers) == 0


sol = Solution()

print(sol.isCovered([[1, 2], [3, 4], [5, 6]], 2, 5))  # True

assert sol.isCovered([[1, 2], [3, 4], [5, 6]], 2, 5) == True
assert sol.isCovered([[1, 10], [10, 20]], 21, 21) == False

assert sol.isCovered([[1, 50]], 1, 50) == True
assert sol.isCovered([[1, 25], [26, 50]], 1, 50) == True
assert sol.isCovered([[1, 10], [20, 30], [40, 50]], 15, 25) == False
assert sol.isCovered([[1, 10], [20, 30], [40, 50]], 10, 20) == False
assert sol.isCovered([[5, 5]], 5, 5) == True
assert sol.isCovered([[1, 2], [2, 3], [3, 4], [4, 5]], 1, 5) == True
assert sol.isCovered([[1, 1], [3, 3], [5, 5]], 1, 5) == False
assert sol.isCovered([[10, 20], [15, 25], [20, 30]], 10, 30) == True
assert sol.isCovered([[1, 50]], 25, 25) == True
assert sol.isCovered([[1, 10], [12, 20]], 10, 12) == False
assert sol.isCovered([[1, 10], [12, 20]], 11, 11) == False
assert sol.isCovered([[1, 1], [2, 2], [3, 3], [4, 4], [5, 5]], 1, 5) == True
