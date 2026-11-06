"""
Given a sorted array of integers and an integer num, return the lowest
index at which num appears in array. Return -1 when num is not in array.

Example 1:

Input: array = [200, 200, 500, 500], num = 500
Output: 2
Explanation: 500 appears at indices 2 and 3. The lowest is 2.

Example 2:

Input: array = [200, 200, 500, 500], num = 300
Output: -1

Example 3:

Input: array = [], num = 200
Output: -1

Constraints:

    0 <= len(array) <= 10^5
    -10^9 <= array[i], num <= 10^9
    array is sorted in non-decreasing order.

    REQUIRED: O(log n) time, O(1) extra space. NO linear scan, NO
    index(), NO bisect.
"""


class Solution:
    def find_first(self, array: list[int], num: int) -> int:
        pass


sol = Solution()

print(sol.find_first([200, 200, 500, 500], 500))  # 2

# assert sol.find_first([200, 200, 500, 500], 500) == 2
# assert sol.find_first([200, 200, 500, 500], 300) == -1
# assert sol.find_first([], 200) == -1
# assert sol.find_first([200, 200, 500, 500], 200) == 0
# assert sol.find_first([200] * 999 + [500], 500) == 999
# assert sol.find_first([500], 500) == 0
# assert sol.find_first([200, 200, 200, 500], 500) == 3
# assert sol.find_first([200, 200, 200, 200, 500, 500, 500], 200) == 0
# assert sol.find_first([200, 200, 200, 200, 500, 500, 500], 500) == 4
# assert sol.find_first([200, 200, 200, 200, 500, 500, 500], 100) == -1
# assert sol.find_first([200, 200, 200, 200, 500, 500, 500], 600) == -1
# assert sol.find_first([500], 200) == -1
# assert sol.find_first([1, 2, 2, 2, 3], 2) == 1
# assert sol.find_first([-10 ** 9, 10 ** 9], -10 ** 9) == 0
# assert sol.find_first([-10 ** 9, 10 ** 9], 10 ** 9) == 1
# assert sol.find_first([7] * 10 ** 5, 7) == 0
# assert sol.find_first(list(range(10 ** 5)), 10 ** 5 - 1) == 10 ** 5 - 1
# assert sol.find_first(list(range(10 ** 5)), 10 ** 5) == -1
