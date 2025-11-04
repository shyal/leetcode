"""
3731. Find Missing Elements

You are given an integer array nums consisting of unique integers.

Originally, nums contained every integer within a certain range. However, some integers might have gone missing from the array.

The smallest and largest integers of the original range are still present in nums.

Return a sorted list of all the missing integers in this range. If no integers are missing, return an empty list.

Example 1:

Input: nums = [1,4,2,5]
Output: [3]
Explanation: The smallest integer is 1 and the largest is 5, so the full range should be [1,2,3,4,5]. Among these, only 3 is missing.

Example 2:

Input: nums = [7,8,6,9]
Output: []
Explanation: The smallest integer is 6 and the largest is 9, so the full range is [6,7,8,9]. All integers are already present, so no integer is missing.

Example 3:

Input: nums = [5,1]
Output: [2,3,4]
Explanation: The smallest integer is 1 and the largest is 5, so the full range should be [1,2,3,4,5]. The missing integers are 2, 3, and 4.

Constraints:

    2 <= nums.length <= 100
    1 <= nums[i] <= 100
"""


class Solution:
    def findMissingElements(self, nums: List[int]) -> List[int]:
        if not nums:
            return []
        return [*sorted(list(set(range(min(nums), max(nums) + 1)) - set(nums)))]


sol = Solution()

# print(sol.findMissingElements([1, 4, 2, 5]))  # [3]

assert sol.findMissingElements([1, 4, 2, 5]) == [3]
assert sol.findMissingElements([7, 8, 6, 9]) == []
assert sol.findMissingElements([5, 1]) == [2, 3, 4]
assert sol.findMissingElements([1, 2]) == []
assert sol.findMissingElements([1, 3]) == [2]
assert sol.findMissingElements([1, 2, 3, 4, 5]) == []
assert sol.findMissingElements([5, 4, 3, 2, 1]) == []
assert sol.findMissingElements([1, 3, 5]) == [2, 4]
assert sol.findMissingElements([10, 1, 5]) == [2, 3, 4, 6, 7, 8, 9]
assert sol.findMissingElements([99, 100]) == []
assert sol.findMissingElements([1, 100]) == [
    2,
    3,
    4,
    5,
    6,
    7,
    8,
    9,
    10,
    11,
    12,
    13,
    14,
    15,
    16,
    17,
    18,
    19,
    20,
    21,
    22,
    23,
    24,
    25,
    26,
    27,
    28,
    29,
    30,
    31,
    32,
    33,
    34,
    35,
    36,
    37,
    38,
    39,
    40,
    41,
    42,
    43,
    44,
    45,
    46,
    47,
    48,
    49,
    50,
    51,
    52,
    53,
    54,
    55,
    56,
    57,
    58,
    59,
    60,
    61,
    62,
    63,
    64,
    65,
    66,
    67,
    68,
    69,
    70,
    71,
    72,
    73,
    74,
    75,
    76,
    77,
    78,
    79,
    80,
    81,
    82,
    83,
    84,
    85,
    86,
    87,
    88,
    89,
    90,
    91,
    92,
    93,
    94,
    95,
    96,
    97,
    98,
    99,
]
assert sol.findMissingElements([]) == []
assert sol.findMissingElements([1]) == []
assert sol.findMissingElements([1, 2, 4, 5, 6, 8]) == [3, 7]
assert sol.findMissingElements([10, 20, 15]) == [11, 12, 13, 14, 16, 17, 18, 19]
