"""
URL: https://leetcode.com/problems/decode-xored-array/description/?envType=problem-list-v2&envId=vn57k9wr

1720. Decode XORed Array

There is a hidden integer array arr that consists of n non-negative integers.

It was encoded into another integer array encoded of length n - 1, such that
encoded[i] = arr[i] XOR arr[i + 1]. For example, if arr = [1,0,2,1], then
encoded = [1,2,3].

You are given the encoded array. You are also given an integer first, that is
the first element of arr, i.e. arr[0].

Return the original array arr. It can be proved that the answer exists and is
unique.


Example 1:

Input: encoded = [1,2,3], first = 1
Output: [1,0,2,1]
Explanation: If arr = [1,0,2,1], then first = 1 and encoded = [1 XOR 0, 0 XOR 2, 2 XOR 1] = [1,2,3]

Example 2:

Input: encoded = [6,2,7,3], first = 4
Output: [4,2,0,7,4]


Constraints:

    2 <= n <= 10^4
    encoded.length == n - 1
    0 <= encoded[i] <= 10^5
    0 <= first <= 10^5

---

encoded[i] = arr[i] XOR arr[i + 1]

first = arr[i] XOR arr[i + 1]
1 = 1 XOR x => 1 = 1 XOR 0
thus arr = [0, ....]

---

weird problem. anyway.


"""

class Solution:
    def decode(self, encoded: List[int], first: int) -> List[int]:
        res = [first]
        for x in encoded:
            res.append(x ^ res[-1])
        return res


sol = Solution()

print(sol.decode([1, 2, 3], 1))  # [1, 0, 2, 1]

assert sol.decode([1, 2, 3], 1) == [1, 0, 2, 1]
assert sol.decode([6, 2, 7, 3], 4) == [4, 2, 0, 7, 4]
assert sol.decode([0], 0) == [0, 0]
assert sol.decode([0], 5) == [5, 5]
assert sol.decode([7], 7) == [7, 0]
assert sol.decode([3], 1) == [1, 2]
assert sol.decode([0, 0, 0], 7) == [7, 7, 7, 7]
assert sol.decode([5, 5], 5) == [5, 0, 5]
assert sol.decode([1, 1, 1, 1], 0) == [0, 1, 0, 1, 0]
assert sol.decode([1, 1, 1, 1, 1], 1) == [1, 0, 1, 0, 1, 0]
assert sol.decode([2, 4, 8, 16], 1) == [1, 3, 7, 15, 31]
assert sol.decode([1, 3, 5], 2) == [2, 3, 0, 5]
assert sol.decode([100000], 100000) == [100000, 0]
assert sol.decode([100000], 3) == [3, 100003]
assert len(sol.decode([1] * 9999, 0)) == 10000