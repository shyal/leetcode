"""
https://leetcode.com/problems/can-place-flowers/description

605. Can Place Flowers
Easy
You have a long flowerbed in which some of the plots are planted, and some are not. However, flowers cannot be planted in adjacent plots.

Given an integer array flowerbed containing 0's and 1's, where 0 means empty and 1 means not empty, and an integer n, return true if n new flowers can be planted in the flowerbed without violating the no-adjacent-flowers rule and false otherwise.

Example 1:

Input: flowerbed = [1,0,0,0,1], n = 1
Output: true
Example 2:

Input: flowerbed = [1,0,0,0,1], n = 2
Output: false

Constraints:

1 <= flowerbed.length <= 2 * 104
flowerbed[i] is 0 or 1.
There are no two adjacent flowers in flowerbed.
0 <= n <= flowerbed.length
"""


class Solution:
    def canPlaceFlowers(self, flowerbed: List[int], n: int) -> bool:
        added = 0
        for i in range(len(flowerbed)):
            left_slot_free = i == 0 or flowerbed[i - 1] == 0
            right_slot_free = i == len(flowerbed) - 1 or flowerbed[i + 1] == 0
            if (left_slot_free and right_slot_free) and flowerbed[i] == 0:
                if added < n:
                    flowerbed[i] = 1
                    added += 1
        return added == n


sol = Solution()
assert sol.canPlaceFlowers(flowerbed=[1, 0, 0, 0, 1], n=1) == True
assert sol.canPlaceFlowers(flowerbed=[1, 0, 0, 0, 1], n=2) == False
assert sol.canPlaceFlowers(flowerbed=[1, 0, 0, 0, 0, 0, 0, 1], n=2) == True
assert sol.canPlaceFlowers(flowerbed=[1, 0, 0, 1, 0, 0, 0, 1], n=1) == True
assert sol.canPlaceFlowers(flowerbed=[0, 1, 0, 1, 0, 0, 0, 1, 0, 1], n=1) == True

# Edge case: Single empty plot, n=1
assert sol.canPlaceFlowers(flowerbed=[0], n=1) == True

# Edge case: Single empty plot, n=0
assert sol.canPlaceFlowers(flowerbed=[0], n=0) == True

# Edge case: Single planted plot, n=0
assert sol.canPlaceFlowers(flowerbed=[1], n=0) == True

# Edge case: Single planted plot, n=1
assert sol.canPlaceFlowers(flowerbed=[1], n=1) == False

# Edge case: All empty, length 3, max placements
assert sol.canPlaceFlowers(flowerbed=[0, 0, 0], n=2) == True

# Edge case: All empty, length 3, less than max
assert sol.canPlaceFlowers(flowerbed=[0, 0, 0], n=1) == True

# Edge case: All empty, length 3, more than max
assert sol.canPlaceFlowers(flowerbed=[0, 0, 0], n=3) == False

# Edge case: Placements at beginning and end
assert sol.canPlaceFlowers(flowerbed=[0, 0, 1, 0, 0], n=2) == True

# Edge case: Less than max for mixed
assert sol.canPlaceFlowers(flowerbed=[0, 0, 1, 0, 0], n=1) == True

# Edge case: All empty, length 5, max=3
assert sol.canPlaceFlowers(flowerbed=[0] * 5, n=3) == True

# Edge case: All empty, length 5, less than max
assert sol.canPlaceFlowers(flowerbed=[0] * 5, n=2) == True

# Edge case: No possible placements, n=0
assert sol.canPlaceFlowers(flowerbed=[1, 0, 1, 0, 1], n=0) == True

# Edge case: No possible placements, n=1
assert sol.canPlaceFlowers(flowerbed=[1, 0, 1, 0, 1], n=1) == False


