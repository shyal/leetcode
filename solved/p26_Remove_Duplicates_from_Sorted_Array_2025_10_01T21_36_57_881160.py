"""
URL: https://leetcode.com/problems/remove-duplicates-from-sorted-array/description/

26. Remove Duplicates from Sorted Array

Given an integer array nums sorted in non-decreasing order, remove the duplicates in-place such that each unique element appears only once. The relative order of the elements should be kept the same. Then return the number of unique elements in nums.

Consider the number of unique elements of nums to be k, to get accepted, you need to do the following things:

        Change the array nums such that the first k elements of nums contain the unique elements in the order they were present in nums initially. The remaining elements of nums are not important as well as the size of nums.
        Return k.

Custom Judge:

The judge will test your solution with the following code:

int[] nums = [...]; // Input array
int[] expectedNums = [...]; // The expected answer with correct length

int k = removeDuplicates(nums); // Calls your implementation

assert k == expectedNums.length;
for (int i = 0; i < k; i++) {
    assert nums[i] == expectedNums[i];
}

If all assertions pass, then your solution will be accepted.


Example 1:

Input: nums = [1,1,2]
Output: 2, nums = [1,2,_]
Explanation: Your function should return k = 2, with the first two elements of nums being 1 and 2 respectively.
It does not matter what you leave beyond the returned k (hence they are underscores).

Example 2:

Input: nums = [0,0,1,1,1,2,2,3,3,4]
Output: 5, nums = [0,1,2,3,4,_,_,_,_,_]
Explanation: Your function should return k = 5, with the first five elements of nums being 0, 1, 2, 3, and 4 respectively.
It does not matter what you leave beyond the returned k (hence they are underscores).


Constraints:

        1 <= nums.length <= 3 * 104
        -100 <= nums[i] <= 100
        nums is sorted in non-decreasing order.

-----------

 w  r
[0, 1, 1, 1, 2, 2, 3, 3, 4]
    x.    x. x     x.    x

"""


class Solution:
    def bf0(self, nums):
        s = set(nums)
        nums[: len(s)] = [*sorted(list(s))]
        return len(s)

    def removeDuplicates(self, nums: List[int]) -> int:
        write = 1
        for i in range(1, len(nums)):
            if nums[i] != nums[i - 1]:
                nums[write] = nums[i]
                write += 1
        return write


sol = Solution()

nums = [1, 1, 2]
k = sol.removeDuplicates(nums)
assert k == 2
assert nums[:k] == [1, 2]

nums = [0, 0, 1, 1, 1, 2, 2, 3, 3, 4]
k = sol.removeDuplicates(nums)
assert k == 5
assert nums[:k] == [0, 1, 2, 3, 4]

nums = [5]
k = sol.removeDuplicates(nums)
assert k == 1
assert nums[:k] == [5]

nums = [1, 2, 3, 4, 5]
k = sol.removeDuplicates(nums)
assert k == 5
assert nums[:k] == [1, 2, 3, 4, 5]

nums = [7, 7, 7, 7]
k = sol.removeDuplicates(nums)
assert k == 1
assert nums[:k] == [7]

nums = [-1, -1]
k = sol.removeDuplicates(nums)
assert k == 1
assert nums[:k] == [-1]

nums = [-100, 100]
k = sol.removeDuplicates(nums)
assert k == 2
assert nums[:k] == [-100, 100]

nums = [-100, -100, -50, 0, 0, 50, 100, 100]
k = sol.removeDuplicates(nums)
assert k == 5
assert nums[:k] == [-100, -50, 0, 50, 100]

nums = [1, 2, 2, 3]
k = sol.removeDuplicates(nums)
assert k == 3
assert nums[:k] == [1, 2, 3]
