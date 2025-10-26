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

ok here's a strategy: look for a subarray that matches
a certain number (guess), e.g 18.

[7,2,5,(10,8)]

Can we then split the remainder of the array (7,2,5) into k -1
adjacent sets.

If we guess 10:

[(7,2,5),(10),(8)] but we have 3 subarrays, which is too many.

If we guess 5:

[7,2,(5),10,8] now we still have at least 3 subarrays, which is too many.

If we guess 15:

[(7,2,5),(10,8)]


Ugh! I give up. This is too hard. I'm thinking of prefix sum solutions,
binary search etc. but it might be a bit too early still for such
a hard question. Soon though.

"""


class Solution:
    def splitArray(self, nums: List[int], k: int) -> int:
        pass


sol = Solution()

# print(sol.splitArray([7, 2, 5, 10, 8], 2))  # 18

# assert sol.splitArray([7,2,5,10,8], 2) == 18
# assert sol.splitArray([1,2,3,4,5], 2) == 9
# assert sol.splitArray([1,2,3,4,5], 1) == 15
# assert sol.splitArray([1,2,3,4,5], 3) == 6
# assert sol.splitArray([1,2,3,4,5], 5) == 5
# assert sol.splitArray([0], 1) == 0
# assert sol.splitArray([1,1000000], 2) == 1000000
# assert sol.splitArray([1,2,1000000,3], 2) == 1000003
# assert sol.splitArray([1,2,1000000,3], 3) == 1000000
# assert sol.splitArray([7,2,5,10,8], 1) == 32
# assert sol.splitArray([7,2,5,10,8], 5) == 10
# assert sol.splitArray([0,0,0], 2) == 0
# assert sol.splitArray([1000000,1000000], 1) == 2000000
# assert sol.splitArray([1000000,1000000], 2) == 1000000
