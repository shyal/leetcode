"""
URL: https://leetcode.com/problems/final-array-state-after-k-multiplication-operations-i/description/?envType=problem-list-v2&envId=vn57k9wr

3264. Final Array State After K Multiplication Operations I

You are given an integer array nums, an integer k, and an integer multiplier.

You need to perform k operations on nums. In each operation:

- Find the minimum value x in nums. If there are multiple occurrences of the minimum value, select the one that appears first.
- Replace the selected minimum value x with x * multiplier.

Return an integer array denoting the final state of nums after performing all k operations.

Example 1:

Input: nums = [2,1,3,5,6], k = 5, multiplier = 2
Output: [8,4,6,5,6]
Explanation:

Operation | Result
-----------------
After operation 1 | [2, 2, 3, 5, 6]
After operation 2 | [4, 2, 3, 5, 6]
After operation 3 | [4, 4, 3, 5, 6]
After operation 4 | [4, 4, 6, 5, 6]
After operation 5 | [8, 4, 6, 5, 6]

Example 2:

Input: nums = [1,2], k = 3, multiplier = 4
Output: [16,8]
Explanation:

Operation | Result
-----------------
After operation 1 | [4, 2]
After operation 2 | [4, 8]
After operation 3 | [16, 8]

Constraints:

    1 <= nums.length <= 100
    1 <= nums[i] <= 100
    1 <= k <= 10
    1 <= multiplier <= 5

LEETCODE: Accepted (11 ms, 19.6 MB)
"""


class Solution:
    def getFinalState(self, nums: List[int], k: int, multiplier: int) -> List[int]:
        h = [[x, i] for i, x in enumerate(nums)]
        heapify(h)
        for _ in range(k):
            _min, i = heappop(h)
            heappush(h, [_min * multiplier, i])
        h.sort(key=lambda x: x[1])
        return [x[0] for x in h]


sol = Solution()

print(sol.getFinalState([2, 1, 3, 5, 6], 5, 2))  # [8,4,6,5,6]

assert sol.getFinalState([2, 1, 3, 5, 6], 5, 2) == [8, 4, 6, 5, 6]
assert sol.getFinalState([1, 2], 3, 4) == [16, 8]

assert sol.getFinalState([1], 1, 2) == [2]
assert sol.getFinalState([1], 10, 2) == [1024]
assert sol.getFinalState([5, 5, 5, 5], 4, 3) == [15, 15, 15, 15]
assert sol.getFinalState([10, 9, 8, 7, 6, 5, 4, 3, 2, 1], 10, 2) == [
    10,
    9,
    8,
    7,
    12,
    10,
    8,
    12,
    8,
    8,
]
assert sol.getFinalState([1, 1, 1, 1, 1], 5, 1) == [1, 1, 1, 1, 1]
assert sol.getFinalState([100] * 100, 10, 5) == [
    500,
    500,
    500,
    500,
    500,
    500,
    500,
    500,
    500,
    500,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
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
assert sol.getFinalState([1, 2, 3, 4, 5], 0, 3) == [1, 2, 3, 4, 5]
assert sol.getFinalState([3, 3, 2, 2, 1, 1], 6, 2) == [3, 3, 4, 4, 4, 4]
assert sol.getFinalState([1, 2, 3, 4, 5], 10, 1) == [1, 2, 3, 4, 5]
assert sol.getFinalState([2, 2, 2, 2, 2], 5, 0) == [0, 2, 2, 2, 2]
assert sol.getFinalState([1, 2, 3, 4, 5], 10, 5) == [125, 50, 75, 100, 25]
assert sol.getFinalState([100] * 100, 1, 1) == [
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
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
