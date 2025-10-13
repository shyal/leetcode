"""
URL: https://leetcode.com/problems/top-k-frequent-elements/description/

347. Top K Frequent Elements

Given an integer array nums and an integer k, return the k most frequent elements. You may return the answer in any order.

Example 1:

Input: nums = [1,1,1,2,2,3], k = 2
Output: [1,2]

Example 2:

Input: nums = [1], k = 1
Output: [1]

Constraints:

    1 <= nums.length <= 10^5
    -10^4 <= nums[i] <= 10^4
    k is in the range [1, the number of unique elements in the array].
    It is guaranteed that the answer is unique.

---

This is an easy solve with a Counter, but clearly suboptimal.
"""


class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        c = list(dict(Counter(nums)).items())
        c.sort(key=lambda x: -x[1])
        return [x[0] for x in c[:k]]


sol = Solution()

# print(sol.topKFrequent([1, 1, 1, 2, 2, 3], 2))  # [1, 2]

assert sorted(sol.topKFrequent([1, 1, 1, 2, 2, 3], 2)) == [1, 2]
assert sorted(sol.topKFrequent([1], 1)) == [1]
assert sorted(sol.topKFrequent([7] * 10, 1)) == [7]
assert sorted(sol.topKFrequent([-1, -1, -1, 1, 1, 2], 2)) == [-1, 1]
assert sorted(sol.topKFrequent([1, 2, 3, 4, 5], 5)) == [1, 2, 3, 4, 5]
assert sorted(sol.topKFrequent([0] * 4 + [1] * 2, 2)) == [0, 1]
assert sorted(sol.topKFrequent([-10000] * 3 + [10000] * 1, 1)) == [-10000]
assert sorted(sol.topKFrequent([1] * 5 + [2] * 4 + [3] * 3 + [4] * 2 + [5] * 1, 3)) == [
    1,
    2,
    3,
]
