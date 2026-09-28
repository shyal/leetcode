"""
URL: https://leetcode.com/problems/partition-equal-subset-sum/description/?envType=problem-list-v2&envId=vn57k9wr

416. Partition Equal Subset Sum

Given an integer array nums, return true if you can partition the array into two subsets such that the sum of the elements in both subsets is equal or false otherwise.

Example 1:

Input: nums = [1,5,11,5]
Output: true
Explanation: The array can be partitioned as [1, 5, 5] and [11].

Example 2:

Input: nums = [1,2,3,5]
Output: false
Explanation: The array cannot be partitioned into equal sum subsets.

Constraints:

    1 <= nums.length <= 200
    1 <= nums[i] <= 100
---
hmm a greedy approach would be sorting, computing the prefix
then looking for a split point
so let's try to falsify this approach

 1 2 3 4 true
 2 3 1 4 true

right, that doesn't work.

The constraints are quite small. 200 numbers.. so would buckets work

0 1 1 1 1

that doesn't help

so this is likely a dp question

1 2 3 4

let's start with a prefix sum

1 3 6 10 doesn't seem to help

let's add some numbers

1 1 2 3 5
1 2 3 | 5 1

the process i ran, was to take 5, then poach the one from the
other side. That nearly sounds like a knapsack problem.

but i can't remember knapsack whatsoever

1 1 2 3 5

right.. so sum the array: 12


then take numbers until you reach 6, then the problem
is simpler: which numbers can i pick to reach 6

Since the constraints are not too bad, we could just go with combinations
which would be a bit of a brute force approach

let's try brute force first
def canPartition(nums: [int]) -> bool
  s = sum(nums)
  if s % 2
    return False
  k = s // 2
  for i in 1..<len(nums)
    for comb in combinations(nums, i)
      if sum(comb) == k
        return True
  False

bf works just fine, but it's too slow
so maybe instead of working with the numbers, we could work with the counts

def canPartition(nums: [int]) -> bool
  c = counter(nums)
  print(c)

working with counts is an optimization, but numbers like 1 2 3 4 5 etc. defeat
the purpose


maybe if we compute combinations by hand, that sum to target

LEETCODE: Time Limit Exceeded (39/149 cases)
"""


# mu 0.6
# def canPartition(nums: [int]) -> bool
#   def helper(i, total)
#       if total == k
#           return True
#       for j in range(i, len(nums))
#           if helper(j + 1, total + nums[i])
#             return True
#       False
#
#   s = sum(nums)
#   if s % 2
#     return False
#   k = s // 2
#   helper(0, 0)

class Solution:
    def canPartition(self, nums: list[int]) -> bool:
        def helper(i, total):
            if total == k:
                return True
            for j in range(i, len(nums)):
                if helper(j + 1, total + nums[i]):
                    return True
            return False
        s = sum(nums)
        if s % 2:
            return False
        k = s // 2
        return helper(0, 0)


sol = Solution()
print(sol.canPartition([1, 5, 11, 5]))
assert sol.canPartition([100] * 200) == True
assert sol.canPartition([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]) == True
assert sol.canPartition([2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]) == True
assert sol.canPartition([1, 5, 11, 5]) == True
assert sol.canPartition([1, 2, 3, 5]) == False
assert sol.canPartition([1]) == False
assert sol.canPartition([2, 2]) == True
assert sol.canPartition([1, 1, 1, 1, 1, 1]) == True
assert sol.canPartition([1] * 199 + [2]) == False
assert sol.canPartition([1, 2, 5, 9, 11, 15]) == False
assert sol.canPartition([3, 3, 3, 4, 5]) == True
assert sol.canPartition([50, 50, 50, 50, 50, 50, 50, 50]) == True
assert sol.canPartition([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]) == False
assert sol.canPartition([1, 99]) == False
