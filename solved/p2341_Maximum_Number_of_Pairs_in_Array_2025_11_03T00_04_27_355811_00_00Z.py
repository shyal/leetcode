"""
URL: https://leetcode.com/problems/maximum-number-of-pairs-in-array/description/?envType=problem-list-v2&envId=vn57k9wr

2341. Maximum Number of Pairs in Array

You are given a 0-indexed integer array nums. In one operation, you may do the following:

- Choose two integers in nums that are equal.
- Remove both integers from nums, forming a pair.

The operation is done on nums as many times as possible.

Return a 0-indexed integer array answer of size 2 where answer[0] is the number of pairs that are formed and answer[1] is the number of leftover integers in nums after doing the operation as many times as possible.

Example 1:

Input: nums = [1,3,2,1,3,2,2]
Output: [3,1]
Explanation:
Form a pair with nums[0] and nums[3] and remove them from nums. Now, nums = [3,2,3,2,2].
Form a pair with nums[0] and nums[2] and remove them from nums. Now, nums = [2,2,2].
Form a pair with nums[0] and nums[1] and remove them from nums. Now, nums = [2].
No more pairs can be formed. A total of 3 pairs have been formed, and there is 1 number leftover in nums.

Example 2:

Input: nums = [1,1]
Output: [1,0]
Explanation: Form a pair with nums[0] and nums[1] and remove them from nums. Now, nums = [].
No more pairs can be formed. A total of 1 pair has been formed, and there are 0 numbers leftover in nums.

Example 3:

Input: nums = [0]
Output: [0,1]
Explanation: No pairs can be formed, and there is 1 number leftover in nums.

Constraints:

- 1 <= nums.length <= 100
- 0 <= nums[i] <= 100
"""


class Solution:
    def numberOfPairs(self, nums: List[int]) -> List[int]:
        pairs = 0
        remaining = 0
        for count in Counter(nums).values():
            if count == 1:
                remaining += 1
            elif count % 2 == 0:
                pairs += count // 2
            else:
                pairs += (count - 1) // 2
                remaining += 1
        return [pairs, remaining]


sol = Solution()

# print(sol.numberOfPairs([1, 3, 2, 1, 3, 2, 2]))  # [3,1]

assert sol.numberOfPairs([1, 3, 2, 1, 3, 2, 2]) == [3, 1]
assert sol.numberOfPairs([1, 1]) == [1, 0]
assert sol.numberOfPairs([0]) == [0, 1]
assert sol.numberOfPairs([1]) == [0, 1]
assert sol.numberOfPairs([1, 1, 1]) == [1, 1]
assert sol.numberOfPairs([1, 1, 1, 1]) == [2, 0]
assert sol.numberOfPairs([1, 2, 3, 4]) == [0, 4]
assert sol.numberOfPairs([0, 0, 0, 0, 0]) == [2, 1]
assert sol.numberOfPairs([100, 100]) == [1, 0]
assert sol.numberOfPairs([1, 1, 2, 2, 3]) == [2, 1]
assert sol.numberOfPairs([5, 5, 5, 5, 5, 5]) == [3, 0]
assert sol.numberOfPairs([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]) == [0, 10]
