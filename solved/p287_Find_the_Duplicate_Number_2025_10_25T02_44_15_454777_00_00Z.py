"""
URL: https://leetcode.com/problems/find-the-duplicate-number/description/

287. Find the Duplicate Number

Given an array of integers nums containing n + 1 integers where each integer is in the range [1, n] inclusive.

There is exactly one duplicate number in nums, return this duplicate number.

You must solve the problem without modifying the array nums and uses only constant extra space.


Example 1:

Input: nums = [1,3,4,2,2]
Output: 2

Example 2:

Input: nums = [3,1,3,4,2]
Output: 3


Constraints:

    1 <= n <= 105
    nums.length == n + 1
    1 <= nums[i] <= n
    All the integers in nums appear only once except for precisely one integer which appears two or more times.


---

Ok this question is quite.. "interesting" (feels contrived, but anyway). The idea here
is that we can use cycle detection.. because we can use the values as indices.

nums =  [1,3,4,2,2]
indices: 0,1,2,3,4

1 -> 3 -> 2 -> 4
          |   |
          ^ <-v

So value 1 we jump to the value at index 1, which is 3
at 3 we jump at value at index 3 which is 2
etc.

We notice a cycle at values `2`.

The second example isn't as simple:

nums = [3,1,3,4,2]
indices 0,1,2,3,4

3 -> 4 -> 2 -> 3
     |         |
     ^ <------ v


Ok we can see the cycle here:


def findDuplicate(self, nums):
    it = 0
    for _ in range(len(nums) + 2):
        it = nums[it]
        # print(f"{it} -> ", end="")
    # print("")
    # 1 -> 3 -> 2 -> 4 -> 2 -> 4 ->

So that's our slow pointer.

[1, 3, 4, 2, 2]
1 -> 3 -> 2 -> 4 ->
slow and fast are, 4, 4

[3, 1, 3, 4, 2]
3 -> 4 -> 2 ->
slow and fast are, 2, 2

OK i give up. I'm not sure how to init the slow and fast pointers.
I try to draw what i think is supposed to happen, but somehow it doesn't.
"""


class Solution(object):

    def findDuplicate(self, nums):
        slow = 0
        fast = 0
        # print(nums)
        for _ in range(len(nums) * 2):
            slow = nums[slow]
            fast = nums[nums[fast]]
            # print(f"{slow} -> ", end="")
            # if slow == fast:
            # print("")
            # print(f"slow and fast are, {slow}, {fast}")
            # break


sol = Solution()
# sol.findDuplicate([1, 3, 4, 2, 2])
sol.findDuplicate([3, 1, 3, 4, 2])

# assert sol.findDuplicate([1, 3, 4, 2, 2]) == 2
# assert sol.findDuplicate([3, 1, 3, 4, 2]) == 3
# assert sol.findDuplicate([1, 1]) == 1
# assert sol.findDuplicate([1, 2, 2, 3]) == 2
# assert sol.findDuplicate([3, 3, 3, 3]) == 3
# assert sol.findDuplicate([1, 2, 3, 4, 4]) == 4
# assert sol.findDuplicate([4, 1, 2, 3, 4]) == 4
# assert sol.findDuplicate([1, 2, 3, 1]) == 1
# assert sol.findDuplicate([2, 2, 2, 2, 2]) == 2
# assert sol.findDuplicate([1, 1, 1]) == 1
# assert sol.findDuplicate([2, 1, 2]) == 2
# assert sol.findDuplicate([4, 3, 1, 4, 2]) == 4
