"""
Given a list of integers arr, move every 0 to the end of the list and
return arr. The other elements keep their order.

Example 1:

Input: arr = [1, 10, 0, 2, 8, 3, 0, 0, 6, 4, 0, 5, 7, 0]
Output: [1, 10, 2, 8, 3, 6, 4, 5, 7, 0, 0, 0, 0, 0]

Example 2:

Input: arr = [0, 0, 3]
Output: [3, 0, 0]

Example 3:

Input: arr = []
Output: []

Constraints:

    0 <= len(arr) <= 10^5
    -10^9 <= arr[i] <= 10^9

    REQUIRED: O(n) time, O(1) extra space, the change made in arr
    itself. NO second list, NO remove(), NO insert(), NO sort.
"""


class Solution:
    def moveZerosToEnd(self, arr: list[int]) -> list[int]:
        pass


sol = Solution()

print(sol.moveZerosToEnd([1, 10, 0, 2, 8, 3, 0, 0, 6, 4, 0, 5, 7, 0]))  # [1, 10, 2, 8, 3, 6, 4, 5, 7, 0, 0, 0, 0, 0]

# assert sol.moveZerosToEnd([1, 10, 0, 2, 8, 3, 0, 0, 6, 4, 0, 5, 7, 0]) == [1, 10, 2, 8, 3, 6, 4, 5, 7, 0, 0, 0, 0, 0]
# assert sol.moveZerosToEnd([0, 0, 3]) == [3, 0, 0]
# assert sol.moveZerosToEnd([]) == []
# assert sol.moveZerosToEnd([0]) == [0]
# assert sol.moveZerosToEnd([1]) == [1]
# assert sol.moveZerosToEnd([0, 0]) == [0, 0]
# assert sol.moveZerosToEnd([1, 0, 2]) == [1, 2, 0]
# assert sol.moveZerosToEnd([1, -1, 2, 4, 6]) == [1, -1, 2, 4, 6]
# assert sol.moveZerosToEnd([6, 1, 0, 3, 0, -1, 2]) == [6, 1, 3, -1, 2, 0, 0]
# assert sol.moveZerosToEnd([0, 1, 2, 3, 0, 0, 1, 1, 6, 4, 1]) == [1, 2, 3, 1, 1, 6, 4, 1, 0, 0, 0]
# a = [0, 7, 0, 8]
# assert sol.moveZerosToEnd(a) is a and a == [7, 8, 0, 0]
# assert sol.moveZerosToEnd([0] * 10 ** 5) == [0] * 10 ** 5
# assert sol.moveZerosToEnd([v for k in range(1, 50001) for v in (0, k)]) == list(range(1, 50001)) + [0] * 50000
