"""
EPI 12.8 Find the longest subarray with distinct entries

Given a list of integers A, return the length of the longest subarray of
A in which no value appears twice. A subarray is a run of consecutive
entries. The empty list has no nonempty subarray, so its answer is 0.

Example 1:

Input: A = [1, 2, 1, 3, 4, 3]
Output: 4
Explanation: [2, 1, 3, 4] has distinct entries. Every longer subarray
repeats 1 or 3.

Example 2:

Input: A = [5, 5, 5]
Output: 1

Example 3:

Input: A = []
Output: 0

Constraints:

    0 <= len(A) <= 10^5
    -10^9 <= A[i] <= 10^9

    REQUIRED: O(n) time, where n is the length of A.
"""


class Solution:
    def longest_subarray_with_distinct_entries(self, A: list[int]) -> int:
        pass


sol = Solution()

print(sol.longest_subarray_with_distinct_entries([1, 2, 1, 3, 4, 3]))  # 4

# assert sol.longest_subarray_with_distinct_entries([1, 2, 1, 3, 4, 3]) == 4
# assert sol.longest_subarray_with_distinct_entries([5, 5, 5]) == 1
# assert sol.longest_subarray_with_distinct_entries([]) == 0
# assert sol.longest_subarray_with_distinct_entries([7]) == 1
# assert sol.longest_subarray_with_distinct_entries([1, 2, 3]) == 3
# assert sol.longest_subarray_with_distinct_entries([1, 2, 3, 1]) == 3
# assert sol.longest_subarray_with_distinct_entries([1, 2, 3, 3, 4]) == 3
# assert sol.longest_subarray_with_distinct_entries([1, 2, 2, 3, 4, 5]) == 4
# assert sol.longest_subarray_with_distinct_entries([1, 2, 3, 2, 1]) == 3
# assert sol.longest_subarray_with_distinct_entries([1, 2, 3, 4, 1, 2]) == 4
# assert sol.longest_subarray_with_distinct_entries([3, 1, 2, 1, 3, 4]) == 4
# assert sol.longest_subarray_with_distinct_entries([-1, 0, -1, 1, 0]) == 3
# assert sol.longest_subarray_with_distinct_entries(list(range(10 ** 5))) == 10 ** 5
# assert sol.longest_subarray_with_distinct_entries([i % 500 for i in range(10 ** 5)]) == 500
# assert sol.longest_subarray_with_distinct_entries([0] * 10 ** 5) == 1
# assert sol.longest_subarray_with_distinct_entries([0] + list(range(10 ** 5))) == 10 ** 5
