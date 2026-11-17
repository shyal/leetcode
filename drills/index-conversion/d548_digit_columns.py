"""
Digit Columns

Given an array nums of positive integers that all have the same number of
digits, return cols, a list of tuples where cols[j] holds digit j of every
number in nums, in the order of nums. Digit 0 is the most significant.

Example 1:

Input: nums = [104, 275, 316, 489]
Output: [(1, 2, 3, 4), (0, 7, 1, 8), (4, 5, 6, 9)]
Explanation: The digits of 104 are 1, 0, 4. Digit 1 of the four numbers is 0, 7, 1, 8.

Example 2:

Input: nums = [7]
Output: [(7,)]

Example 3:

Input: nums = [10, 20]
Output: [(1, 2), (0, 0)]

Constraints:

    1 <= len(nums) <= 10^5
    1 <= nums[i] < 10^9
    All integers in nums have the same number of digits.

    REQUIRED: O(len(nums) * d) time, d the number of digits. NO str().
"""


class Solution:
    def digit_columns(self, nums: list[int]) -> list[tuple[int, ...]]:
        pass


sol = Solution()

print(sol.digit_columns([104, 275, 316, 489]))  # [(1, 2, 3, 4), (0, 7, 1, 8), (4, 5, 6, 9)]

# assert sol.digit_columns([104, 275, 316, 489]) == [(1, 2, 3, 4), (0, 7, 1, 8), (4, 5, 6, 9)]
# assert sol.digit_columns([7]) == [(7,)]
# assert sol.digit_columns([10, 20]) == [(1, 2), (0, 0)]
# assert sol.digit_columns([123456789]) == [(1,), (2,), (3,), (4,), (5,), (6,), (7,), (8,), (9,)]
# assert sol.digit_columns([5, 5, 5]) == [(5, 5, 5)]
# assert sol.digit_columns([90, 91, 92, 93, 94]) == [(9, 9, 9, 9, 9), (0, 1, 2, 3, 4)]
# assert sol.digit_columns([100000000, 999999999]) == [(1, 9)] + [(0, 9)] * 8
# assert sol.digit_columns([12, 34] * 50000)[1][:4] == (2, 4, 2, 4)
