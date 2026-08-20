"""
DRILL: Slide, Never Shrink
TRAINS: sliding-window-variable

Given a binary array nums and an integer k, return the length of the
longest run of consecutive 1s you can make by flipping at most k zeros
to 1.

The point of this drill is the loop shape, not the answer. Only the
longest run is wanted, so the window never has to give ground: at every
step it either grows by one on the right, or shifts right by one without
changing width. It never gets narrower, so its final width is the answer.

Example 1:

Input: nums = [1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0], k = 2
Output: 6
Explanation: flipping the two zeros at indices 4 and 5 gives six
consecutive 1s from index 5 to index 10.

Example 2:

Input: nums = [0, 0, 0], k = 0
Output: 0

Example 3:

Input: nums = [1, 1, 1], k = 2
Output: 3
Explanation: k may exceed the number of zeros present.

Constraints:

    1 <= len(nums) <= 10^5
    0 <= k <= len(nums)
    nums[i] is 0 or 1.

    REQUIRED: one pass, O(n), O(1) extra space. left advances at most
    ONCE per element read: use `if`, NEVER `while`. The width never
    decreases, so the answer is the final width, len(nums) - left, and
    no running maximum is needed. Shrinking back to a legal window on
    every step is the failure mode this drill exists to kill: it is the
    shape of Grow and Shrink, and writing it here means the drill was
    not attempted. A window that is briefly illegal is fine, because a
    wider legal one was already seen.
"""


class Solution:
    def longestOnes(self, nums: List[int], k: int) -> int:
        pass


sol = Solution()

assert sol.longestOnes([1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0], 2) == 6
assert sol.longestOnes([0, 0, 0], 0) == 0
assert sol.longestOnes([1, 1, 1], 2) == 3
assert sol.longestOnes([0], 1) == 1
assert sol.longestOnes([0], 0) == 0
assert sol.longestOnes([1], 0) == 1
assert sol.longestOnes([0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1], 3) == 10
assert sol.longestOnes([1, 0, 1, 0, 1], 1) == 3
assert sol.longestOnes([1, 0, 1, 0, 1], 2) == 5
assert sol.longestOnes([0, 1, 1, 1, 0], 0) == 3
assert sol.longestOnes([1, 1, 0, 0, 1, 1, 1, 0, 1], 1) == 5
assert sol.longestOnes([0, 0, 0, 1], 4) == 4

print("All tests passed!")
