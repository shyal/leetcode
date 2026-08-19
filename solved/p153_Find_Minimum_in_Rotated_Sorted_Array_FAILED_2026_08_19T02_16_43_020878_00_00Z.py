"""
URL: https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/description/?envType=problem-list-v2&envId=vn57k9wr

153. Find Minimum in Rotated Sorted Array

Suppose an array of length n sorted in ascending order is rotated between 1 and n times.
For example, the array nums = [0,1,2,4,5,6,7] might become:

    [4,5,6,7,0,1,2] if it was rotated 4 times.
    [0,1,2,4,5,6,7] if it was rotated 7 times.

Notice that rotating an array [a[0], a[1], a[2], ..., a[n-1]] 1 time results in the array
[a[n-1], a[0], a[1], a[2], ..., a[n-2]].

Given the sorted rotated array nums of unique elements, return the minimum element of this array.

You must write an algorithm that runs in O(log n) time.


Example 1:

Input: nums = [3,4,5,1,2]
Output: 1
Explanation: The original array was [1,2,3,4,5] rotated 3 times.

Example 2:

Input: nums = [4,5,6,7,0,1,2]
Output: 0
Explanation: The original array was [0,1,2,4,5,6,7] and it was rotated 4 times.

Example 3:

Input: nums = [11,13,15,17]
Output: 11
Explanation: The original array was [11,13,15,17] and it was rotated 4 times.


Constraints:

    n == nums.length
    1 <= n <= 5000
    -5000 <= nums[i] <= 5000
    All the integers of nums are unique.
    nums is sorted and rotated between 1 and n times.

---

 l
       m
[3,4,5,6,7,8,0,1]
               r

       l
           m
[3,4,5,6,7,8,0,1]
               r

           l
             m
[3,4,5,6,7,8,0,1]
               r
             l
             m
[3,4,5,6,7,8,0,1]
               r

------------------

 l
       m
[7,8,0,1,3,4,5,6]
               r
 l
   m
[7,8,0,1,3,4,5,6]
       r
 l
 m
[7,8,0,1,3,4,5,6]
   r
"""



class Solution:
    def findMin(self, nums: List[int]) -> int:
      left = 0
      right = len(nums) - 1
      result = -1

      while left < right:
          mid = left + (right - left) // 2
          left_val = nums[left]
          mid_val = nums[mid]
          right_val = nums[right]
          if left_val < mid_val:
              if right < len(nums) -1 and nums[right+1] < nums[right]:
                  return nums[right+1]
              else:
                  left = mid
          else:
              if left > 0 and nums[left-1] > nums[left]:
                  return nums[left-1]
              right = mid

      return result


sol = Solution()

print(sol.findMin([3,4,5,6,7,8,0,1]))  # 0

# assert sol.findMin([3, 4, 5, 1, 2]) == 1
# assert sol.findMin([4, 5, 6, 7, 0, 1, 2]) == 0
# assert sol.findMin([11, 13, 15, 17]) == 11
# assert sol.findMin([1]) == 1
# assert sol.findMin([-5000]) == -5000
# assert sol.findMin([2, 1]) == 1
# assert sol.findMin([1, 2]) == 1
# assert sol.findMin([3, 1, 2]) == 1
# assert sol.findMin([2, 3, 1]) == 1
# assert sol.findMin([1, 2, 3]) == 1
# assert sol.findMin([1, 2, 3, 4, 5]) == 1
# assert sol.findMin([5, 1, 2, 3, 4]) == 1
# assert sol.findMin([2, 3, 4, 5, 1]) == 1
# assert sol.findMin([7, 0, 1, 2, 4, 5, 6]) == 0
# assert sol.findMin([1, 2, 4, 5, 6, 7, 0]) == 0
# assert sol.findMin([2, 4, 5, 6, 7, 0, 1]) == 0
# assert sol.findMin([-1, -2]) == -2
# assert sol.findMin([4, 5, -3, -1, 0, 2]) == -3
# assert sol.findMin([-5000, 5000]) == -5000
# assert sol.findMin([5000, -5000]) == -5000
# assert sol.findMin([0, 1, 2, 4, 5, 6, 7]) == 0
# assert sol.findMin([2, 3, 4, 5, 6, 7, 8, 9, 1]) == 1
# assert sol.findMin([-2, -1, 0, 1, 2, -5, -4, -3]) == -5
# assert sol.findMin(list(range(1000, 5000)) + list(range(0, 1000))) == 0
# assert sol.findMin(list(range(-5000, 0))) == -5000

# FAILED: walked away after 26m 48s; no working solution.
# Judge the moves actually attempted as struggled, not clean.
