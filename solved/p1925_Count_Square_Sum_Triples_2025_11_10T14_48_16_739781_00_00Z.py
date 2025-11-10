"""
URL: https://leetcode.com/problems/count-square-sum-triples/description/?envType=problem-list-v2&envId=vn57k9wr

1925. Count Square Sum Triples

A square triple (a,b,c) is a triple where a, b, and c are integers and a^2 + b^2 = c^2.

Given an integer n, return the number of square triples such that 1 <= a, b, c <= n.

Example 1:

Input: n = 5
Output: 2
Explanation: The square triples are (3,4,5) and (4,3,5).

Example 2:

Input: n = 10
Output: 4
Explanation: The square triples are (3,4,5), (4,3,5), (6,8,10), and (8,6,10).

Constraints:

    1 <= n <= 250
"""


class Solution:
    def countTriples(self, n: int) -> int:
        res = 0
        for a, b, c in combinations([x**2 for x in range(1, n + 1)], 3):
            res += (a + b) == c
        return res * 2


sol = Solution()

# print(sol.countTriples(5))  # 2


sol.countTriples(219)
assert sol.countTriples(5) == 2
assert sol.countTriples(10) == 4
assert sol.countTriples(1) == 0
assert sol.countTriples(2) == 0
assert sol.countTriples(3) == 0
assert sol.countTriples(4) == 0
assert sol.countTriples(6) == 2
assert sol.countTriples(13) == 6
assert sol.countTriples(15) == 8
assert sol.countTriples(17) == 10
assert sol.countTriples(25) == 16
