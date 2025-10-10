"""
URL: https://leetcode.com/problems/range-sum-query-immutable/description/

303. Range Sum Query - Immutable

Given an integer array nums, handle multiple queries of the following type:

        Calculate the sum of the elements of nums between indices left and right inclusive where left <= right.

Implement the NumArray class:

        NumArray(int[] nums) Initializes the object with the integer array nums.
        int sumRange(int left, int right) Returns the sum of the elements of nums between indices left and right inclusive (i.e. nums[left] + nums[left + 1] + ... + nums[right]).


Example 1:

Input
["NumArray", "sumRange", "sumRange", "sumRange"]
[[[-2, 0, 3, -5, 2, -1]], [0, 2], [2, 5], [0, 5]]
Output
[null, 1, -1, -3]

Explanation
NumArray numArray = new NumArray([-2, 0, 3, -5, 2, -1]);
numArray.sumRange(0, 2); // return (-2) + 0 + 3 = 1
numArray.sumRange(2, 5); // return 3 + (-5) + 2 + (-1) = -1
numArray.sumRange(0, 5); // return (-2) + 0 + 3 + (-5) + 2 + (-1) = -3


Constraints:

        1 <= nums.length <= 104
        -105 <= nums[i] <= 105
        0 <= left <= right < nums.length
        At most 104 calls will be made to sumRange.

---

Ok this one felt obvious, simply accumulate values, using itertools
then subtract the [0 -> left -1] from [0 to right].
even figured out a neat trick to avoid bounds checking.

"""


class NumArray:

    def __init__(self, nums: List[int]):
        self.prefix = [*accumulate(nums), 0]

    def sumRange(self, left: int, right: int) -> int:
        return self.prefix[right] - self.prefix[left - 1]


numArray = NumArray([-2, 0, 3, -5, 2, -1])
assert numArray.sumRange(0, 2) == 1
assert numArray.sumRange(2, 5) == -1
assert numArray.sumRange(0, 5) == -3
numArray = NumArray([5])
assert numArray.sumRange(0, 0) == 5
numArray = NumArray([0, 0, 0])
assert numArray.sumRange(0, 2) == 0
assert numArray.sumRange(1, 1) == 0
numArray = NumArray([-1, -2, -3])
assert numArray.sumRange(0, 2) == -6
assert numArray.sumRange(1, 2) == -5
numArray = NumArray([1, 2, 3, 4])
assert numArray.sumRange(1, 1) == 2
assert numArray.sumRange(3, 3) == 4
numArray = NumArray([1, 2, 3])
assert numArray.sumRange(0, 2) == 6
numArray = NumArray([1, -1, 1])
assert numArray.sumRange(0, 1) == 0
numArray = NumArray([-100000])
assert numArray.sumRange(0, 0) == -100000
numArray = NumArray([100000])
assert numArray.sumRange(0, 0) == 100000
