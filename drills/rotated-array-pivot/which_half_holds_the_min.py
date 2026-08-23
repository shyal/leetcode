"""
DRILL: Which Half Holds the Min
TRAINS: rotated-array-pivot

Given a rotated sorted array nums of distinct integers and an index mid,
return "left" when the minimum of nums sits at mid or to its left, and
"right" when it sits to the right of mid.

A rotated sorted array is an ascending array whose first k elements, for
some k with 0 <= k < len(nums), have been moved in order to the back:
with k = 3, [0, 1, 2, 4, 5, 6, 7] becomes [4, 5, 6, 7, 0, 1, 2].

This is the decision inside every rotated-array binary search. The
rotation leaves two ascending runs, and every value in the second run
sits below every value in the first. The minimum starts the second run,
and the last element always belongs to it.

Example 1:

Input: nums = [4, 5, 6, 7, 0, 1, 2], mid = 3
Output: "right"
Explanation: the minimum 0 sits at index 4, right of mid.

Example 2:

Input: nums = [4, 5, 6, 7, 0, 1, 2], mid = 4
Output: "left"
Explanation: the minimum sits at mid itself.

Example 3:

Input: nums = [1, 2, 3, 4, 5], mid = 2
Output: "left"
Explanation: an array with k = 0 is still rotated sorted; its minimum
is at index 0.

Constraints:

    1 <= len(nums) <= 10^4
    -10^4 <= nums[i] <= 10^4
    All values in nums are distinct.
    0 <= mid < len(nums)

    REQUIRED: O(1), a single comparison of nums[mid] against the last
    element. NO loop, NO scan, NO min(). A scan finds the minimum while
    skipping the decision, and the decision is the rep.
"""


class Solution:
    def minSide(self, nums: List[int], mid: int) -> str:
        pass


sol = Solution()

print(sol.minSide([4, 5, 6, 7, 0, 1, 2], 3))  # "right"

# assert sol.minSide([4, 5, 6, 7, 0, 1, 2], 3) == "right"
# assert sol.minSide([4, 5, 6, 7, 0, 1, 2], 4) == "left"
# assert sol.minSide([4, 5, 6, 7, 0, 1, 2], 5) == "left"
# assert sol.minSide([4, 5, 6, 7, 0, 1, 2], 0) == "right"
# assert sol.minSide([4, 5, 6, 7, 0, 1, 2], 6) == "left"
# assert sol.minSide([1, 2, 3, 4, 5], 2) == "left"
# assert sol.minSide([1, 2, 3, 4, 5], 0) == "left"
# assert sol.minSide([1, 2, 3, 4, 5], 4) == "left"
# assert sol.minSide([2, 3, 4, 5, 1], 1) == "right"
# assert sol.minSide([2, 3, 4, 5, 1], 3) == "right"
# assert sol.minSide([2, 3, 4, 5, 1], 4) == "left"
# assert sol.minSide([5, 1, 2, 3, 4], 0) == "right"
# assert sol.minSide([5, 1, 2, 3, 4], 1) == "left"
# assert sol.minSide([2, 1], 0) == "right"
# assert sol.minSide([1, 2], 0) == "left"
# assert sol.minSide([1], 0) == "left"
