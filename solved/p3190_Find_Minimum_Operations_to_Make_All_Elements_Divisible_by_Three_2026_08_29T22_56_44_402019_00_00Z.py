"""
URL: https://leetcode.com/problems/find-minimum-operations-to-make-all-elements-divisible-by-three/description/?envType=problem-list-v2&envId=vn57k9wr

3190. Find Minimum Operations to Make All Elements Divisible by Three

You are given an integer array nums. In one operation, you can add or subtract 1 from any element of nums.

Return the minimum number of operations to make all elements of nums divisible by 3.

Example 1:

Input: nums = [1,2,3,4]
Output: 3
Explanation:
All array elements can be made divisible by 3 using 3 operations:
- Subtract 1 from 1.
- Add 1 to 2.
- Subtract 1 from 4.

Example 2:

Input: nums = [3,6,9]
Output: 0

Constraints:

    1 <= nums.length <= 50
    1 <= nums[i] <= 50
"""


class Solution:
    def minimumOperations(self, nums: List[int]) -> int:
        res = 0
        for n in nums:
            if n % 3 == 0:
                continue
            elif (n + 1) % 3 == 0:
                res += 1
            else:
                res += 1
        return res


sol = Solution()

print(sol.minimumOperations([1, 2, 3, 4]))  # 3

assert sol.minimumOperations([1, 2, 3, 4]) == 3
assert sol.minimumOperations([3, 6, 9]) == 0

assert sol.minimumOperations([0]) == 0
assert sol.minimumOperations([3] * 50) == 0
assert sol.minimumOperations([1] * 50) == 50
assert sol.minimumOperations([2] * 50) == 50
assert sol.minimumOperations([50] * 50) == 50
assert sol.minimumOperations([49, 50, 48]) == 2
assert sol.minimumOperations([1, 1, 2, 2, 0, 0]) == 4
assert sol.minimumOperations([3, 6, 9, 12, 15, 18, 21, 24, 27, 30]) == 0
assert sol.minimumOperations([1, 4, 7, 10, 13, 16, 19, 22, 25, 28]) == 10
assert sol.minimumOperations([2, 5, 8, 11, 14, 17, 20, 23, 26, 29]) == 10
assert sol.minimumOperations([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]) == 7
assert sol.minimumOperations([50, 49, 48, 47, 46, 45, 44, 43, 42, 41]) == 7
