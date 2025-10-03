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

    Subtract 1 from 1.
    Add 1 to 2.
    Subtract 1 from 4.

Example 2:

Input: nums = [3,6,9]

Output: 0


Constraints:

    1 <= nums.length <= 50
    1 <= nums[i] <= 50

---

Ok first let's figure how to compute the number of ops to make a number divisible by 3.

0 % 3 == 0
1 % 3 == 1
2 % 3 == 2
3 % 3 == 0
4 % 3 == 1
5 % 3 == 2
6 % 3 == 0
7 % 3 == 1
8 % 3 == 2
9 % 3 == 0

Looks like we're always just 1 operation away from being divisible by 3, IF we're not
already divisible by 3.

"""


class Solution:
    def minimumOperations(self, nums: List[int]) -> int:
        return sum(int(bool(x % 3)) for x in nums)


sol = Solution()

assert sol.minimumOperations([1, 2, 3, 4]) == 3
assert sol.minimumOperations([3, 6, 9]) == 0
