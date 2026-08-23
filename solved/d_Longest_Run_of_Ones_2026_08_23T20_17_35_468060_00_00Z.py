"""
DRILL: Longest Run of Ones
TRAINS: sliding-window-variable

Given a binary array nums, return the length of the longest run of
consecutive 1s.

The point of this drill is the loop shape: at every step the window
either grows by one on the right, or shifts right by one at the same
width. A window of pure 1s grows; a window holding a zero shifts. The
width can only grow, so the final width is the answer.

Example 1:

Input: nums = [1, 1, 0, 1, 1, 1]
Output: 3
Explanation: the run at indices 3 to 5.

Example 2:

Input: nums = [1, 0, 1, 1, 0, 1]
Output: 2

Example 3:

Input: nums = [0, 0, 0]
Output: 0

Constraints:

    1 <= len(nums) <= 10^5
    nums[i] is 0 or 1.

    REQUIRED: one pass, O(n), O(1) extra space. Two pointers, and left
    advances at most ONCE per element read: use `if`, NEVER `while`.
    The answer is the final width, len(nums) - left, taken once after
    the loop. A plain streak counter solves this problem while skipping
    the slide, and the slide is the rep.


---

Forgot `if nums[left] == 0:`. Assisted / learning.


"""


class Solution:
    def findMaxConsecutiveOnes(self, nums: List[int]) -> int:
        zeros = 0
        left = 0
        best = 0
        for right in range(len(nums)):
            if nums[right] == 0:
                zeros += 1
            if zeros > 0:
                if nums[left] == 0:
                    zeros -= 1
                left += 1
            best = max(best, right - left + 1)
        return best


sol = Solution()

assert sol.findMaxConsecutiveOnes([1, 1, 0, 1, 1, 1]) == 3
assert sol.findMaxConsecutiveOnes([1, 0, 1, 1, 0, 1]) == 2
assert sol.findMaxConsecutiveOnes([0, 0, 0]) == 0
assert sol.findMaxConsecutiveOnes([1, 1, 1, 1]) == 4
assert sol.findMaxConsecutiveOnes([1]) == 1
assert sol.findMaxConsecutiveOnes([0]) == 0
assert sol.findMaxConsecutiveOnes([0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1]) == 4
assert sol.findMaxConsecutiveOnes([1, 0, 1, 0, 1, 0]) == 1
assert sol.findMaxConsecutiveOnes([0, 0, 1, 1]) == 2
assert sol.findMaxConsecutiveOnes([1, 1, 0, 0, 1]) == 2

print("All tests passed!")
