"""
URL: https://leetcode.com/problems/find-the-xor-of-numbers-which-appear-twice/description/?envType=problem-list-v2&envId=v0n2n1sc

3158. Find the XOR of Numbers Which Appear Twice

You are given an array nums, where each number in the array appears either once or twice.

Return the bitwise XOR of all the numbers that appear twice in the array, or 0 if no number appears twice.


Example 1:

Input: nums = [1,2,1,3]

Output: 1

Explanation:

The only number that appears twice in nums is 1.

Example 2:

Input: nums = [1,2,3]

Output: 0

Explanation:

No number appears twice in nums.

Example 3:

Input: nums = [1,2,2,1]

Output: 3

Explanation:

Numbers 1 and 2 appeared twice. 1 XOR 2 == 3.


Constraints:

        1 <= nums.length <= 50
        1 <= nums[i] <= 50
        Each number in nums appears either once or twice.


---

This is a bit manipulation problem, so let's think whether we can use
a property of xor to solve it.

We know that taking the xor of the same number yields 0

[1,2,1,3]

So if we take the xor of the entire array, we'll end up with the bitwise xor
of 2 and 3, which is `1`, and the bitwise or of the entire array is `3`.

Nope. Can't think of a clever trick we can use. So i'll use a Counter instead.

"""


class Solution:
    def duplicateNumbersXOR(self, nums: List[int]) -> int:
        return reduce(
            xor,
            map(lambda x: x[0], filter(lambda x: x[1] == 2, Counter(nums).items())),
            0,
        )


sol = Solution()
assert sol.duplicateNumbersXOR(nums=[1, 2, 1, 3]) == 1
assert sol.duplicateNumbersXOR(nums=[1, 2, 3]) == 0
assert sol.duplicateNumbersXOR(nums=[1, 2, 2, 1]) == 3
