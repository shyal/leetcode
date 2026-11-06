"""
Given two lists arr1 and arr2, each sorted ascending with no repeated
value, return the values that are in both lists, sorted ascending.

Example 1:

Input: arr1 = [1, 2, 3, 5, 6, 7], arr2 = [3, 6, 7, 8, 20]
Output: [3, 6, 7]

Example 2:

Input: arr1 = [1, 3, 5, 9], arr2 = [2, 4, 6, 10]
Output: []

Example 3:

Input: arr1 = [11], arr2 = [11]
Output: [11]

Constraints:

    0 <= len(arr1), len(arr2) <= 10^5
    0 <= arr1[i], arr2[i] <= 10^9

    REQUIRED: O(n + m) time, O(1) extra space beyond the output. NO set,
    NO dict, NO sort.
"""


class Solution:
    def find_duplicates(self, arr1: list[int], arr2: list[int]) -> list[int]:
        pass


sol = Solution()

print(sol.find_duplicates([1, 2, 3, 5, 6, 7], [3, 6, 7, 8, 20]))  # [3, 6, 7]

# assert sol.find_duplicates([1, 2, 3, 5, 6, 7], [3, 6, 7, 8, 20]) == [3, 6, 7]
# assert sol.find_duplicates([1, 3, 5, 9], [2, 4, 6, 10]) == []
# assert sol.find_duplicates([11], [11]) == [11]
# assert sol.find_duplicates([1, 2, 3, 5, 6, 7], [7, 8, 9, 10, 11, 12]) == [7]
# assert sol.find_duplicates([10, 20, 30, 40, 50, 60, 70, 80], [10, 20, 30, 40, 50, 60]) == [10, 20, 30, 40, 50, 60]
# assert sol.find_duplicates([10, 20, 30, 40, 50, 60, 70], [10, 20, 30, 40, 50, 60, 70]) == [10, 20, 30, 40, 50, 60, 70]
# assert sol.find_duplicates([], []) == []
# assert sol.find_duplicates([], [1, 2]) == []
# assert sol.find_duplicates([1, 2], []) == []
# assert sol.find_duplicates([1], [2]) == []
# assert sol.find_duplicates([2], [1]) == []
# assert sol.find_duplicates([1, 2, 3], [3]) == [3]
# assert sol.find_duplicates([3], [1, 2, 3]) == [3]
# assert sol.find_duplicates([1, 5, 9], [0, 5, 10]) == [5]
# assert sol.find_duplicates(list(range(0, 10 ** 5, 2)), list(range(0, 10 ** 5, 3))) == list(range(0, 10 ** 5, 6))
# assert sol.find_duplicates(list(range(10 ** 5)), [10 ** 5 - 1]) == [10 ** 5 - 1]
