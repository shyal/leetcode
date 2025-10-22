"""
URL: https://leetcode.com/problems/partition-equal-subset-sum/description/

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

Ok so the trick here is to generate a subset that's equal to half the sum of nums.
So already, we if the sum is not divisible by 2, then it's not possible.

There are multiple approaches here, but this most efficient might be
to generate subsets with a prefix.

Apparently not. This hits a TLE.

Ok finally passed after several submissions to overcome TLEs.

Would be good to revisit this, with the most optimal solution.

"""


class Solution:
    def canPartitionBruteForce(self, nums: List[int]) -> bool:
        """
        This solution isn't very efficient, as we're recompute the sum for
        each combination.
        """
        n = sum(nums)
        if n % 2:
            return False
        combs = chain(*(combinations(nums, x) for x in range(1, len(nums) + 1)))
        return any(sum(comb) == n // 2 for comb in combs)

    def canPartitionsubsets(self, nums: List[int]) -> bool:
        """
        This time around, we generate subsets manually, and check if
        their sub is half of n, not super efficient, but can build on
        this.
        """
        n = sum(nums)
        if n % 2:
            return False

        def subsets(i, subset):
            if sum(subset) == n // 2:
                return True
            for j in range(i, len(nums)):
                if subsets(j + 1, subset + [nums[i]]):
                    return True
            return False

        return subsets(0, [])

    def canPartition(self, nums: List[int]) -> bool:
        """
        Optimal solution:
        - Compute subsets
            - Compute prefix
            - if prefix sum is double sum of nums, return True
        """
        n = sum(nums)
        if n % 2:
            return False

        @cache
        def subsets(i, prefix):
            if prefix == n // 2:
                return True
            if prefix > n // 2:
                return False
            for j in range(i, len(nums)):
                r = subsets(j + 1, prefix + nums[j])
                if r == True:
                    return True
            return False

        nums.sort(reverse=True)

        return subsets(0, 0)


sol = Solution()
TLE = [
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    99,
    97,
]
res = sol.canPartition(nums=TLE)
assert res == False
TLE = [
    5,
    79,
    2,
    4,
    8,
    16,
    32,
    64,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
]


res = sol.canPartition(nums=TLE)
assert res == True

res = sol.canPartition(nums=[1, 5, 11, 5])
assert res == True
res = sol.canPartition(nums=[1, 2, 3, 5])
assert res == False
res = sol.canPartition(nums=[1])
assert res == False
res = sol.canPartition(nums=[1, 1])
assert res == True
res = sol.canPartition(nums=[2])
assert res == False
res = sol.canPartition(nums=[1, 2, 3])
assert res == True
res = sol.canPartition(nums=[1, 2, 5])
assert res == False
res = sol.canPartition(nums=[100, 100])
assert res == True
res = sol.canPartition(nums=[99, 100])
assert res == False
res = sol.canPartition(nums=[1, 1, 1, 97])
assert res == False
res = sol.canPartition(nums=[1, 2, 3, 4])
assert res == True
res = sol.canPartition(nums=[3, 3, 3, 3, 3])
assert res == False
res = sol.canPartition(nums=[2, 2, 2, 2])
assert res == True
res = sol.canPartition(nums=[1, 3, 4, 8])
assert res == True
res = sol.canPartition(nums=[9, 1, 1, 1])
assert res == False
res = sol.canPartition(nums=[100, 80, 30])
assert res == False
