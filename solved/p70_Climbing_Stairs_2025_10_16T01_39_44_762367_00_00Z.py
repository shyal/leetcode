"""
URL: https://leetcode.com/problems/climbing-stairs/description/

70. Climbing Stairs

You are climbing a staircase. It takes n steps to reach the top.

Each time you can either climb 1 or 2 steps. In how many distinct ways can you climb to the top?


Example 1:

Input: n = 2
Output: 2
Explanation: There are two ways to climb to the top.
1. 1 step + 1 step
2. 2 steps

Example 2:

Input: n = 3
Output: 3
Explanation: There are three ways to climb to the top.
1. 1 step + 1 step + 1 step
2. 1 step + 2 steps
3. 2 steps + 1 step


Constraints:

        1 <= n <= 45

---

Alright so i'm not too sure how this template applies to this problem, so
let's work through this problem step by step (pun intended).


              5
             ___
          3 |
         ---
     2  |
    ---
 1 |
---

- on step 1, there's only one way of getting there
- on step 2, there's two ways, i.e 1+1 or 2
- on step 3, there's 3 ways of getting there: 1+1+1, 2+1, 1+2
- on step 4, there's at least 5 ways i can count getting there: 1+1+1+1, 1+1+2, 1+2+1, 2+2+1+1, 2+2

Ok the pattern looks like fibbonacci. So we could compute fib using DP. I pasted in the template (lcdpbottomup):

def dp_problem(self, nums: List[int], target: int) -> int:  # Adapt params to your problem
    # Step 1: Define DP array (dp[i] = optimal for first i elements or value i)
    n = len(nums)  # Or target + 1 for amount-based (e.g., Coin Change)
    dp = [sys.maxsize] * (n + 1)  # Or [0] * (n + 1); use maxsize for min, 0 for max/count
    dp[0] = 0  # Base case: dp[0] is often 0 (empty/no cost)

    # Step 2: Fill DP table bottom-up
    for i in range(1, n + 1):  # Or range(1, target + 1) for amount-based
        # For each i, compute min/max from previous states
        for choice in nums:  # Or range(i) for subsequence (e.g., LIS)
            if i - choice >= 0:  # Valid transition? (e.g., coin <= amount)
                # Transition: dp[i] = min/max(dp[i], dp[i - choice] + 1)  # Adapt +1/-cost/etc.
                dp[i] = min(dp[i], dp[i - choice] + 1)  # Example for min coins

    # Step 3: Return result (dp[n] or dp[target]; handle impossible cases)
    return dp[n] if dp[n] != sys.maxsize else -1  # Adapt for your problem

I ended up getting rid of most of it, but i guess it provided a starting point.
"""


class Solution:
    def climbStairs(self, n: int) -> int:
        dp = [maxsize] * n
        dp[0] = 1
        dp[1] = 2

        for i in range(2, n):
            dp[i] = dp[i - 1] + dp[i - 2]

        return dp[-1]


sol = Solution()

assert sol.climbStairs(2) == 2
assert sol.climbStairs(3) == 3
assert sol.climbStairs(10) == 89
