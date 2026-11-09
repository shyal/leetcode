"""
EPI 16.12 Find the longest nondecreasing subsequence

Given a list A of integers, return the length of the longest
subsequence of A whose entries are nondecreasing: each entry is at
least the entry before it. A subsequence keeps the order of A and may
skip entries.

Example 1:

Input: A = [3, 1, 2, 2, 5, 4]
Output: 4
Explanation: [1, 2, 2, 5] and [1, 2, 2, 4].

Example 2:

Input: A = [5, 4, 3, 2, 1]
Output: 1

Example 3:

Input: A = [2, 2, 2, 2]
Output: 4
Explanation: equal entries are nondecreasing.

Constraints:

    1 <= len(A) <= 1000
    -10^4 <= A[i] <= 10^4

    REQUIRED: O(len(A)^2) time and O(len(A)) extra space. NO
    enumeration of subsequences.
"""


class Solution:
    def longest_nondecreasing_subsequence_length(self, A: list[int]) -> int:
        pass


sol = Solution()

print(sol.longest_nondecreasing_subsequence_length([3, 1, 2, 2, 5, 4]))  # 4

# assert sol.longest_nondecreasing_subsequence_length([3, 1, 2, 2, 5, 4]) == 4
# assert sol.longest_nondecreasing_subsequence_length([5, 4, 3, 2, 1]) == 1
# assert sol.longest_nondecreasing_subsequence_length([2, 2, 2, 2]) == 4
# assert sol.longest_nondecreasing_subsequence_length([7]) == 1
# assert sol.longest_nondecreasing_subsequence_length([1, 2, 3]) == 3
# assert sol.longest_nondecreasing_subsequence_length([3, 1, 4, 1, 5, 9, 2, 6]) == 4
# assert sol.longest_nondecreasing_subsequence_length([0, 1, 0, 1, 0, 1]) == 4
# assert sol.longest_nondecreasing_subsequence_length([9, 1, 2, 3]) == 3
# assert sol.longest_nondecreasing_subsequence_length([1, 2, 3, 0]) == 3
# assert sol.longest_nondecreasing_subsequence_length([-5, -5, -10, -1]) == 3
# assert sol.longest_nondecreasing_subsequence_length(list(range(1000, 0, -1))) == 1
# assert sol.longest_nondecreasing_subsequence_length([5] * 1000) == 1000
# assert sol.longest_nondecreasing_subsequence_length([(i * 37) % 101 for i in range(1000)]) == 40
