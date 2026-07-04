"""
URL: https://leetcode.com/problems/contains-duplicate-ii/description/?envType=problem-list-v2&envId=vn57k9wr

219. Contains Duplicate II

Given an integer array nums and an integer k, return true if there are two
distinct indices i and j in the array such that nums[i] == nums[j] and
abs(i - j) <= k.


Example 1:

Input: nums = [1,2,3,1], k = 3
Output: true

Example 2:

Input: nums = [1,0,1,1], k = 1
Output: true

Example 3:

Input: nums = [1,2,3,1,2,3], k = 2
Output: false


Constraints:

    1 <= nums.length <= 10^5
    -10^9 <= nums[i] <= 10^9
    0 <= k <= 10^5
"""

class Solution:
    def containsNearbyDuplicate(self, nums: List[int], k: int) -> bool:
        d = {}
        for i, n in enumerate(nums):
            if n in d:
                if i - d[n] <= k:
                    return True
            d[n] = i

        return False



sol = Solution()

print(sol.containsNearbyDuplicate([1, 2, 3, 1], 3))  # True

assert sol.containsNearbyDuplicate([1, 2, 3, 1], 3) == True
assert sol.containsNearbyDuplicate([1, 0, 1, 1], 1) == True
assert sol.containsNearbyDuplicate([1, 2, 3, 1, 2, 3], 2) == False
assert sol.containsNearbyDuplicate([1], 1) == False
assert sol.containsNearbyDuplicate([1], 0) == False
assert sol.containsNearbyDuplicate([1, 1], 0) == False
assert sol.containsNearbyDuplicate([1, 1], 1) == True
assert sol.containsNearbyDuplicate([0, 0, 0], 0) == False
assert sol.containsNearbyDuplicate([1, 2, 1], 2) == True
assert sol.containsNearbyDuplicate([1, 2, 1], 1) == False
assert sol.containsNearbyDuplicate([1, 2, 3, 1], 2) == False
assert sol.containsNearbyDuplicate([1, 2, 1, 1], 1) == True
assert sol.containsNearbyDuplicate([-1, 5, -1], 2) == True
assert sol.containsNearbyDuplicate([-1000000000, 1000000000, -1000000000], 2) == True
assert sol.containsNearbyDuplicate([-1000000000, 1000000000, -1000000000], 1) == False
assert sol.containsNearbyDuplicate([1, 2, 3, 4, 5], 100000) == False
assert sol.containsNearbyDuplicate([99, 99], 100000) == True
assert sol.containsNearbyDuplicate([4, 4, 4, 4], 1) == True
assert sol.containsNearbyDuplicate(list(range(100000)) + [0], 100000) == True
assert sol.containsNearbyDuplicate(list(range(100000)) + [0], 99999) == False