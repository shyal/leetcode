"""
URL: https://leetcode.com/problems/decode-xored-array/description/

1720. Decode XORed Array

There is a hidden integer array arr that consists of n non-negative integers.

It was encoded into another integer array encoded of length n - 1, such that encoded[i] = arr[i] XOR arr[i+1]. For example, if arr = [1,0,2,1], then encoded = [1,2,3].

You are given the encoded array. You are also given an integer first, that is the first element of arr, i.e. arr[0].

Return the hidden array arr.


Example 1:

Input: encoded = [1,2,3], first = 1
Output: [1,0,2,1]
Explanation: If arr = [1,0,2,1], then first = 1 and encoded = [1 XOR 0, 0 XOR 2, 2 XOR 1] = [1,2,3]

Example 2:

Input: encoded = [6,2,7,3], first = 4
Output: [4,2,0,7,4]
Explanation: If arr = [4,2,0,7,4], then encoded = [4 XOR 2, 2 XOR 0, 0 XOR 7, 7 XOR 4] = [6,2,7,3]


Constraints:

    2 <= n <= 10^4
    encoded.length == n - 1
    0 <= encoded[i] <= 10^5
    0 <= first <= 10^5

---

Kind of struggling to understand the question.

Input: encoded = [1,2,3], first = 1
Output: [1,0,2,1]
Explanation: If arr = [1,0,2,1], then first = 1 and encoded = [1 XOR 0, 0 XOR 2, 2 XOR 1] = [1,2,3]

>>> 1 ^ 1
0
>>> 0 ^ 2
2
>>> 2 ^ 3

So it seems i simply need to xor start with the first encoded item,
then xor the result with the following items in 'encoded' successively.
"""


class Solution:
    def decode(self, encoded: List[int], first: int) -> List[int]:
        res = [first]
        for e in encoded:
            first ^= e
            res.append(first)
        return res


sol = Solution()

assert sol.decode([1, 2, 3], 1) == [1, 0, 2, 1]
assert sol.decode([6, 2, 7, 3], 4) == [4, 2, 0, 7, 4]
assert sol.decode([0], 5) == [5, 5]
assert sol.decode([3], 1) == [1, 2]
assert sol.decode([0, 0], 0) == [0, 0, 0]
assert sol.decode([1, 1], 1) == [1, 0, 1]
assert sol.decode([0], 0) == [0, 0]
assert sol.decode([100000], 100000) == [100000, 0]
assert sol.decode([1, 3, 5], 0) == [0, 1, 2, 7]
