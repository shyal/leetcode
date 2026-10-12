"""
DRILL: Split Into A Run
TRAINS: consecutive-sum-split

Given two positive integers n and k, return True if n is the sum of k
consecutive positive integers, and False otherwise.

Example 1:

Input: n = 15, k = 3
Output: True
Explanation: 15 = 4 + 5 + 6.

Example 2:

Input: n = 15, k = 4
Output: False
Explanation: 3 + 4 + 5 + 6 = 18 and 2 + 3 + 4 + 5 = 14. No run of four
positive integers sums to 15.

Example 3:

Input: n = 15, k = 6
Output: False
Explanation: The smallest run of six positive integers, 1 + 2 + 3 + 4 + 5 + 6,
already sums to 21.

Constraints:

    1 <= n <= 10^9
    1 <= k <= 10^5

    REQUIRED: O(1), arithmetic on n and k only. NO loop. NO search for the
    first integer of the run.
"""


class Solution:

    def splitIntoRun(self, n: int, k: int) -> bool:
        pass


sol = Solution()

print(sol.splitIntoRun(15, 3))  # True

# assert sol.splitIntoRun(15, 3) is True
# assert sol.splitIntoRun(15, 4) is False
# assert sol.splitIntoRun(15, 6) is False
# assert sol.splitIntoRun(15, 1) is True
# assert sol.splitIntoRun(15, 2) is True
# assert sol.splitIntoRun(15, 5) is True
# assert sol.splitIntoRun(16, 2) is False
# assert sol.splitIntoRun(16, 3) is False
# assert sol.splitIntoRun(16, 4) is False
# assert sol.splitIntoRun(16, 5) is False
# assert sol.splitIntoRun(9, 2) is True
# assert sol.splitIntoRun(9, 3) is True
# assert sol.splitIntoRun(1, 1) is True
# assert sol.splitIntoRun(1, 2) is False
# assert sol.splitIntoRun(3, 2) is True
# assert sol.splitIntoRun(10 ** 9, 44721) is False
# assert sol.splitIntoRun(10 ** 9, 44720) is False
# assert sol.splitIntoRun(10 ** 9, 25) is True
# assert sol.splitIntoRun(10 ** 9, 10 ** 5) is False
