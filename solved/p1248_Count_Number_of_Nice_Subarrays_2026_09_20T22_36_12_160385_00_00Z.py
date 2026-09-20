"""
URL: https://leetcode.com/problems/count-number-of-nice-subarrays/description/?envType=problem-list-v2&envId=vn57k9wr

1248. Count Number of Nice Subarrays

Given an array of integers nums and an integer k. A continuous subarray is called nice if there are k odd numbers on it.

Return the number of nice sub-arrays.

Example 1:

Input: nums = [1,1,2,1,1], k = 3
Output: 2
Explanation: The only sub-arrays with 3 odd numbers are [1,1,2,1] and [1,2,1,1].

Example 2:

Input: nums = [2,4,6], k = 1
Output: 0
Explanation: There are no odd numbers in the array.

Example 3:

Input: nums = [2,2,2,1,2,2,1,2,2,2], k = 2
Output: 16

Constraints:

    1 <= nums.length <= 50000
    1 <= nums[i] <= 10^5
    1 <= k <= nums.length

---

Could not think of the optimal solution.

LEETCODE: Time Limit Exceeded (14/38 cases)
"""


class Solution:
    def numberOfSubarraysBruteForce(self, nums: List[int], k: int) -> int:
        res = []
        for i in range(len(nums)):
            for j in range(i, len(nums)):
                if sum(x % 2 for x in nums[i : j + 1]) == k:
                    res.append(nums[i : j + 1])
        return len(res)

    def numberOfSubarrays(self, nums: List[int], k: int) -> int:
        return self.numberOfSubarraysBruteForce(nums, k)


sol = Solution()

print(sol.numberOfSubarrays([1, 1, 2, 1, 1], 3))  # 2

assert sol.numberOfSubarrays([1, 1, 2, 1, 1], 3) == 2
assert sol.numberOfSubarrays([2, 4, 6], 1) == 0
assert sol.numberOfSubarrays([2, 2, 2, 1, 2, 2, 1, 2, 2, 2], 2) == 16

assert sol.numberOfSubarrays([1], 1) == 1
assert sol.numberOfSubarrays([2], 1) == 0
assert sol.numberOfSubarrays([1, 3, 5, 7, 9], 3) == 3
assert sol.numberOfSubarrays([2, 2, 2, 2, 2], 1) == 0
assert sol.numberOfSubarrays([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 5) == 2
# assert sol.numberOfSubarrays([1] * 50000, 50000) == 1
# assert sol.numberOfSubarrays([2] * 49999 + [1], 1) == 50000
assert sol.numberOfSubarrays([1, 2, 1, 2, 1, 2, 1, 2, 1, 2], 4) == 6
assert sol.numberOfSubarrays([1, 1, 1, 1, 1], 1) == 5
# assert sol.numberOfSubarrays([10**5] * 100 + [1] * 10 + [10**5] * 100, 10) == 10201
assert sol.numberOfSubarrays([1, 1, 2, 2, 1, 1, 2, 2, 1, 1], 4) == 7
assert sol.numberOfSubarrays([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 1) == 18
