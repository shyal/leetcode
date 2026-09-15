"""
URL: https://leetcode.com/problems/counting-bits/description/?envType=problem-list-v2&envId=vn57k9wr

338. Counting Bits

Given an integer n, return an array ans of length n + 1 such that for each i (0 <= i <= n), ans[i] is the number of 1's in the binary representation of i.

Do not solve it with built-in functions (i.e., like __builtin_popcount in C++).

Example 1:

Input: n = 2
Output: [0,1,1]
Explanation:
0 --> 0
1 --> 1
2 --> 10

Example 2:

Input: n = 5
Output: [0,1,1,2,1,2]
Explanation:
0 --> 0
1 --> 1
2 --> 10
3 --> 11
4 --> 100
5 --> 101

Constraints:

    0 <= n <= 10^5

Follow up:

    It is very easy to come up with a solution with a runtime of O(n log n). Can you do it in linear time O(n) and possibly in a single pass?

---

LEETCODE: Accepted (103 ms, 20.4 MB)
"""


class Solution:

    def toBits(self, n):
        res = []
        while n:
            div, mod = divmod(n, 2)
            res.append(mod)
            n = div
        return res

    def countOnes(self, n):
        return sum(self.toBits(n))

    def countBits(self, n: int) -> List[int]:
        res = []
        for i in range(n + 1):
            res.append(self.countOnes(i))
        return res


sol = Solution()

print(sol.countBits(2))  # [0,1,1]

assert sol.countBits(2) == [0, 1, 1]
assert sol.countBits(5) == [0, 1, 1, 2, 1, 2]

assert sol.countBits(0) == [0]
assert sol.countBits(1) == [0, 1]
assert sol.countBits(10) == [0, 1, 1, 2, 1, 2, 2, 3, 1, 2, 2]
assert sol.countBits(16) == [0, 1, 1, 2, 1, 2, 2, 3, 1, 2, 2, 3, 2, 3, 3, 4, 1]
assert sol.countBits(31) == [
    0,
    1,
    1,
    2,
    1,
    2,
    2,
    3,
    1,
    2,
    2,
    3,
    2,
    3,
    3,
    4,
    1,
    2,
    2,
    3,
    2,
    3,
    3,
    4,
    2,
    3,
    3,
    4,
    3,
    4,
    4,
    5,
]
assert sol.countBits(32) == [
    0,
    1,
    1,
    2,
    1,
    2,
    2,
    3,
    1,
    2,
    2,
    3,
    2,
    3,
    3,
    4,
    1,
    2,
    2,
    3,
    2,
    3,
    3,
    4,
    2,
    3,
    3,
    4,
    3,
    4,
    4,
    5,
    1,
]
assert sol.countBits(63) == [
    0,
    1,
    1,
    2,
    1,
    2,
    2,
    3,
    1,
    2,
    2,
    3,
    2,
    3,
    3,
    4,
    1,
    2,
    2,
    3,
    2,
    3,
    3,
    4,
    2,
    3,
    3,
    4,
    3,
    4,
    4,
    5,
    1,
    2,
    2,
    3,
    2,
    3,
    3,
    4,
    2,
    3,
    3,
    4,
    3,
    4,
    4,
    5,
    2,
    3,
    3,
    4,
    3,
    4,
    4,
    5,
    3,
    4,
    4,
    5,
    4,
    5,
    5,
    6,
]
assert sol.countBits(64) == [
    0,
    1,
    1,
    2,
    1,
    2,
    2,
    3,
    1,
    2,
    2,
    3,
    2,
    3,
    3,
    4,
    1,
    2,
    2,
    3,
    2,
    3,
    3,
    4,
    2,
    3,
    3,
    4,
    3,
    4,
    4,
    5,
    1,
    2,
    2,
    3,
    2,
    3,
    3,
    4,
    2,
    3,
    3,
    4,
    3,
    4,
    4,
    5,
    2,
    3,
    3,
    4,
    3,
    4,
    4,
    5,
    3,
    4,
    4,
    5,
    4,
    5,
    5,
    6,
    1,
]
assert sol.countBits(100) == [
    0,
    1,
    1,
    2,
    1,
    2,
    2,
    3,
    1,
    2,
    2,
    3,
    2,
    3,
    3,
    4,
    1,
    2,
    2,
    3,
    2,
    3,
    3,
    4,
    2,
    3,
    3,
    4,
    3,
    4,
    4,
    5,
    1,
    2,
    2,
    3,
    2,
    3,
    3,
    4,
    2,
    3,
    3,
    4,
    3,
    4,
    4,
    5,
    2,
    3,
    3,
    4,
    3,
    4,
    4,
    5,
    3,
    4,
    4,
    5,
    4,
    5,
    5,
    6,
    1,
    2,
    2,
    3,
    2,
    3,
    3,
    4,
    2,
    3,
    3,
    4,
    3,
    4,
    4,
    5,
    2,
    3,
    3,
    4,
    3,
    4,
    4,
    5,
    3,
    4,
    4,
    5,
    4,
    5,
    5,
    6,
    2,
    3,
    3,
    4,
    3,
]
assert sol.countBits(15) == [0, 1, 1, 2, 1, 2, 2, 3, 1, 2, 2, 3, 2, 3, 3, 4]
