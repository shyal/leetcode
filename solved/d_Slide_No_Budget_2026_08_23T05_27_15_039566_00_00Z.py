"""
DRILL: Slide, No Budget
TRAINS: sliding-window-variable

Given a binary array nums, return the length of the longest run of
consecutive 1s.

This is Slide, Never Shrink with the budget removed. There are no flips,
so any zero inside the window makes it illegal. The window still never
gives ground: at every step it grows by one on the right, or shifts
right by one without changing width.

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

    REQUIRED: one pass, O(n), O(1) extra space. left advances at most
    ONCE per element read: use `if`, NEVER `while`. Keep no running
    maximum and never reset a counter to zero on reading a zero: the
    width never decreases, so the answer is the final width,
    len(nums) - left. The plain streak counter solves this problem but
    skips the slide, and the slide is the rep: writing it here means
    the drill was not attempted.

---

Assisted. Still learning this pattern. Used max deliberately.
I realise it's not needed.


"""


class Solution:
    def findMaxConsecutiveOnes(self, nums: List[int]) -> int:
        left = 0
        zeros = 0
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
