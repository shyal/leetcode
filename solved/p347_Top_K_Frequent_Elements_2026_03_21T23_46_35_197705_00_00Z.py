"""
URL: https://leetcode.com/problems/top-k-frequent-elements/description/?envType=problem-list-v2&envId=vn57k9wr

347. Top K Frequent Elements

Given an integer array nums and an integer k, return the k most frequent elements. You may return the answer in any order.

Example 1:

Input: nums = [1,1,1,2,2,3], k = 2
Output: [1,2]

Example 2:

Input: nums = [1], k = 1
Output: [1]

Example 3:

Input: nums = [1,2,1,2,1,2,3,1,3,2], k = 2
Output: [1,2]

Constraints:

    1 <= nums.length <= 10^5
    -10^4 <= nums[i] <= 10^4
    k is in the range [1, the number of unique elements in the array].
    It is guaranteed that the answer is unique.

Follow up: Your algorithm's time complexity must be better than O(n log n), where n is the array's size.

---

So here we need to track, e.g the 2 most frequent elements. 

Input: nums = [1,1,1,2,2,3], k = 2
Output: [1,2]

1 shows up 3 times
2 shows up twice

So this is clearly something we can do using a counter. I'm pretty sure the ideal solution doesn't involve a counter, but a counter would do the trick here.

"""

class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        c = [(val, count) for val, count in dict(Counter(nums)).items()]
        return [x[0] for x in [*sorted(c, key=lambda x: x[1], reverse=True)][:k]]

sol = Solution()

# print(sol.topKFrequent([1,1,1,2,2,3], 2))  # [1,2]

assert sorted(sol.topKFrequent([1,1,1,2,2,3], 2)) == sorted([1,2])
assert sorted(sol.topKFrequent([1], 1)) == sorted([1])
assert sorted(sol.topKFrequent([1,2,1,2,1,2,3,1,3,2], 2)) == sorted([1,2])
assert sorted(sol.topKFrequent([1,1,1,1,1], 1)) == sorted([1])
assert sorted(sol.topKFrequent([-1,-1,-1,0,0,1], 2)) == sorted([-1,0])
assert sorted(sol.topKFrequent([1,2,3,4,5], 5)) == sorted([1,2,3,4,5])
assert sorted(sol.topKFrequent([4,1,-1,2,-1,2,3], 2)) == sorted([-1,2])
assert sorted(sol.topKFrequent([0], 1)) == sorted([0])
assert sorted(sol.topKFrequent([1,1,2], 2)) == sorted([1,2])
assert sorted(sol.topKFrequent([1,1,1,2,2,3], 3)) == sorted([1,2,3])