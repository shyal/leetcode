"""
URL: https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/description/?envType=problem-list-v2&envId=vn57k9wr

167. Two Sum II - Input Array Is Sorted

Given a 1-indexed array of integers numbers that is already sorted in
non-decreasing order, find two numbers such that they add up to a specific
target number. Let these two numbers be numbers[index1] and numbers[index2]
where 1 <= index1 < index2 <= numbers.length.

Return the indices of the two numbers index1 and index2, each incremented
by one, as an integer array [index1, index2] of length 2.

The tests are generated such that there is exactly one solution. You may
not use the same element twice.

Your solution must use only constant extra space.


Example 1:

Input: numbers = [2,7,11,15], target = 9
Output: [1,2]
Explanation: The sum of 2 and 7 is 9. Therefore, index1 = 1, index2 = 2. We return [1, 2].

Example 2:

Input: numbers = [2,3,4], target = 6
Output: [1,3]
Explanation: The sum of 2 and 4 is 6. Therefore index1 = 1, index2 = 3. We return [1, 3].

Example 3:

Input: numbers = [-1,0], target = -1
Output: [1,2]
Explanation: The sum of -1 and 0 is -1. Therefore index1 = 1, index2 = 2. We return [1, 2].


Constraints:

    2 <= numbers.length <= 3 * 10^4
    -1000 <= numbers[i] <= 1000
    numbers is sorted in non-decreasing order.
    -1000 <= target <= 1000
    The tests are generated such that there is exactly one solution.
"""

class Solution:
    def twoSum(self, numbers: List[int], target: int) -> List[int]:
        i = 0
        j = len(numbers) -1
        while i != j:
            res = numbers[i] + numbers[j]
            if res == target:
                return [i + 1, j + 1]
            elif res < target:
                i += 1
            else:
                j -= 1
        return []


sol = Solution()

# print(sol.twoSum([2, 7, 11, 15], 9))  # [1, 2]

assert sol.twoSum([2, 7, 11, 15], 9) == [1, 2]
assert sol.twoSum([2, 3, 4], 6) == [1, 3]
assert sol.twoSum([-1, 0], -1) == [1, 2]
assert sol.twoSum([1, 2], 3) == [1, 2]
assert sol.twoSum([3, 3], 6) == [1, 2]
assert sol.twoSum([0, 0, 3, 4], 0) == [1, 2]
assert sol.twoSum([1, 2, 3, 4, 5], 6) == [1, 5]
assert sol.twoSum([1, 3, 4, 7, 11], 7) == [2, 3]
assert sol.twoSum([2, 7, 11, 15], 26) == [3, 4]
assert sol.twoSum([-5, -3, -1], -8) == [1, 2]
assert sol.twoSum([-2, -1, 1, 2], 0) == [1, 4]
assert sol.twoSum([1, 2, 2, 4], 4) == [2, 3]
assert sol.twoSum([5, 25, 75], 100) == [2, 3]
assert sol.twoSum([-10, -8, -2, 1, 2, 5, 6], 0) == [3, 5]
assert sol.twoSum([-1000, 1000], 0) == [1, 2]
assert sol.twoSum([-3, -1, 0, 2], -4) == [1, 2]
assert sol.twoSum(list(range(1, 101)) + [1000], 199) == [99, 100]

print("All tests passed!")