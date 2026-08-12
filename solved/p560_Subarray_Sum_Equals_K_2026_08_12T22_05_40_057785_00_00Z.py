"""
URL: https://leetcode.com/problems/subarray-sum-equals-k/description/?envType=problem-list-v2&envId=vn57k9wr

560. Subarray Sum Equals K

Given an array of integers nums and an integer k, return the total number of
subarrays whose sum equals to k.

A subarray is a contiguous non-empty sequence of elements within an array.


Example 1:

Input: nums = [1,1,1], k = 2
Output: 2

Example 2:

Input: nums = [1,2,3], k = 3
Output: 2


Constraints:

    1 <= nums.length <= 2 * 10^4
    -1000 <= nums[i] <= 1000
    -10^7 <= k <= 10^7


---

Solved it via brute force, but completely forgot about the prefix sum
method. So i looked up the O(1) solution.

"""

class Solution:

    def subarraySumBruteForce(self, nums: List[int], k: int) -> int:
        prefix = [*accumulate(nums)]
        def get_sum(i, j):
            return prefix[j] - (prefix[i - 1] if i - 1 >= 0 else 0)

        count = 0
        for i in range(len(nums)):
            for j in range(i, len(nums)):
                if get_sum(i, j) == k:
                    count += 1

        return count


    def subarraySum(self, nums: List[int], k: int) -> int:
        res = 0
        prefix = 0
        D = defaultdict(int)
        D[0] = 1
        for n in nums:
            prefix += n
            if prefix - k in D:
                res += D[prefix - k]
            D[prefix] += 1
        return res



sol = Solution()

print(sol.subarraySum([1, 2, 3, 4, 3, 2, 1], 10))

assert sol.subarraySum([1, 1, 1], 2) == 2
assert sol.subarraySum([1, 2, 3], 3) == 2
assert sol.subarraySum([1], 1) == 1
assert sol.subarraySum([1], 0) == 0
assert sol.subarraySum([5], 5) == 1
assert sol.subarraySum([-1], -1) == 1
assert sol.subarraySum([0, 0, 0], 0) == 6
assert sol.subarraySum([0, 0, 0, 0, 0], 0) == 15
assert sol.subarraySum([-1, -1, 1], 0) == 1
assert sol.subarraySum([1, -1, 1, -1], 0) == 4
assert sol.subarraySum([-1, -2, -3], -3) == 2
assert sol.subarraySum([2, 2, 2], 6) == 1
assert sol.subarraySum([2, 2, 2], 4) == 2
assert sol.subarraySum([2, 2, 2], 2) == 3
assert sol.subarraySum([1, 2, 3], 100) == 0
assert sol.subarraySum([1, 2, 3], -1) == 0
assert sol.subarraySum([3, 4, 7, 2, -3, 1, 4, 2], 7) == 4
assert sol.subarraySum([1000, -1000, 1000], 1000) == 3
assert sol.subarraySum([1, 2, 1, 2, 1], 3) == 4
assert sol.subarraySum([0, 1, 0], 1) == 4
assert sol.subarraySum([1] * 100, 1) == 100
assert sol.subarraySum(list(range(1, 11)), 55) == 1