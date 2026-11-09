"""
EPI 10.3 Sort an almost-sorted array

Given an iterator sequence of integers and an integer k, return the
elements of sequence sorted ascending. Each element is at most k
positions away from its position in the sorted order.

Example 1:

Input: sequence = iter([3, -1, 2, 6, 4, 5, 8]), k = 2
Output: [-1, 2, 3, 4, 5, 6, 8]
Explanation: 3 is at index 0 and belongs at index 2. 6 is at index 3
and belongs at index 5. No element is more than 2 positions from its
place.

Example 2:

Input: sequence = iter([2, 1]), k = 1
Output: [1, 2]

Example 3:

Input: sequence = iter([]), k = 0
Output: []

Constraints:

    0 <= n <= 10^5, where n is the number of elements
    0 <= k <= 10^3
    -10^9 <= element <= 10^9

    REQUIRED: O(n log k) time and O(k) extra space, the output not
    counted. NO sorted(), NO list.sort(), NO list(sequence).
"""


class Solution:
    def sort_approximately_sorted_array(self, sequence: Iterator[int], k: int) -> list[int]:
        pass


sol = Solution()

print(sol.sort_approximately_sorted_array(iter([3, -1, 2, 6, 4, 5, 8]), 2))  # [-1, 2, 3, 4, 5, 6, 8]

# assert sol.sort_approximately_sorted_array(iter([3, -1, 2, 6, 4, 5, 8]), 2) == [-1, 2, 3, 4, 5, 6, 8]
# assert sol.sort_approximately_sorted_array(iter([2, 1]), 1) == [1, 2]
# assert sol.sort_approximately_sorted_array(iter([]), 0) == []
# assert sol.sort_approximately_sorted_array(iter([]), 3) == []
# assert sol.sort_approximately_sorted_array(iter([5]), 0) == [5]
# assert sol.sort_approximately_sorted_array(iter([1, 2, 3, 4]), 0) == [1, 2, 3, 4]
# assert sol.sort_approximately_sorted_array(iter([1, 2, 3, 4]), 3) == [1, 2, 3, 4]
# assert sol.sort_approximately_sorted_array(iter([4, 3, 2, 1]), 3) == [1, 2, 3, 4]
# assert sol.sort_approximately_sorted_array(iter([2, 1, 4, 3, 6, 5]), 1) == [1, 2, 3, 4, 5, 6]
# assert sol.sort_approximately_sorted_array(iter([3, 3, 1, 1]), 2) == [1, 1, 3, 3]
# assert sol.sort_approximately_sorted_array(iter([0, -5, -10]), 2) == [-10, -5, 0]
# assert sol.sort_approximately_sorted_array(iter([2, 0, 1]), 5) == [0, 1, 2]
# assert sol.sort_approximately_sorted_array(iter(v for i in range(0, 10 ** 5, 2) for v in (i + 1, i)), 1) == list(range(10 ** 5))
# assert sol.sort_approximately_sorted_array(iter(v for i in range(0, 10 ** 5, 1000) for v in range(i + 999, i - 1, -1)), 999) == list(range(10 ** 5))
