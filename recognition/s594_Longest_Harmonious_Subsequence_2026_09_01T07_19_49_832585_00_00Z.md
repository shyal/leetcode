We define a harmonious array as an array where the difference between its maximum value and its minimum value is **exactly** `1`.

Given an integer array `nums`, return the length of its longest harmonious subsequence among all its possible subsequences.

**Example 1:**

**Input:** nums = [1,3,2,2,5,2,3,7]

**Output:** 5

**Explanation:**

The longest harmonious subsequence is `[3,2,2,2,3]`.

**Example 2:**

**Input:** nums = [1,2,3,4]

**Output:** 2

**Explanation:**

The longest harmonious subsequences are `[1,2]`, `[2,3]`, and `[3,4]`, all of which have a length of 2.

**Example 3:**

**Input:** nums = [1,1,1,1]

**Output:** 0

**Explanation:**

No harmonic subsequence exists.

**Constraints:**

- `1 <= nums.length <= 2 * 10^4`
- `-10^9 <= nums[i] <= 10^9`

## <!-- answer -->

The question doesn't specify whether we can sort or not, and sorting is the simplest solution i can think of right now:

[1,3,2,2,5,2,3,7]

becomes

[1,2,2,2,3,3,5,7]

Now it can be a sliding window problem. The right pointer runs, and if the difference between min and mix become more than 1, the left pointer goes in a while loop until the diff between min and max are back to 1. And we record the maximum right - left + 1 we encountered.

There are likely more optimial solutions in O(n) but i can't think of one right now.

<!-- spot {"problem": "594", "target": "counter-build", "reason": "untested, 199 reachable through it", "seconds": 639} -->
