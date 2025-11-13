"""
URL: https://leetcode.com/problems/maximum-number-of-operations-to-move-ones-to-the-end/description/?envType=problem-list-v2&envId=vn57k9wr

3228. Maximum Number of Operations to Move Ones to the End

You are given a binary string s.

You can perform the following operation on the string any number of times:

- Choose any index i from the string where i + 1 < s.length such that s[i] == '1' and s[i + 1] == '0'.
- Move the character s[i] to the right until it reaches the end of the string or another '1'. For example, for s = "010010", if we choose i = 1, the resulting string will be s = "000110".

Return the maximum number of operations that you can perform.

Example 1:

Input: s = "1001101"
Output: 4
Explanation:
We can perform the following operations:
- Choose index i = 0. The resulting string is "0011101".
- Choose index i = 4. The resulting string is "0011011".
- Choose index i = 3. The resulting string is "0010111".
- Choose index i = 2. The resulting string is "0001111".

Example 2:

Input: s = "00111"
Output: 0

Constraints:
- 1 <= s.length <= 10^5
- s[i] is either '0' or '1'.

---

10 -> 01 == 1
100 -> 001 == 1
110 -> 011 == 2



0011101

Find the right most zero, and count the number of 1s to its left, + 1.

"""


class Solution:
    def maxOperations(self, s: str) -> int:
        s = s[::-1]
        g = [[key, len(list(val))] for key, val in groupby(s)]
        mult = 0
        count = 0
        for c, num in g:
            if c == "1" and mult == 0:
                continue
            if c == "0":
                mult += 1
            elif c == "1":
                count += mult * num
        return count


sol = Solution()

# print(sol.maxOperations("1001101"))  # 4

assert sol.maxOperations("1001101") == 4
assert sol.maxOperations("00111") == 0
assert sol.maxOperations("0") == 0
assert sol.maxOperations("1") == 0
assert sol.maxOperations("1010") == 3
assert sol.maxOperations("01") == 0
assert sol.maxOperations("010101") == 3
assert sol.maxOperations("000") == 0
assert sol.maxOperations("1111") == 0
assert sol.maxOperations("10100") == 3
# assert sol.maxOperations("1001") == 2

assert sol.maxOperations("10") == 1
assert sol.maxOperations("100") == 1
assert sol.maxOperations("110") == 2
assert sol.maxOperations("1110") == 3
assert sol.maxOperations("101") == 1
assert sol.maxOperations("00101") == 1
assert sol.maxOperations("100000") == 1
assert sol.maxOperations("01110") == 3
assert sol.maxOperations("1100") == 2
