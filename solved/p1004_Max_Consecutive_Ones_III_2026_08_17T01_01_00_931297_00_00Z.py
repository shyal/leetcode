"""
URL: https://leetcode.com/problems/max-consecutive-ones-iii/description/?envType=problem-list-v2&envId=vn57k9wr

1004. Max Consecutive Ones III

Given a binary array nums and an integer k, return the maximum number of
consecutive 1's in the array if you can flip at most k 0's.


Example 1:

Input: nums = [1,1,1,0,0,0,1,1,1,1,0], k = 2
Output: 6
Explanation: [1,1,1,0,0,1,1,1,1,1,1]
Flipped numbers (positions 5 and 10) were flipped from 0 to 1. The longest
subarray is the last 6 elements.

Example 2:

Input: nums = [0,0,1,1,0,0,1,1,1,0,1,1,0,0,0,1,1,1,1], k = 3
Output: 10
Explanation: [0,0,1,1,1,1,1,1,1,1,1,1,0,0,0,1,1,1,1]
Flipped numbers (positions 4, 5, and 9) were flipped from 0 to 1. The longest
subarray spans indices 2 through 11.


Constraints:

    1 <= nums.length <= 10^5
    nums[i] is either 0 or 1.
    0 <= k <= nums.length

---

Did ok but tripped up on the end due to window bookkeeping.
Also there was an invalid assert which tripped me up.
So i got assisted to finish it off.

"""

class Solution:
    def acc(self, nums):
        self.ones  = list(accumulate(int(x == 1) for x in nums))
        self.zeros = list(accumulate(int(x == 0) for x in nums))

    def count(self, i, j, k):
        ones = self.ones[j] - (self.ones[i-1] if i > 0 else 0)
        zeros = self.zeros[j] - (self.zeros[i-1] if i > 0 else 0)
        res = ones + min(zeros, k)
        return res, zeros > k

    def longestOnes(self, nums: List[int], k: int) -> int:
        self.prefix = []
        self.acc(nums)
        _max = 0
        left, right = 0, 0
        while right < len(nums):
            count, cont = self.count(left, right, k)
            if cont:
                left += 1
            else:
                _max = max(_max, count)
                right += 1
        return _max



sol = Solution()

print(sol.longestOnes([1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0], 2))  # 6

assert sol.longestOnes([1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0], 2) == 6
assert sol.longestOnes([0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1], 3) == 10
assert sol.longestOnes([1], 0) == 1
assert sol.longestOnes([0], 0) == 0
# assert sol.longestOnes([0], 1) == 1
assert sol.longestOnes([1, 1, 1], 0) == 3
assert sol.longestOnes([0, 0, 0], 0) == 0
assert sol.longestOnes([0, 0, 0], 3) == 3
assert sol.longestOnes([0, 0, 0], 1) == 1
assert sol.longestOnes([1, 0, 1, 1, 0, 1, 1, 1], 0) == 3
assert sol.longestOnes([1, 0, 1, 0, 1], 1) == 3
assert sol.longestOnes([1, 0, 1, 0, 1], 2) == 5
assert sol.longestOnes([0, 1, 0, 1], 2) == 4
assert sol.longestOnes([1, 1, 0, 0, 1, 1, 1, 0, 1], 1) == 5
assert sol.longestOnes([0, 1, 1, 0, 0, 1], 2) == 5
assert sol.longestOnes([0, 0, 0, 1], 4) == 4
assert sol.longestOnes([1, 1, 1, 1], 2) == 4
assert sol.longestOnes([0, 1, 1, 1, 0], 0) == 3
# assert sol.longestOnes([0] * 100 + [1] * 5 + [0] * 100, 2) == 9
# assert sol.longestOnes([1] * 1000, 0) == 1000