"""
URL: https://leetcode.com/problems/sort-array-by-parity-ii/description/?envType=problem-list-v2&envId=vn57k9wr

922. Sort Array By Parity II

Given an array of integers nums, half of the integers in nums are odd, and the other half are even.

Sort the array so that whenever nums[i] is odd, i is odd, and whenever nums[i] is even, i is even.

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
"""


class Solution:
    def sortArrayByParityII(self, nums: List[int]) -> List[int]:
        G = [[k, list(v)] for k, v in groupby(nums, key=lambda x: x % 2 == 0)]
        oe = defaultdict(list)
        for k, v in G:
            oe[k].extend(v)
        res = []
        for i in range(len(nums)):
            res.append(oe[i % 2 == 0].pop())
        return res


sol = Solution()
print(sol.sortArrayByParityII([4, 1, 2, 1]))
# print(sol.sortArrayByParityII([4, 2, 5, 7]))  # [4,5,2,7]

# assert sol.sortArrayByParityII([4,2,5,7]) == [4,5,2,7]
# assert sol.sortArrayByParityII([2,3]) == [2,3]
# assert sol.sortArrayByParityII([1,0]) == [0,1]
# assert sol.sortArrayByParityII([0,1]) == [0,1]
# assert sol.sortArrayByParityII([1,0,3,2]) == [0,1,2,3]
# assert sol.sortArrayByParityII([3,4,1,2]) == [4,3,2,1]
# assert sol.sortArrayByParityII([111,888,111,888]) == [888,111,888,111]
# assert sol.sortArrayByParityII([0,1,2,3,4,5]) == [0,1,2,3,4,5]
# assert sol.sortArrayByParityII([1,2,3,4,5,6]) == [2,1,4,3,6,5]
