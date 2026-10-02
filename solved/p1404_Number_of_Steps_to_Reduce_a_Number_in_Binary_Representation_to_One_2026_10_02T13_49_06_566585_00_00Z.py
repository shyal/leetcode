"""
URL: https://leetcode.com/problems/number-of-steps-to-reduce-a-number-in-binary-representation-to-one/description/?envType=problem-list-v2&envId=vn57k9wr

1404. Number of Steps to Reduce a Number in Binary Representation to One

Given the binary representation of an integer as a string s, return the number of steps to reduce it to 1 under the following rules:

- If the current number is even, you have to divide it by 2.
- If the current number is odd, you have to add 1 to it.

It is guaranteed that you can always reach one for all test cases.

Example 1:

Input: s = "1101"
Output: 6
Explanation: "1101" corresponds to number 13 in their decimal representation.
Step 1) 13 is odd, add 1 and obtain 14.
Step 2) 14 is even, divide by 2 and obtain 7.
Step 3) 7 is odd, add 1 and obtain 8.
Step 4) 8 is even, divide by 2 and obtain 4.
Step 5) 4 is even, divide by 2 and obtain 2.
Step 6) 2 is even, divide by 2 and obtain 1.

Example 2:

Input: s = "10"
Output: 1
Explanation: "10" corresponds to number 2 in their decimal representation.
Step 1) 2 is even, divide by 2 and obtain 1.

Example 3:

Input: s = "1"
Output: 0

Constraints:

    1 <= s.length <= 500
    s consists of characters '0' or '1'
    s[0] == '1'

---

LEETCODE: Accepted (3 ms, 19.5 MB)
"""


# mu 0.7
# def numSteps(s: str) -> int
#   num = to_int(list(int(x) for x in s), base=2)
#   ret count = 0
#   while num != 1
#     count += 1
#     if even(num)
#       num = num // 2
#     else
#       num = num + 1

def to_int(digits, reverse=False, base=10):
    out = 0
    for d in digits[::-1] if reverse else digits:
        out = out * base + d
    return out


def even(n):
    return n % 2 == 0


class Solution:
    def numSteps(self, s: str) -> int:
        num = to_int(list(int(x) for x in s), base=2)
        count = 0
        while num != 1:
            count += 1
            if even(num):
                num = num // 2
            else:
                num = num + 1
        return count


sol = Solution()
print(sol.numSteps('1101'))
assert sol.numSteps('1111011110000011100000110001011011110010111001010111110001') == 85
assert sol.numSteps('1101') == 6
assert sol.numSteps('10') == 1
assert sol.numSteps('1') == 0
assert sol.numSteps('11') == 3
assert sol.numSteps('111') == 4
