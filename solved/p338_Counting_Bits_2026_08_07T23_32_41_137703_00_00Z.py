"""
URL: https://leetcode.com/problems/counting-bits/description/?envType=problem-list-v2&envId=vn57k9wr

338. Counting Bits

Given an integer n, return an array ans of length n + 1 such that for each i
(0 <= i <= n), ans[i] is the number of 1's in the binary representation of i.

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

    It is very easy to come up with a solution with a runtime of O(n log n).
    Can you do it in linear time O(n) and possibly in a single pass?

    
---

Far from being a big solve, and i'd forgotten about this move:

    def toBin(self, n):
        div, mod = divmod(n, 2)
        ret = [mod]
        if div:
            ret = self.toBin(div) + ret
        return ret

From i had to steal by searching for toBin.
"""

class Solution:

    def toBin(self, n):
        div, mod = divmod(n, 2)
        ret = [mod]
        if div:
            ret = self.toBin(div) + ret
        return ret

    def countBits(self, n: int) -> List[int]:
        return [sum(x == 1 for x in self.toBin(v)) for v in range(n+1)]


sol = Solution()

# print(sol.toBin(5))
# print(sum(x == '1' for x in sol.toBin(3)))

# print(sol.countBits(2))  # [0, 1, 1]

assert sol.countBits(2) == [0, 1, 1]
assert sol.countBits(5) == [0, 1, 1, 2, 1, 2]
assert sol.countBits(0) == [0]
assert sol.countBits(1) == [0, 1]
assert sol.countBits(3) == [0, 1, 1, 2]
assert sol.countBits(4) == [0, 1, 1, 2, 1]
assert sol.countBits(7) == [0, 1, 1, 2, 1, 2, 2, 3]
assert sol.countBits(8) == [0, 1, 1, 2, 1, 2, 2, 3, 1]
assert sol.countBits(15) == [0, 1, 1, 2, 1, 2, 2, 3, 1, 2, 2, 3, 2, 3, 3, 4]
assert sol.countBits(16) == [0, 1, 1, 2, 1, 2, 2, 3, 1, 2, 2, 3, 2, 3, 3, 4, 1]
assert len(sol.countBits(100)) == 101
assert sol.countBits(1024)[1024] == 1
assert sol.countBits(1024)[1023] == 10
assert max(sol.countBits(255)) == 8
assert sum(sol.countBits(3)) == 4
assert sol.countBits(100000)[-1] == 6
assert len(sol.countBits(100000)) == 100001
result = sol.countBits(1000)
assert all(result[i] == bin(i).count("1") for i in range(1001))
assert all(sol.countBits(512)[2**k] == 1 for k in range(10))
assert all(sol.countBits(511)[2**k - 1] == k for k in range(1, 10))