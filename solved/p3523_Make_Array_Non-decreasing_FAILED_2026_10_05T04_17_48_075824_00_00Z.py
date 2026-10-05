"""
URL: https://leetcode.com/problems/make-array-non-decreasing/description/?envType=problem-list-v2&envId=vn57k9wr

3523. Make Array Non-decreasing

You are given an integer array nums. In one operation, you can select a subarray and replace it with a single element equal to its maximum value.

Return the maximum possible size of the array after performing zero or more operations such that the resulting array is non-decreasing.

Example 1:

Input: nums = [4,2,5,3,5]
Output: 3
Explanation:
One way to achieve the maximum size is:
1) Replace subarray nums[1..2] = [2, 5] with 5 -> [4, 5, 3, 5].
2) Replace subarray nums[2..3] = [3, 5] with 5 -> [4, 5, 5].
The final array [4, 5, 5] is non-decreasing with size 3.

Example 2:

Input: nums = [1,2,3]
Output: 3
Explanation:
No operation is needed as the array [1,2,3] is already non-decreasing.

Constraints:

    1 <= nums.length <= 2 * 10^5
    1 <= nums[i] <= 2 * 10^5
---
[1, 3, 2, 4, 3, 5]
[1, 3, 2, 4, 3, 5]









brute force was terrible idea:

def maximumPossibleSize(nums: [int]) -> int
    def is_increasing()
        for (a, b) in zip(nums, nums[1:])
            if a > b
                return False
        True
    while not is_increasing()
        _min = min(nums)
        min_index = nums.index(_min)
        if min_index < len(nums) - 1
            pick = max(nums[min_index:min_index + 2])
            nums[min_index:min_index+2] = [pick]
        else
            pick = max(nums[min_index-1:min_index + 1])
            nums[min_index-1:min_index+1] = [pick]
    print(nums)
    len nums
"""


# mu 0.7
# def maximumPossibleSize(nums: [int]) -> int
#     def is_increasing()
#         for (a, b) in zip(nums, nums[1:])
#             if a > b
#                 return False
#         True
#     heapify(nums)
#     h = nums
#     while not is_increasing() and len h >= 3
#         a, b, c = heappop(h), heappop(h), heappop(h)
#         x = [a, b, c]
#         heappush(h, b)
#         heappush(h, c)
#         print(nums)
#     len h

class Solution:
    def maximumPossibleSize(self, nums: list[int]) -> int:
        def is_increasing():
            for (a, b) in zip(nums, nums[1:]):
                if a > b:
                    return False
            return True
        heapify(nums)
        h = nums
        while not is_increasing() and len(h) >= 3:
            a, b, c = heappop(h), heappop(h), heappop(h)
            x = [a, b, c]
            heappush(h, b)
            heappush(h, c)
            print(nums)
        return len(h)


sol = Solution()
assert sol.maximumPossibleSize([1, 3, 2, 4, 3, 5]) == 4
print(sol.maximumPossibleSize([4, 2, 5, 3, 5]))
assert sol.maximumPossibleSize([4, 2, 5, 3, 5]) == 3
assert sol.maximumPossibleSize([1, 2, 3]) == 3
assert sol.maximumPossibleSize([1]) == 1
assert sol.maximumPossibleSize([2, 1]) == 1
assert sol.maximumPossibleSize(list(range(1, 11))) == 10
assert sol.maximumPossibleSize(list(range(10, 0, -1))) == 1
assert sol.maximumPossibleSize([5] * 10) == 10
assert sol.maximumPossibleSize([5, 1, 5, 1, 5, 1]) == 3
assert sol.maximumPossibleSize([-3, -2, -1]) == 3
assert sol.maximumPossibleSize([0, -1, -2, -3]) == 1
assert sol.maximumPossibleSize([200000, 1, 200000, 1, 200000]) == 3
assert sol.maximumPossibleSize(list(range(1000, 0, -1))) == 1


# FAILED: walked away after 25m 15s; no working solution.
# Judge the move the defect is in as struggled, not clean. A move the code never reached gets no verdict.
