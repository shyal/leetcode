"""
EPI 5.4 Advancing through an array

Given a list of non-negative integers A, you start at index 0. From
index i you can move forward by any number of steps from 0 to A[i].
Return True if you can reach the last index, and False if not.

Example 1:

Input: A = [3, 3, 1, 0, 2, 0, 1]
Output: True
Explanation: 0 -> 1 -> 4 -> 6.

Example 2:

Input: A = [3, 2, 0, 0, 2, 0, 1]
Output: False
Explanation: No index from 0 to 3 can move past index 3, and A[3] = 0.

Example 3:

Input: A = [0]
Output: True
Explanation: Index 0 is the last index.

Constraints:

    1 <= len(A) <= 10^5
    0 <= A[i] <= 10^5

    REQUIRED: O(n) time, O(1) extra space. NO recursion.
"""


class Solution:
    def can_reach_end(self, A: list[int]) -> bool:
        pass


sol = Solution()

print(sol.can_reach_end([3, 3, 1, 0, 2, 0, 1]))  # True

# assert sol.can_reach_end([3, 3, 1, 0, 2, 0, 1]) is True
# assert sol.can_reach_end([3, 2, 0, 0, 2, 0, 1]) is False
# assert sol.can_reach_end([0]) is True
# assert sol.can_reach_end([5]) is True
# assert sol.can_reach_end([0, 1]) is False
# assert sol.can_reach_end([1, 0]) is True
# assert sol.can_reach_end([2, 0, 0]) is True
# assert sol.can_reach_end([1, 0, 1]) is False
# assert sol.can_reach_end([1, 1, 1, 1]) is True
# assert sol.can_reach_end([4, 0, 0, 0, 0]) is True
# assert sol.can_reach_end([3, 0, 0, 0, 1]) is False
# assert sol.can_reach_end([2, 3, 1, 1, 4]) is True
# assert sol.can_reach_end([3, 2, 1, 0, 4]) is False
# assert sol.can_reach_end([1] * 10 ** 5) is True
# assert sol.can_reach_end([10 ** 5] + [0] * (10 ** 5 - 1)) is True
# assert sol.can_reach_end([1] * 50000 + [0] + [1] * 49999) is False
# assert sol.can_reach_end([2, 0] * 50000) is True
