"""
URL: https://leetcode.com/problems/rearrange-array-elements-by-sign/description/?envType=problem-list-v2&envId=vn57k9wr

2149. Rearrange Array Elements by Sign

You are given a 0-indexed integer array nums of even length consisting of an equal number of positive and negative integers.

You should return the array of nums such that the array follows the given conditions:

1. Every consecutive pair of integers have opposite signs.
2. For all integers with the same sign, the order in which they were present in nums is preserved.
3. The rearranged array begins with a positive integer.

Return the modified array after rearranging the elements to satisfy the aforementioned conditions.

Example 1:

Input: nums = [3,1,-2,-5,2,-4]
Output: [3,-2,1,-5,2,-4]
Explanation:
The positive integers in nums are [3,1,2]. The negative integers are [-2,-5,-4].
The only possible way to rearrange them such that they satisfy all conditions is [3,-2,1,-5,2,-4].
Other ways such as [1,-2,2,-5,3,-4], [3,1,2,-2,-5,-4], [-2,3,-5,1,-4,2] are incorrect because they do not satisfy one or more conditions.

Example 2:

Input: nums = [-1,1]
Output: [1,-1]
Explanation:
1 is the only positive integer and -1 the only negative integer in nums.
So nums is rearranged to [1,-1].

Constraints:

    2 <= nums.length <= 2 * 10^5
    nums.length is even
    1 <= |nums[i]| <= 10^5
    nums consists of equal number of positive and negative integers.
"""


class Solution:
    def rearrangeArray(self, nums: List[int]) -> List[int]:
        pos = [x for x in nums if x >= 0]
        neg = [x for x in nums if x < 0]
        return [*chain.from_iterable(zip(pos, neg))]


sol = Solution()

print(sol.rearrangeArray([3, 1, -2, -5, 2, -4]))  # [3,-2,1,-5,2,-4]

assert sol.rearrangeArray([3, 1, -2, -5, 2, -4]) == [3, -2, 1, -5, 2, -4]
assert sol.rearrangeArray([-1, 1]) == [1, -1]

assert sol.rearrangeArray([1, -1, 2, -2, 3, -3, 4, -4, 5, -5]) == [
    1,
    -1,
    2,
    -2,
    3,
    -3,
    4,
    -4,
    5,
    -5,
]
assert sol.rearrangeArray([-100000, 100000, -99999, 99999]) == [
    100000,
    -100000,
    99999,
    -99999,
]
assert sol.rearrangeArray([10, -10, 10, -10, 10, -10, 10, -10]) == [
    10,
    -10,
    10,
    -10,
    10,
    -10,
    10,
    -10,
]
assert sol.rearrangeArray([5, 5, 5, 5, -5, -5, -5, -5]) == [5, -5, 5, -5, 5, -5, 5, -5]
assert sol.rearrangeArray([100000, -100000, 99999, -99999, 1, -1]) == [
    100000,
    -100000,
    99999,
    -99999,
    1,
    -1,
]
assert sol.rearrangeArray([-1, 2, -3, 4, -5, 6, -7, 8]) == [2, -1, 4, -3, 6, -5, 8, -7]
assert sol.rearrangeArray([1, -1, 1, -1, 1, -1, 1, -1]) == [1, -1, 1, -1, 1, -1, 1, -1]
assert sol.rearrangeArray([-1, 1, -2, 2, -3, 3, -4, 4]) == [1, -1, 2, -2, 3, -3, 4, -4]
assert sol.rearrangeArray([1, -1, 2, -2, 3, -3, 4, -4, 5, -5, 6, -6]) == [
    1,
    -1,
    2,
    -2,
    3,
    -3,
    4,
    -4,
    5,
    -5,
    6,
    -6,
]
assert sol.rearrangeArray([1, -1, 1, -1, 2, -2, 2, -2]) == [1, -1, 1, -1, 2, -2, 2, -2]
assert sol.rearrangeArray([10, -10]) == [10, -10]
