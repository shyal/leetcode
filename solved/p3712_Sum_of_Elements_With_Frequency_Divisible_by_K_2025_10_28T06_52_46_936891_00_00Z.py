"""
URL: https://leetcode.com/problems/sum-of-elements-with-frequency-divisible-by-k/description/?envType=problem-list-v2&envId=vn57k9wr

3712. Sum of Elements With Frequency Divisible by K

You are given an integer array nums and an integer k.

Return an integer denoting the sum of all elements in nums whose frequency is divisible by k, or 0 if there are no such elements.

Note: An element is included in the sum exactly as many times as it appears in the array if its total frequency is divisible by k.

Example 1:

Input: nums = [1,2,2,3,3,3,3,4], k = 2
Output: 16
Explanation:
- The number 1 appears once (odd frequency).
- The number 2 appears twice (even frequency).
- The number 3 appears four times (even frequency).
- The number 4 appears once (odd frequency).
So, the total sum is 2 + 2 + 3 + 3 + 3 + 3 = 16.

Example 2:

Input: nums = [1,2,3,4,5], k = 2
Output: 0
Explanation:
There are no elements that appear an even number of times, so the total sum is 0.

Example 3:

Input: nums = [4,4,4,1,2,3], k = 3
Output: 12
Explanation:
- The number 1 appears once.
- The number 2 appears once.
- The number 3 appears once.
- The number 4 appears three times.
So, the total sum is 4 + 4 + 4 = 12.

Constraints:
- 1 <= nums.length <= 100
- 1 <= nums[i] <= 100
- 1 <= k <= 100
"""


class Solution:
    def sumDivisibleByK(self, nums: List[int], k: int) -> int:
        counts = Counter(nums)
        return sum(item * count for item, count in counts.items() if count % k == 0)


sol = Solution()

# print(sol.sumDivisibleByK([1, 2, 2, 3, 3, 3, 3, 4], 2))  # 16

assert sol.sumDivisibleByK([1, 2, 2, 3, 3, 3, 3, 4], 2) == 16
assert sol.sumDivisibleByK([1, 2, 3, 4, 5], 2) == 0
assert sol.sumDivisibleByK([4, 4, 4, 1, 2, 3], 3) == 12
assert sol.sumDivisibleByK([1], 1) == 1
assert sol.sumDivisibleByK([1], 2) == 0
assert sol.sumDivisibleByK([2, 2], 2) == 4
assert sol.sumDivisibleByK([1, 1, 1], 3) == 3
assert sol.sumDivisibleByK([1, 1, 1, 1], 2) == 4
assert sol.sumDivisibleByK([5, 5, 5, 5, 5], 5) == 25
assert sol.sumDivisibleByK([1, 2, 3], 1) == 6
assert sol.sumDivisibleByK([1, 1, 2, 2, 2, 3, 3, 3, 3], 2) == 14
assert sol.sumDivisibleByK([100] * 100, 100) == 10000
assert sol.sumDivisibleByK([100] * 100, 99) == 0
assert sol.sumDivisibleByK([1, 2, 1, 2, 1, 2], 3) == 9
assert sol.sumDivisibleByK([1, 1, 2, 2, 3, 3, 4, 4, 5, 5], 2) == 30
assert sol.sumDivisibleByK([10] * 99, 100) == 0
assert sol.sumDivisibleByK([1] * 1 + [2] * 2 + [3] * 3, 1) == 14
assert sol.sumDivisibleByK([99, 99, 99, 100, 100], 2) == 200
assert sol.sumDivisibleByK([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 10) == 0
