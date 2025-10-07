"""
URL: https://leetcode.com/problems/sum-multiples/description/?envType=problem-list-v2&envId=vn57k9wr

2652. Sum Multiples

Given a positive integer n, find the sum of all integers in the range [1, n] inclusive that are divisible by 3, 5, or 7.

Return an integer denoting the sum of all numbers in the given range satisfying the constraint.


Example 1:

Input: n = 7
Output: 21
Explanation: Numbers in the range [1, 7] that are divisible by 3, 5, or 7 are: 3, 5, 6, 7. The sum of these numbers is 21.

Example 2:

Input: n = 10
Output: 40
Explanation: Numbers in the range [1, 10] that are divisible by 3, 5, or 7 are: 3, 5, 6, 7, 9, 10. The sum of these numbers is 40.

Example 3:

Input: n = 9
Output: 30
Explanation: Numbers in the range [1, 9] that are divisible by 3, 5, or 7 are: 3, 5, 6, 7, 9. The sum of these numbers is 30.


Constraints:

    1 <= n <= 10^3
"""


class Solution:
    def sumOfMultiples(self, n: int) -> int:
        return sum(
            x for x in range(1, n + 1) if (x % 3 == 0 or x % 5 == 0 or x % 7 == 0)
        )


sol = Solution()

assert sol.sumOfMultiples(7) == 21
assert sol.sumOfMultiples(10) == 40
assert sol.sumOfMultiples(9) == 30
assert sol.sumOfMultiples(1) == 0
assert sol.sumOfMultiples(2) == 0
assert sol.sumOfMultiples(3) == 3
assert sol.sumOfMultiples(4) == 3
assert sol.sumOfMultiples(5) == 8
assert sol.sumOfMultiples(6) == 14
assert sol.sumOfMultiples(14) == 66
assert sol.sumOfMultiples(15) == 81
assert sol.sumOfMultiples(21) == 140
assert sol.sumOfMultiples(1000) == 272066
