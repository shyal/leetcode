"""
URL: https://leetcode.com/problems/count-pairs-that-form-a-complete-day-i/description/?envType=problem-list-v2&envId=vn57k9wr

3184. Count Pairs That Form a Complete Day I

Given an integer array hours representing times in hours, return an integer denoting the number of pairs i, j where i < j and hours[i] + hours[j] forms a complete day.

A complete day is defined as a time duration that is an exact multiple of 24 hours.

For example, 1 day is 24 hours, 2 days is 48 hours, 3 days is 72 hours, and so on.

Example 1:

Input: hours = [12,12,30,24,24]
Output: 2
Explanation: The pairs of indices that form a complete day are (0, 1) and (3, 4).

Example 2:

Input: hours = [72,48,24,3]
Output: 3
Explanation: The pairs of indices that form a complete day are (0, 1), (0, 2), and (1, 2).

Constraints:

    1 <= hours.length <= 100
    1 <= hours[i] <= 10^9
"""


class Solution:
    def countCompleteDayPairs(self, hours: List[int]) -> int:
        return sum(
            i < j and (hours[i] + hours[j]) % 24 == 0
            for i, j in combinations(range(len(hours)), 2)
        )


sol = Solution()

assert sol.countCompleteDayPairs([12, 12, 30, 24, 24]) == 2
assert sol.countCompleteDayPairs([72, 48, 24, 3]) == 3
assert sol.countCompleteDayPairs([1]) == 0
assert sol.countCompleteDayPairs([1, 23]) == 1
assert sol.countCompleteDayPairs([1, 1]) == 0
assert sol.countCompleteDayPairs([24, 48, 72]) == 3
assert sol.countCompleteDayPairs([12, 36, 60]) == 3
assert sol.countCompleteDayPairs([3, 21, 3, 21]) == 4
assert sol.countCompleteDayPairs([13, 11]) == 1
assert sol.countCompleteDayPairs([16, 8]) == 1
assert sol.countCompleteDayPairs([12, 24]) == 0
assert sol.countCompleteDayPairs([24, 48, 12, 36]) == 2
assert sol.countCompleteDayPairs([2, 2, 2, 22, 22]) == 6
assert sol.countCompleteDayPairs([1000000000, 8]) == 1
assert sol.countCompleteDayPairs([1000000000]) == 0
assert sol.countCompleteDayPairs([16, 16, 16]) == 0
