"""
URL: https://leetcode.com/problems/find-the-original-array-of-prefix-xor/description/?envType=problem-list-v2&envId=vn57k9wr

2433. Find The Original Array of Prefix Xor

You are given an integer array pref of size n. Find and return the array arr of size n that satisfies:

    pref[i] = arr[0] ^ arr[1] ^ ... ^ arr[i].

Note that ^ denotes the bitwise-xor operation.

It can be proven that the answer is unique.

Example 1:

Input: pref = [5,2,0,3,1]
Output: [5,7,2,3,2]
Explanation: From the array [5,7,2,3,2] we have the following:
- pref[0] = 5.
- pref[1] = 5 ^ 7 = 2.
- pref[2] = 5 ^ 7 ^ 2 = 0.
- pref[3] = 5 ^ 7 ^ 2 ^ 3 = 3.
- pref[4] = 5 ^ 7 ^ 2 ^ 3 ^ 2 = 1.

Example 2:

Input: pref = [13]
Output: [13]
Explanation: We have pref[0] = arr[0] = 13.

Constraints:

    1 <= pref.length <= 10^5
    0 <= pref[i] <= 10^6

---


5 ^ x = 2

   101
^  111
------
   010


5 ^ 2 = 7

LEETCODE: Accepted (11 ms, 36.7 MB)
"""


class Solution:
    def findArray(self, pref: List[int]) -> List[int]:
        return [pref[0]] + [a ^ b for a, b in zip(pref, pref[1:])]


sol = Solution()

print(sol.findArray([5, 2, 0, 3, 1]))  # [5,7,2,3,2]

assert sol.findArray([5, 2, 0, 3, 1]) == [5, 7, 2, 3, 2]
assert sol.findArray([13]) == [13]

assert sol.findArray([0]) == [0]
assert sol.findArray([0, 0, 0, 0, 0]) == [0, 0, 0, 0, 0]
assert sol.findArray([1, 1, 1, 1, 1]) == [1, 0, 0, 0, 0]
assert sol.findArray([10**6] * 10) == [1000000, 0, 0, 0, 0, 0, 0, 0, 0, 0]
assert sol.findArray([0, 10**6, 0, 10**6, 0]) == [0, 1000000, 1000000, 1000000, 1000000]
assert sol.findArray([1, 3, 0, 3, 2, 2, 0]) == [1, 2, 3, 3, 1, 0, 2]
assert sol.findArray([2**20, 2**20, 0, 2**20, 2**20]) == [
    1048576,
    0,
    1048576,
    1048576,
    0,
]
assert sol.findArray([0, 1, 3, 0, 3, 2, 2, 0]) == [0, 1, 2, 3, 3, 1, 0, 2]
assert sol.findArray([10**6]) == [1000000]
assert sol.findArray([10**6] * 10**5)[:10] == [1000000, 0, 0, 0, 0, 0, 0, 0, 0, 0]
assert sol.findArray([i ^ (i - 1) for i in range(1, 11)]) == [
    1,
    2,
    2,
    6,
    6,
    2,
    2,
    14,
    14,
    2,
]
assert sol.findArray([0] * (10**5))[:10] == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
