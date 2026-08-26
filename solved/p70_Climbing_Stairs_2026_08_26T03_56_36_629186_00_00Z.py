"""
URL: https://leetcode.com/problems/climbing-stairs/description/?envType=problem-list-v2&envId=vn57k9wr

70. Climbing Stairs

You are climbing a staircase. It takes n steps to reach the top.

Each time you can either climb 1 or 2 steps. In how many distinct ways can you climb to the top?

Example 1:

Input: n = 2
Output: 2
Explanation:
There are two ways to climb to the top.
1. 1 step + 1 step
2. 2 steps

Example 2:

Input: n = 3
Output: 3
Explanation:
There are three ways to climb to the top.
1. 1 step + 1 step + 1 step
2. 1 step + 2 steps
3. 2 steps + 1 step

Constraints:

    1 <= n <= 45
"""


class Solution:
    def climbStairs(self, n: int) -> int:
        @cache
        def fib(n):
            if n <= 3:
                return n
            return fib(n - 1) + fib(n - 2)

        return fib(n)


sol = Solution()

print(sol.climbStairs(2))  # 2

assert sol.climbStairs(2) == 2
assert sol.climbStairs(3) == 3

assert sol.climbStairs(1) == 1
assert sol.climbStairs(45) == 1836311903
assert sol.climbStairs(10) == 89
assert sol.climbStairs(20) == 10946
assert sol.climbStairs(30) == 1346269
assert sol.climbStairs(40) == 165580141
assert sol.climbStairs(4) == 5
assert sol.climbStairs(5) == 8
assert sol.climbStairs(6) == 13
assert sol.climbStairs(7) == 21
assert sol.climbStairs(8) == 34
assert sol.climbStairs(9) == 55
