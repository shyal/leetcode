"""
URL: https://leetcode.com/problems/construct-the-minimum-bitwise-array-i/description/?envType=problem-list-v2&envId=vn57k9wr

3314. Construct the Minimum Bitwise Array I

You are given an array nums consisting of n prime integers.

You need to construct an array ans of length n, such that, for each index i, the bitwise OR of ans[i] and ans[i] + 1 is equal to nums[i], i.e. ans[i] OR (ans[i] + 1) == nums[i].

Additionally, you must minimize each value of ans[i] in the resulting array.

If it is not possible to find such a value for ans[i] that satisfies the condition, then set ans[i] = -1.

Example 1:

Input: nums = [2,3,5,7]
Output: [-1,1,4,3]
Explanation:
- For i = 0, as there is no value for ans[0] that satisfies ans[0] OR (ans[0] + 1) = 2, so ans[0] = -1.
- For i = 1, the smallest ans[1] that satisfies ans[1] OR (ans[1] + 1) = 3 is 1, because 1 OR (1 + 1) = 3.
- For i = 2, the smallest ans[2] that satisfies ans[2] OR (ans[2] + 1) = 5 is 4, because 4 OR (4 + 1) = 5.
- For i = 3, the smallest ans[3] that satisfies ans[3] OR (ans[3] + 1) = 7 is 3, because 3 OR (3 + 1) = 7.

Example 2:

Input: nums = [11,13,31]
Output: [9,12,15]
Explanation:
- For i = 0, the smallest ans[0] that satisfies ans[0] OR (ans[0] + 1) = 11 is 9, because 9 OR (9 + 1) = 11.
- For i = 1, the smallest ans[1] that satisfies ans[1] OR (ans[1] + 1) = 13 is 12, because 12 OR (12 + 1) = 13.
- For i = 2, the smallest ans[2] that satisfies ans[2] OR (ans[2] + 1) = 31 is 15, because 15 OR (15 + 1) = 31.

Constraints:

    1 <= nums.length <= 100
    2 <= nums[i] <= 1000
    nums[i] is a prime number.
"""


class Solution:
    def minBitwiseArray(self, nums: List[int]) -> List[int]:
        res = []
        for n in nums:
            r = float("inf")
            for i in range(n):
                if i | (i + 1) == n:
                    r = min(r, i)
            res.append(-1 if r == float("inf") else r)
        return res


sol = Solution()

print(sol.minBitwiseArray([2, 3, 5, 7]))  # [-1,1,4,3]

assert sol.minBitwiseArray([2, 3, 5, 7]) == [-1, 1, 4, 3]
assert sol.minBitwiseArray([11, 13, 31]) == [9, 12, 15]

assert sol.minBitwiseArray([2]) == [-1]
assert sol.minBitwiseArray([3]) == [1]
assert sol.minBitwiseArray([997]) == [996]
assert sol.minBitwiseArray([2, 2, 2, 2]) == [-1, -1, -1, -1]
assert sol.minBitwiseArray([3, 3, 3, 3]) == [1, 1, 1, 1]
assert sol.minBitwiseArray([5, 7, 11, 13]) == [4, 3, 9, 12]
assert sol.minBitwiseArray([31, 31, 31]) == [15, 15, 15]
assert sol.minBitwiseArray([2, 3, 5, 7, 11, 13, 17, 19, 23, 29]) == [
    -1,
    1,
    4,
    3,
    9,
    12,
    16,
    17,
    19,
    28,
]
assert sol.minBitwiseArray([997] * 100) == [
    996,
    996,
    996,
    996,
    996,
    996,
    996,
    996,
    996,
    996,
    996,
    996,
    996,
    996,
    996,
    996,
    996,
    996,
    996,
    996,
    996,
    996,
    996,
    996,
    996,
    996,
    996,
    996,
    996,
    996,
    996,
    996,
    996,
    996,
    996,
    996,
    996,
    996,
    996,
    996,
    996,
    996,
    996,
    996,
    996,
    996,
    996,
    996,
    996,
    996,
    996,
    996,
    996,
    996,
    996,
    996,
    996,
    996,
    996,
    996,
    996,
    996,
    996,
    996,
    996,
    996,
    996,
    996,
    996,
    996,
    996,
    996,
    996,
    996,
    996,
    996,
    996,
    996,
    996,
    996,
    996,
    996,
    996,
    996,
    996,
    996,
    996,
    996,
    996,
    996,
    996,
    996,
    996,
    996,
    996,
    996,
    996,
    996,
    996,
    996,
]
assert sol.minBitwiseArray([2] * 100) == [
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
]
assert sol.minBitwiseArray(
    [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71]
) == [-1, 1, 4, 3, 9, 12, 16, 17, 19, 28, 15, 36, 40, 41, 39, 52, 57, 60, 65, 67]
assert sol.minBitwiseArray(
    [
        2,
        3,
        5,
        7,
        11,
        13,
        17,
        19,
        23,
        29,
        31,
        37,
        41,
        43,
        47,
        53,
        59,
        61,
        67,
        71,
        73,
        79,
        83,
        89,
        97,
    ]
) == [
    -1,
    1,
    4,
    3,
    9,
    12,
    16,
    17,
    19,
    28,
    15,
    36,
    40,
    41,
    39,
    52,
    57,
    60,
    65,
    67,
    72,
    71,
    81,
    88,
    96,
]
