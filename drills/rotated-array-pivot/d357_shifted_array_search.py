"""
Given an array shiftArr of distinct integers and an integer num, return
the index of num in shiftArr, or -1 when num is not in it. The array
is a sorted array shifted to the left by an unknown offset between 0
and len(shiftArr) - 1: the sorted array [2, 4, 5, 9, 12, 17] shifted
three times to the left is [9, 12, 17, 2, 4, 5].

Example 1:

Input: shiftArr = [9, 12, 17, 2, 4, 5], num = 2
Output: 3

Example 2:

Input: shiftArr = [9, 12, 17, 2, 4, 5], num = 17
Output: 2

Example 3:

Input: shiftArr = [1, 2, 3, 4, 5, 0], num = 7
Output: -1

Constraints:

    1 <= len(shiftArr) <= 10^5
    -10^9 <= shiftArr[i], num <= 10^9
    The values of shiftArr are distinct.

    REQUIRED: O(log n) time, O(1) extra space. NO scan for the offset,
    NO sorting, NO index().
"""


class Solution:
    def shifted_arr_search(self, shiftArr: list[int], num: int) -> int:
        pass


sol = Solution()

print(sol.shifted_arr_search([9, 12, 17, 2, 4, 5], 2))  # 3

# assert sol.shifted_arr_search([9, 12, 17, 2, 4, 5], 2) == 3
# assert sol.shifted_arr_search([9, 12, 17, 2, 4, 5], 17) == 2
# assert sol.shifted_arr_search([1, 2, 3, 4, 5, 0], 7) == -1
# assert sol.shifted_arr_search([2], 2) == 0
# assert sol.shifted_arr_search([2], 3) == -1
# assert sol.shifted_arr_search([1, 2], 2) == 1
# assert sol.shifted_arr_search([2, 1], 1) == 1
# assert sol.shifted_arr_search([0, 1, 2, 3, 4, 5], 1) == 1
# assert sol.shifted_arr_search([1, 2, 3, 4, 5, 0], 0) == 5
# assert sol.shifted_arr_search([9, 12, 17, 2, 4, 5, 6], 4) == 4
# assert sol.shifted_arr_search([9, 12, 17, 2, 4, 5], 9) == 0
# assert sol.shifted_arr_search([9, 12, 17, 2, 4, 5], 5) == 5
# assert sol.shifted_arr_search([9, 12, 17, 2, 4, 5], 3) == -1
# assert sol.shifted_arr_search([9, 12, 17, 2, 4, 5], 20) == -1
# assert sol.shifted_arr_search([9, 12, 17, 2, 4, 5], 1) == -1
# assert sol.shifted_arr_search([4, 5, 6, 7, 0, 1, 2], 0) == 4
# assert sol.shifted_arr_search([-3, -1, -9, -7, -5], -5) == 4
# assert sol.shifted_arr_search(list(range(10 ** 5)), 10 ** 5 - 1) == 10 ** 5 - 1
# assert sol.shifted_arr_search(list(range(70000, 10 ** 5)) + list(range(70000)), 69999) == 10 ** 5 - 1
# assert sol.shifted_arr_search(list(range(70000, 10 ** 5)) + list(range(70000)), 0) == 30000
# assert sol.shifted_arr_search(list(range(70000, 10 ** 5)) + list(range(70000)), 10 ** 5) == -1
