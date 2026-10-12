"""
URL: https://leetcode.com/problems/minimum-time-to-make-rope-colorful/description/?envType=problem-list-v2&envId=vn57k9wr

1578. Minimum Time to Make Rope Colorful

Alice has n balloons arranged on a rope. You are given a 0-indexed string colors where colors[i] is the color of the i-th balloon.

Alice wants the rope to be colorful. She does not want two consecutive balloons to be of the same color, so she asks Bob for help. Bob can remove some balloons from the rope to make it colorful. You are given a 0-indexed integer array neededTime where neededTime[i] is the time (in seconds) that Bob needs to remove the i-th balloon from the rope.

Return the minimum time Bob needs to make the rope colorful.

Example 1:

Input: colors = "abaac", neededTime = [1,2,3,4,5]
Output: 3
Explanation: In the above image, 'a' is blue, 'b' is red, and 'c' is green.
Bob can remove the blue balloon at index 2. This takes 3 seconds.
There are no longer two consecutive balloons of the same color. Total time = 3.

Example 2:

Input: colors = "abc", neededTime = [1,2,3]
Output: 0
Explanation: The rope is already colorful. Bob does not need to remove any balloons from the rope.

Example 3:

Input: colors = "aabaa", neededTime = [1,2,3,4,1]
Output: 2
Explanation: Bob will remove the balloons at indices 0 and 4. Each balloon takes 1 second to remove.
There are no longer two consecutive balloons of the same color. Total time = 1 + 1 = 2.

Constraints:

    n == colors.length == neededTime.length
    1 <= n <= 10^5
    1 <= neededTime[i] <= 10^4
    colors contains only lowercase English letters.
---
could this be as simple as finding groups of duplicate, and removing their 
cheapest balloons? if so, a groupby would to the grouping work
then look at groups with more than a count of 1
and move their cheapest duplicates to bring the count
of each group down to 1

LEETCODE: Accepted (267 ms, 35.2 MB)
"""


# mu 0.10
# class Solution
#   def minCost(colors: str, neededTime: [int]) -> int
#     groups = [[a, len(list(b))] for a, b in groupby(enumerate(colors), key= x -> x[1])]
#     offset = 0
#     time = 0
#     for col, count in groups
#       if count > 1
#         total_time = sum(neededTime[offset:offset + count])
#         max_time = next(iter(sorted(neededTime[offset:offset + count], reverse=True)))
#         time += total_time - max_time
#       offset += count
#     time

class Solution:
    def minCost(self, colors: str, neededTime: list[int]) -> int:
        groups = [[a, len(list(b))] for a, b in groupby(enumerate(colors), key=lambda x: x[1])]
        offset = 0
        time = 0
        for col, count in groups:
            if count > 1:
                total_time = sum(neededTime[offset:offset + count])
                max_time = next(iter(sorted(neededTime[offset:offset + count], reverse=True)))
                time += total_time - max_time
            offset += count
        return time


sol = Solution()
print(sol.minCost('abaac', [1, 2, 3, 4, 5]))
_l, _r = sol.minCost('abaac', [1, 2, 3, 4, 5]), 3
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.minCost('abc', [1, 2, 3]), 0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.minCost('aabaa', [1, 2, 3, 4, 1]), 2
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.minCost('a', [1]), 0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.minCost('aa', [1, 1]), 1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.minCost('aa', [1, 100]), 1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.minCost('aaa', [1, 100, 1]), 2
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.minCost('ababab', [1, 1, 1, 1, 1, 1]), 0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.minCost('zzzzzz', [10000, 10000, 10000, 10000, 10000, 10000]), 50000
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.minCost('zzzzzz', [1, 2, 3, 4, 5, 6]), 15
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.minCost('aabbccddeeff', [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]), 36
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.minCost('abcdeffedcba', [1, 2, 3, 4, 5, 6, 6, 5, 4, 3, 2, 1]), 6
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
