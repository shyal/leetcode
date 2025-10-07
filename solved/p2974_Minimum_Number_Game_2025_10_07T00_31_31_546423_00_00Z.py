"""
URL: https://leetcode.com/problems/minimum-number-game/description/

2974. Minimum Number Game

You are given a 0-indexed integer array nums of even length consisting of distinct positive integers.

Alice and Bob are playing a game using the array nums, with an initially empty array arr.

They take turns performing operations, with Alice going first.

In each operation:

    Alice chooses the smallest element in nums and removes it.

    Bob chooses the smallest element in the remaining elements of nums and removes it.

    Bob appends his chosen element to arr.

    Alice appends her chosen element to arr.

The game continues until nums becomes empty.

Return the array arr after the game ends.


Example 1:

Input: nums = [5,4,2,3]
Output: [3,2,5,4]
Explanation:
Round 1: nums = [5,4,2,3]
 - Alice removes 2, nums = [5,4,3]
 - Bob removes 3, nums = [5,4]
 - Bob appends 3 to arr = [3]
 - Alice appends 2 to arr = [3,2]
Round 2: nums = [5,4]
 - Alice removes 4, nums = [5]
 - Bob removes 5, nums = []
 - Bob appends 5 to arr = [3,2,5]
 - Alice appends 4 to arr = [3,2,5,4]

Example 2:

Input: nums = [2,5]
Output: [5,2]
Explanation:
Round 1: nums = [2,5]
 - Alice removes 2, nums = [5]
 - Bob removes 5, nums = []
 - Bob appends 5 to arr = [5]
 - Alice appends 2 to arr = [5,2]


Constraints:

    2 <= nums.length <= 100
    nums.length % 2 == 0
    1 <= nums[i] <= 100
    All elements in nums are distinct.
"""


class Solution:
    def numberGame(self, nums: List[int]) -> List[int]:
        arr = []
        while nums:
            alice_min = min(nums)
            nums.remove(alice_min)
            bob_min = min(nums)
            nums.remove(bob_min)
            arr.extend([bob_min, alice_min])
        return arr


sol = Solution()

assert sol.numberGame([5, 4, 2, 3]) == [3, 2, 5, 4]
assert sol.numberGame([2, 5]) == [5, 2]
assert sol.numberGame([1, 2]) == [2, 1]
assert sol.numberGame([1, 3, 2, 4]) == [2, 1, 4, 3]
assert sol.numberGame([6, 1, 3, 2, 4, 5]) == [2, 1, 4, 3, 6, 5]
assert sol.numberGame([99, 100]) == [100, 99]
assert sol.numberGame([10, 20, 30, 40]) == [20, 10, 40, 30]
assert sol.numberGame([100, 1, 50, 2]) == [2, 1, 100, 50]
assert sol.numberGame([4, 3, 2, 1]) == [2, 1, 4, 3]
assert sol.numberGame([7, 8, 9, 10, 11, 12]) == [8, 7, 10, 9, 12, 11]
