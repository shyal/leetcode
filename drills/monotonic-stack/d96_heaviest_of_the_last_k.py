"""
DRILL: Heaviest Of The Last K

Crates roll off a belt one at a time and weights[i] is the weight of the
i-th crate. Given weights and an integer k, return res, where res[i] is
the heaviest weight among crate i and the k - 1 crates before it. Near
the start there are fewer than k crates, so use the ones there are.
Keep the candidates in a monotonic queue.

Example 1:

Input: weights = [1, 3, -1, -3, 5, 3, 6, 7], k = 3
Output: [1, 3, 3, 3, 5, 5, 6, 7]
Explanation: res[3] looks at 3, -1, -3 and res[4] at -1, -3, 5.

Example 2:

Input: weights = [4, 4, 2, 2], k = 2
Output: [4, 4, 4, 2]
Explanation: res[2] looks at 4, 2. The first 4 is out of reach by then.

Constraints:

    1 <= k <= len(weights) <= 10^5
    -10^4 <= weights[i] <= 10^4

    REQUIRED: one pass, O(n) total. Each crate is appended once and
    popped at most once. NO max() over a slice, NO heap.
"""


class Solution:
    def heaviestOfLastK(self, weights: list[int], k: int) -> list[int]:
        pass


sol = Solution()

print(sol.heaviestOfLastK([1, 3, -1, -3, 5, 3, 6, 7], 3))  # [1, 3, 3, 3, 5, 5, 6, 7]

# assert sol.heaviestOfLastK([1, 3, -1, -3, 5, 3, 6, 7], 3) == [1, 3, 3, 3, 5, 5, 6, 7]
# assert sol.heaviestOfLastK([4, 4, 2, 2], 2) == [4, 4, 4, 2]
# assert sol.heaviestOfLastK([5], 1) == [5]
# assert sol.heaviestOfLastK([5, 4, 3, 2, 1], 1) == [5, 4, 3, 2, 1]
# assert sol.heaviestOfLastK([5, 4, 3, 2, 1], 2) == [5, 5, 4, 3, 2]
# assert sol.heaviestOfLastK([1, 2, 3, 4, 5], 3) == [1, 2, 3, 4, 5]
# assert sol.heaviestOfLastK([2, 2, 2, 2], 3) == [2, 2, 2, 2]
# assert sol.heaviestOfLastK([9, 1, 1, 1, 1], 3) == [9, 9, 9, 1, 1]
# assert sol.heaviestOfLastK([1, 3, 1, 2, 0, 5], 3) == [1, 3, 3, 3, 2, 5]
# assert sol.heaviestOfLastK([-1, -3, -5, -7], 2) == [-1, -1, -3, -5]
# assert sol.heaviestOfLastK([1, 2, 3, 4, 5], 5) == [1, 2, 3, 4, 5]
