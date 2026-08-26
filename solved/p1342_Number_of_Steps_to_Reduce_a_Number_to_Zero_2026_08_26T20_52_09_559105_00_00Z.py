"""
URL: https://leetcode.com/problems/number-of-steps-to-reduce-a-number-to-zero/description/?envType=problem-list-v2&envId=vn57k9wr

1342. Number of Steps to Reduce a Number to Zero

Given an integer num, return the number of steps to reduce it to zero.

In one step, if the current number is even, you have to divide it by 2, otherwise, you have to subtract 1 from it.

Example 1:

Input: num = 14
Output: 6
Explanation:
Step 1) 14 is even; divide by 2 and obtain 7.
Step 2) 7 is odd; subtract 1 and obtain 6.
Step 3) 6 is even; divide by 2 and obtain 3.
Step 4) 3 is odd; subtract 1 and obtain 2.
Step 5) 2 is even; divide by 2 and obtain 1.
Step 6) 1 is odd; subtract 1 and obtain 0.

Example 2:

Input: num = 8
Output: 4
Explanation:
Step 1) 8 is even; divide by 2 and obtain 4.
Step 2) 4 is even; divide by 2 and obtain 2.
Step 3) 2 is even; divide by 2 and obtain 1.
Step 4) 1 is odd; subtract 1 and obtain 0.

Example 3:

Input: num = 123
Output: 12

Constraints:

    0 <= num <= 10^6
"""


class Solution:
    def numberOfSteps(self, num: int) -> int:
        count = 0
        while num:
            count += 1
            if num % 2 == 0:
                num = num // 2
            else:
                num = num - 1
        return count


sol = Solution()

print(sol.numberOfSteps(14))  # 6

assert sol.numberOfSteps(14) == 6
assert sol.numberOfSteps(8) == 4
assert sol.numberOfSteps(123) == 12

assert sol.numberOfSteps(0) == 0
assert sol.numberOfSteps(1) == 1
assert sol.numberOfSteps(2) == 2
assert sol.numberOfSteps(3) == 3
assert sol.numberOfSteps(10**6) == 26
assert sol.numberOfSteps(999999) == 31
assert sol.numberOfSteps(16) == 5
assert sol.numberOfSteps(15) == 7
assert sol.numberOfSteps(1023) == 19
assert sol.numberOfSteps(1024) == 11
assert sol.numberOfSteps(500000) == 25
assert sol.numberOfSteps(1) == 1
