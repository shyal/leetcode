"""
URL: https://leetcode.com/problems/find-minimum-operations-to-make-all-elements-divisible-by-three/description/?envType=problem-list-v2&envId=vn57k9wr

3190. Find Minimum Operations to Make All Elements Divisible by Three

You are given an integer array nums. In one operation, you can add or subtract 1
from any element of nums.

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

    def getClosestDivisibleBy3(self, num):
        up, down = num, num
        count = 0
        while True:
            if up % 3 == 0 or down % 3 == 0:
                return count
            count += 1
            up += 1
            down -= 1

    def minimumOperations(self, nums: List[int]) -> int:
        return sum(self.getClosestDivisibleBy3(x) for x in nums)


sol = Solution()

# print(sol.getClosestDivisibleBy3(2))

# print(sol.minimumOperations([1, 2, 3, 4]))  # 3

assert sol.minimumOperations([1, 2, 3, 4]) == 3
assert sol.minimumOperations([3, 6, 9]) == 0
assert sol.minimumOperations([1]) == 1
assert sol.minimumOperations([2]) == 1
assert sol.minimumOperations([3]) == 0
assert sol.minimumOperations([50]) == 1
assert sol.minimumOperations([49]) == 1
assert sol.minimumOperations([48]) == 0
assert sol.minimumOperations([1, 1, 1, 1]) == 4
assert sol.minimumOperations([2, 2, 2]) == 3
assert sol.minimumOperations([1, 2]) == 2
assert sol.minimumOperations([3, 6, 9, 12, 15, 18, 21, 24, 27, 30]) == 0
assert sol.minimumOperations([1, 4, 7, 10]) == 4
assert sol.minimumOperations([2, 5, 8, 11]) == 4
assert sol.minimumOperations([3] * 50) == 0
assert sol.minimumOperations([50] * 50) == 50
assert sol.minimumOperations(list(range(1, 51))) == 34
assert sol.minimumOperations([1, 3, 2, 6, 4, 9]) == 3
assert sol.minimumOperations([44, 45, 46]) == 2