"""
URL: https://leetcode.com/problems/find-three-consecutive-integers-that-sum-to-a-given-number/description/?envType=problem-list-v2&envId=vn57k9wr

2177. Find Three Consecutive Integers That Sum to a Given Number

Given an integer num, return three consecutive integers (as a sorted array) that sum to num. If num cannot be expressed as the sum of three consecutive integers, return an empty array.

Example 1:

Input: num = 33
Output: [10,11,12]
Explanation: 33 can be expressed as 10 + 11 + 12 = 33.
10, 11, 12 are 3 consecutive integers, so we return [10, 11, 12].

Example 2:

Input: num = 4
Output: []
Explanation: There is no way to express 4 as the sum of 3 consecutive integers.

Constraints:

    0 <= num <= 10^15

---

Ok completely misunderstood the problem on first read.

I need to find 3 sorted consecutive numbers that sum to num.

logically, if i just divide the number by 3, call that m
then the solution could be:

m-1, m, m+1

So what could the edge cases be? It's likely that if the number
is not divisible by 3, then this is not doable.

Passes on lc.

"""


class Solution:
    def sumOfThree(self, num: int) -> List[int]:
        if num % 3 != 0:
            return []
        d = num // 3
        return [d - 1, d, d + 1]


sol = Solution()

print(sol.sumOfThree(33))  # [10, 11, 12]

assert sol.sumOfThree(33) == [10, 11, 12]
assert sol.sumOfThree(4) == []

assert sol.sumOfThree(0) == [-1, 0, 1]
assert sol.sumOfThree(3) == [0, 1, 2]
assert sol.sumOfThree(6) == [1, 2, 3]
assert sol.sumOfThree(1) == []
assert sol.sumOfThree(2) == []
assert sol.sumOfThree(10**15) == []
assert sol.sumOfThree(10**15 - 1) == [333333333333332, 333333333333333, 333333333333334]
assert sol.sumOfThree(-3) == [-2, -1, 0]
assert sol.sumOfThree(-6) == [-3, -2, -1]
assert sol.sumOfThree(9) == [2, 3, 4]
assert sol.sumOfThree(12) == [3, 4, 5]
assert sol.sumOfThree(5) == []
