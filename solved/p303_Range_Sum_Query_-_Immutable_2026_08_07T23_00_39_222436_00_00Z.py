"""
URL: https://leetcode.com/problems/range-sum-query-immutable/description/?envType=problem-list-v2&envId=vn57k9wr

303. Range Sum Query - Immutable

Given an integer array nums, handle multiple queries of the following type:

    1. Calculate the sum of the elements of nums between indices left and right
       inclusive where left <= right.

Implement the NumArray class:

    - NumArray(int[] nums) Initializes the object with the integer array nums.
    - int sumRange(int left, int right) Returns the sum of the elements of nums
      between indices left and right inclusive
      (i.e. nums[left] + nums[left + 1] + ... + nums[right]).


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

    1 <= nums.length <= 10^4
    -10^5 <= nums[i] <= 10^5
    0 <= left <= right < nums.length
    At most 10^4 calls will be made to sumRange.
"""

class NumArray:
    def __init__(self, nums: List[int]):
        self.sums = [*accumulate(nums)]

    def sumRange(self, left: int, right: int) -> int:
        return self.sums[right] - (self.sums[left-1] if left > 0 else 0)

obj = NumArray([-2, 0, 3, -5, 2, -1])

# print(obj.sumRange(0, 2))  # 1

assert obj.sumRange(0, 2) == 1
assert obj.sumRange(2, 5) == -1
assert obj.sumRange(0, 5) == -3

assert obj.sumRange(0, 0) == -2
assert obj.sumRange(5, 5) == -1
assert obj.sumRange(3, 3) == -5
assert obj.sumRange(1, 1) == 0
assert obj.sumRange(1, 4) == 0
# assert obj.sumRange(3, 4) == 2
assert obj.sumRange(4, 5) == 1
assert obj.sumRange(2, 3) == -2
assert obj.sumRange(1, 5) == -1

single = NumArray([5])
assert single.sumRange(0, 0) == 5

single_neg = NumArray([-100000])
assert single_neg.sumRange(0, 0) == -100000

zeros = NumArray([0, 0, 0])
assert zeros.sumRange(0, 2) == 0
assert zeros.sumRange(1, 1) == 0
assert zeros.sumRange(0, 1) == 0

extremes = NumArray([100000, -100000, 100000])
assert extremes.sumRange(0, 2) == 100000
assert extremes.sumRange(0, 1) == 0
assert extremes.sumRange(1, 2) == 0
assert extremes.sumRange(2, 2) == 100000

positives = NumArray([1, 2, 3, 4, 5])
assert positives.sumRange(0, 4) == 15
assert positives.sumRange(1, 3) == 9
assert positives.sumRange(4, 4) == 5
assert positives.sumRange(0, 0) == 1

negatives = NumArray([-1, -2, -3])
assert negatives.sumRange(0, 2) == -6
assert negatives.sumRange(0, 1) == -3
assert negatives.sumRange(2, 2) == -3

alternating = NumArray([10, -10, 10, -10, 10])
assert alternating.sumRange(0, 4) == 10
assert alternating.sumRange(0, 3) == 0
assert alternating.sumRange(1, 4) == 0
assert alternating.sumRange(2, 2) == 10

# print("All assertions passed")