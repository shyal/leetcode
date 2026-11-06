"""
Given a list arr of distinct integers and an integer k >= 0, return
every pair [x, y] of two elements of arr with x - y == k, ordered by
the position of y in arr.

Example 1:

Input: arr = [0, -1, -2, 2, 1], k = 1
Output: [[1, 0], [0, -1], [-1, -2], [2, 1]]
Explanation: the y values 0, -1, -2, 1 appear in arr in that order.

Example 2:

Input: arr = [1, 7, 5, 3, 32, 17, 12], k = 17
Output: []

Example 3:

Input: arr = [4, 1], k = 0
Output: []
Explanation: x and y are two different elements, and the elements are
distinct, so no pair has a difference of 0.

Constraints:

    0 <= len(arr) <= 100
    -10^4 <= arr[i] <= 10^4
    0 <= k <= 2 * 10^4

    REQUIRED: O(n) time. NO nested loops over pairs, NO sort.
"""


class Solution:
    def find_pairs_with_given_difference(self, arr: list[int], k: int) -> list[list[int]]:
        pass


sol = Solution()

print(sol.find_pairs_with_given_difference([0, -1, -2, 2, 1], 1))  # [[1, 0], [0, -1], [-1, -2], [2, 1]]

# assert sol.find_pairs_with_given_difference([0, -1, -2, 2, 1], 1) == [[1, 0], [0, -1], [-1, -2], [2, 1]]
# assert sol.find_pairs_with_given_difference([1, 7, 5, 3, 32, 17, 12], 17) == []
# assert sol.find_pairs_with_given_difference([4, 1], 0) == []
# assert sol.find_pairs_with_given_difference([4, 1], 3) == [[4, 1]]
# assert sol.find_pairs_with_given_difference([1, 5, 11, 7], 4) == [[5, 1], [11, 7]]
# assert sol.find_pairs_with_given_difference([1, 5, 11, 7], 6) == [[7, 1], [11, 5]]
# assert sol.find_pairs_with_given_difference([1, 5, 11, 7], 10) == [[11, 1]]
# assert sol.find_pairs_with_given_difference([], 3) == []
# assert sol.find_pairs_with_given_difference([1], 1) == []
# assert sol.find_pairs_with_given_difference([5, 3], 2) == [[5, 3]]
# assert sol.find_pairs_with_given_difference([3, 5], 2) == [[5, 3]]
# assert sol.find_pairs_with_given_difference([-10000, 10000], 20000) == [[10000, -10000]]
# assert sol.find_pairs_with_given_difference(list(range(100)), 1) == [[i + 1, i] for i in range(99)]
# assert sol.find_pairs_with_given_difference(list(range(100)), 99) == [[99, 0]]
# assert sol.find_pairs_with_given_difference(list(range(100)), 100) == []
# assert sol.find_pairs_with_given_difference(list(range(99, -1, -1)), 1) == [[i + 1, i] for i in range(98, -1, -1)]
