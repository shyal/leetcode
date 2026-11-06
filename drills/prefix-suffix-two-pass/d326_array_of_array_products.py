"""
Given a list of integers arr, return a list of the same length in which
position i holds the product of every element of arr except arr[i]. When
arr has fewer than two elements, return an empty list.

Example 1:

Input: arr = [2, 3, 0, 982, 10]
Output: [0, 0, 58920, 0, 0]
Explanation: position 2 holds 2 * 3 * 982 * 10. Every other product
includes the 0.

Example 2:

Input: arr = [8, 10, 2]
Output: [20, 16, 80]
Explanation: 10 * 2, 8 * 2, 8 * 10.

Example 3:

Input: arr = [7]
Output: []

Constraints:

    0 <= len(arr) <= 10^5
    -1000 <= arr[i] <= 1000

    REQUIRED: O(n) time. NO division.
"""


class Solution:
    def array_of_array_products(self, arr: list[int]) -> list[int]:
        pass


sol = Solution()

print(sol.array_of_array_products([2, 3, 0, 982, 10]))  # [0, 0, 58920, 0, 0]

# assert sol.array_of_array_products([2, 3, 0, 982, 10]) == [0, 0, 58920, 0, 0]
# assert sol.array_of_array_products([8, 10, 2]) == [20, 16, 80]
# assert sol.array_of_array_products([7]) == []
# assert sol.array_of_array_products([]) == []
# assert sol.array_of_array_products([2, 2]) == [2, 2]
# assert sol.array_of_array_products([2, 7, 3, 4]) == [84, 24, 56, 42]
# assert sol.array_of_array_products([-3, 17, 430, -6, 5, -12, -11, 5]) == [-144738000, 25542000, 1009800, -72369000, 86842800, -36184500, -39474000, 86842800]
# assert sol.array_of_array_products([0, 0, 5]) == [0, 0, 0]
# assert sol.array_of_array_products([1, -1, 1, -1]) == [1, -1, 1, -1]
# assert sol.array_of_array_products([1] * 10 ** 5) == [1] * 10 ** 5
# assert sol.array_of_array_products([2] * 20) == [2 ** 19] * 20
