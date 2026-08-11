"""
URL: https://leetcode.com/problems/sort-array-by-parity-ii/description/?envType=problem-list-v2&envId=vn57k9wr

922. Sort Array By Parity II

Given an array of integers nums, half of the integers in nums are odd, and the
other half are even.

Sort the array so that whenever nums[i] is odd, i is odd, and whenever nums[i]
is even, i is even.

Return any answer array that satisfies this condition.


Example 1:

Input: nums = [4,2,5,7]
Output: [4,5,2,7]
Explanation: [4,7,2,5], [2,5,4,7], [2,7,4,5] would also have been accepted.

Example 2:

Input: nums = [2,3]
Output: [2,3]


Constraints:

    2 <= nums.length <= 2 * 10^4
    nums.length is even.
    Half of the integers in nums are even.
    0 <= nums[i] <= 1000


Follow Up: Could you solve it in-place?
"""


class Solution:
    def sortArrayByParityII(self, nums: List[int]) -> List[int]:
        nums.sort(key=lambda x: x % 2 == 0)
        return [*chain.from_iterable(zip(nums[len(nums)//2:], nums[:len(nums)//2]))]


sol = Solution()

assert sol.sortArrayByParityII([4, 2, 5, 7]) == [4, 5, 2, 7]
assert sol.sortArrayByParityII([2, 3]) == [2, 3]
assert sol.sortArrayByParityII([3, 2]) == [2, 3]
assert sol.sortArrayByParityII([1, 2]) == [2, 1]
assert sol.sortArrayByParityII([0, 1]) == [0, 1]
assert sol.sortArrayByParityII([1, 0]) == [0, 1]
assert sol.sortArrayByParityII([0, 0, 1, 1]) == [0, 1, 0, 1]
assert sol.sortArrayByParityII([7, 7, 2, 2]) == [2, 7, 2, 7]
assert sol.sortArrayByParityII([1000, 999, 0, 1]) == [1000, 999, 0, 1]
assert sol.sortArrayByParityII([5, 4, 3, 2, 1, 0]) == [4, 5, 2, 3, 0, 1]
assert sol.sortArrayByParityII([2, 1, 4, 3]) == [2, 1, 4, 3]
assert sol.sortArrayByParityII([8, 1, 6, 3, 4, 5, 2, 7]) == [8, 1, 6, 3, 4, 5, 2, 7]
assert sol.sortArrayByParityII(list(range(100))) == list(range(100))

big = sol.sortArrayByParityII(list(range(99, -1, -1)))
assert all(big[i] % 2 == i % 2 for i in range(100))
assert sorted(big) == list(range(100))
assert big[:4] == [98, 99, 96, 97]