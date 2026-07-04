"""
URL: https://leetcode.com/problems/number-of-good-pairs/description/?envType=problem-list-v2&envId=vn57k9wr

1512. Number of Good Pairs

Given an array of integers nums, return the number of good pairs.

A pair (i, j) is called good if nums[i] == nums[j] and i < j.


Example 1:

Input: nums = [1,2,3,1,1,3]
Output: 4
Explanation: There are 4 good pairs (0,3), (0,4), (3,4), (2,5) 0-indexed.

Example 2:

Input: nums = [1,1,1,1]
Output: 6
Explanation: Each pair in the array are good.

Example 3:

Input: nums = [1,2,3]
Output: 0


Constraints:

    1 <= nums.length <= 100
    1 <= nums[i] <= 100
"""


class Solution:
    def numIdenticalPairs(self, nums: List[int]) -> int:
        return int(sum((n * ( n - 1)) / 2 for n in Counter(nums).values()))


sol = Solution()

print(sol.numIdenticalPairs([1, 2, 3, 1, 1, 3]))  # 4

assert sol.numIdenticalPairs([1, 2, 3, 1, 1, 3]) == 4
assert sol.numIdenticalPairs([1, 1, 1, 1]) == 6
assert sol.numIdenticalPairs([1, 2, 3]) == 0
assert sol.numIdenticalPairs([1]) == 0
assert sol.numIdenticalPairs([100]) == 0
assert sol.numIdenticalPairs([7, 7]) == 1
assert sol.numIdenticalPairs([1, 100]) == 0
assert sol.numIdenticalPairs([2, 2, 2]) == 3
assert sol.numIdenticalPairs([3, 3, 3, 3, 3]) == 10
assert sol.numIdenticalPairs([1, 2, 1, 2, 1, 2]) == 6
assert sol.numIdenticalPairs([100, 1, 100, 1, 100]) == 4
assert sol.numIdenticalPairs([1, 2, 3, 4, 5]) == 0
assert sol.numIdenticalPairs([100] * 100) == 4950
assert sol.numIdenticalPairs(list(range(1, 101))) == 0
assert sol.numIdenticalPairs([1, 1] + list(range(2, 100))) == 1