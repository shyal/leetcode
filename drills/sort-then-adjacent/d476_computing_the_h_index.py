"""
EPI 13.3 Computing the h-index

Given a list of integers citations, where citations[i] is the number of
citations of paper i, return the h-index: the largest h such that at
least h papers have at least h citations each.

Example 1:

Input: citations = [4, 1, 7, 2, 9]
Output: 3
Explanation: the papers with 4, 7 and 9 citations have at least 3 each.
There are not 4 papers with at least 4 citations.

Example 2:

Input: citations = [0, 0]
Output: 0

Example 3:

Input: citations = [10]
Output: 1
Explanation: there is only a single paper, so h cannot pass 1.

Constraints:

    0 <= len(citations) <= 10^5
    0 <= citations[i] <= 10^9

    REQUIRED: O(n log n) time, where n is the length of citations.
"""


class Solution:
    def h_index(self, citations: list[int]) -> int:
        pass


sol = Solution()

print(sol.h_index([4, 1, 7, 2, 9]))  # 3

# assert sol.h_index([4, 1, 7, 2, 9]) == 3
# assert sol.h_index([0, 0]) == 0
# assert sol.h_index([10]) == 1
# assert sol.h_index([]) == 0
# assert sol.h_index([0]) == 0
# assert sol.h_index([1]) == 1
# assert sol.h_index([1, 1, 1]) == 1
# assert sol.h_index([2, 2, 2]) == 2
# assert sol.h_index([3, 3, 3]) == 3
# assert sol.h_index([5, 5, 5]) == 3
# assert sol.h_index([1, 2, 3, 4, 5]) == 3
# assert sol.h_index([0, 0, 4, 4]) == 2
# assert sol.h_index([10 ** 5] * 10 ** 5) == 10 ** 5
# assert sol.h_index(list(range(10 ** 5))) == 50000
# assert sol.h_index([0] * 10 ** 5) == 0
