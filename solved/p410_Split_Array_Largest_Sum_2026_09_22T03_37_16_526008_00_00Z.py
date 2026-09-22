"""
URL: https://leetcode.com/problems/split-array-largest-sum/description/?envType=problem-list-v2&envId=vn57k9wr

410. Split Array Largest Sum

Given an integer array nums and an integer k, split nums into k non-empty subarrays such that the largest sum of any subarray is minimized.

Return the minimized largest sum of the split.

A subarray is a contiguous part of the array.

Example 1:

Input: nums = [7,2,5,10,8], k = 2
Output: 18
Explanation: There are four ways to split nums into two subarrays.
The best way is to split it into [7,2,5] and [10,8], where the largest sum among the two subarrays is only 18.

Example 2:

Input: nums = [1,2,3,4,5], k = 2
Output: 9
Explanation: There are four ways to split nums into two subarrays.
The best way is to split it into [1,2,3] and [4,5], where the largest sum among the two subarrays is only 9.

Constraints:

    1 <= nums.length <= 1000
    0 <= nums[i] <= 10^6
    1 <= k <= min(50, nums.length)

---

Sadly i saw a hint that the solution is BS.

The solution is intuitive with k == 2: we can simply use
range queries.

However with k == 3... it gets more complicated.

Input: nums = [1,2,3,4,5], k = 3

[1][2,3][4,5]

took a hint: Stop searching for the split. Search for the answer instead: pick a number, say 18, and ask a yes/no question about it.

So let's begin with the answer: 18, and k = 2. The answer is the bs. Then the rest is splitting the array.

So it's basically subarray sum equal k with a binary search. possibly.

So we find a subarray equal to our guess: 18, then check if we can split the rest of the array.

And we keep on guessing, looking for the smallest guess.

It could also be a linear search, so the bs is really just an optimization.

[1, 2, 3, 2, 1] k = 3

[1, 2] [3] [2, 1]

So the question really is:

Can we split an array k times, where the maximum is guess.

Which i honestly don't know how to do.

1, 2, 3, 2, 1

Took another hint, to use a running sum.

1, 2, 3, 2, 1
1, 3 cut 3 cut 2, 3

Ok so the split function is the same as for shipping packages in d days.

This:

def canSplit(cap):
    return split(cap) <= k

Is a bit of a leap in intuition.

LEETCODE: Accepted (7 ms, 19.5 MB)
"""


class Solution:
    def splitArray(self, nums: List[int], k: int) -> int:
        return first_true(0, 10**10, lambda x: min_chunks(nums, x) <= k)


sol = Solution()

print(sol.splitArray([7, 2, 5, 10, 8], 2))  # 18

assert sol.splitArray([7, 2, 5, 10, 8], 2) == 18
assert sol.splitArray([1, 2, 3, 4, 5], 2) == 9

assert sol.splitArray([0], 1) == 0
assert sol.splitArray([10**6] * 1000, 1) == 1000000000
assert sol.splitArray([10**6] * 1000, 50) == 20000000
assert sol.splitArray([1] * 1000, 50) == 20
assert sol.splitArray([1] * 1000, 1) == 1000
assert sol.splitArray([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 5) == 15
assert sol.splitArray([5, 5, 5, 5, 5, 5, 5, 5, 5, 5], 3) == 20
assert sol.splitArray([100, 200, 300, 400, 500], 5) == 500
assert sol.splitArray([100, 200, 300, 400, 500], 1) == 1500
assert sol.splitArray([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 10) == 1
assert sol.splitArray([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 5) == 0
assert sol.splitArray([10**6, 1, 10**6, 1, 10**6], 3) == 1000001
