"""
DRILL: Sections Under Cap

Given an array weights and an integer cap, cut weights into the fewest
contiguous sections whose sums are each at most cap, and return how many
sections there are. Every weight is at most cap.

Example 1:

Input: weights = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], cap = 15
Output: 5
Explanation: 1+2+3+4+5, 6+7, 8, 9, 10.

Example 2:

Input: weights = [3, 2, 2, 4, 1, 4], cap = 6
Output: 3
Explanation: 3+2, 2+4, 1+4. The second section's sum equals cap.

Example 3:

Input: weights = [5, 5, 5, 5], cap = 20
Output: 1

Constraints:

    1 <= len(weights) <= 5 * 10^4
    1 <= weights[i] <= cap <= 5 * 10^7

    REQUIRED: one pass, O(n). NO nested loop. A section that is still
    open when the array ends is a section; forgetting it returns one
    too few.
"""


class Solution:

    def sections(self, weights: List[int], cap: int) -> int:
        sections = 1
        total = 0
        for w in weights:
            if w > cap:
                return 0
            if total + w > cap:
                sections += 1
                total = w
            else:
                total += w
        return sections


sol = Solution()

print(sol.sections([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 15))  # 5

assert sol.sections([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 15) == 5
assert sol.sections([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 10) == 7
assert sol.sections([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 55) == 1
assert sol.sections([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 54) == 2
assert sol.sections([3, 2, 2, 4, 1, 4], 6) == 3
assert sol.sections([3, 2, 2, 4, 1, 4], 5) == 4
assert sol.sections([1, 2, 3, 1, 1], 3) == 3
assert sol.sections([5, 5, 5, 5], 5) == 4
assert sol.sections([5, 5, 5, 5], 9) == 4
assert sol.sections([5, 5, 5, 5], 10) == 2
assert sol.sections([5, 5, 5, 5], 20) == 1
assert sol.sections([7], 7) == 1
assert sol.sections([1, 1, 1, 1, 1, 10], 10) == 2
assert sol.sections([10, 1, 1, 1, 1, 1], 10) == 2
assert sol.sections([10, 1, 1, 1, 1, 1], 14) == 2
assert sol.sections([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 4) == 3
