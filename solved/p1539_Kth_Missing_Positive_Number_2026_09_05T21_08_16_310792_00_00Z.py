"""
URL: https://leetcode.com/problems/kth-missing-positive-number/description/?envType=problem-list-v2&envId=vn57k9wr

1539. Kth Missing Positive Number

Given an array arr of positive integers sorted in a strictly increasing order, and an integer k.

Return the kth positive integer that is missing from this array.

Example 1:

Input: arr = [2,3,4,7,11], k = 5
Output: 9
Explanation: The missing positive integers are [1,5,6,8,9,10,12,13,...]. The 5th missing positive integer is 9.

Example 2:

Input: arr = [1,2,3,4], k = 2
Output: 6
Explanation: The missing positive integers are [5,6,7,...]. The 2nd missing positive integer is 6.

Constraints:

    1 <= arr.length <= 1000
    1 <= arr[i] <= 1000
    1 <= k <= 1000
    arr[i] < arr[j] for 1 <= i < j <= arr.length

Follow up:

Could you solve this problem in less than O(n) complexity?

---

          m
                                 r
    l
    0  1  2        3            4
[   2, 3, 4,       7,          11]
          1
  1.         5  6.    8. 9. 10


                   m
                                 r
                   l
    0  1  2        3            4
[   2, 3, 4,       7,          11]
          1
  1.         5  6.    8. 9. 10


Solved. Feels like a fluke.. mixture of it clicking and memorization.

"""


class Solution:
    def findKthPositive(self, arr: List[int], k: int) -> int:
        left, right = 0, len(arr) - 1
        while left <= right:
            mid = (left + right) // 2
            missing = arr[mid] - mid - 1
            if missing == k:
                break
            elif missing <= k:
                left = mid + 1
            else:
                right = mid - 1
        return left + k


sol = Solution()

print(sol.findKthPositive([2, 3, 4, 7, 11], 5))  # 9

assert sol.findKthPositive([2, 3, 4, 7, 11], 5) == 9
assert sol.findKthPositive([1, 2, 3, 4], 2) == 6

assert sol.findKthPositive([1], 1) == 2
assert sol.findKthPositive([1000], 1000) == 1001
assert sol.findKthPositive([1, 3, 5, 7, 9], 3) == 6
assert sol.findKthPositive([2, 4, 6, 8, 10], 5) == 9
assert sol.findKthPositive([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 1) == 11
assert sol.findKthPositive([10, 20, 30, 40, 50], 15) == 16
assert sol.findKthPositive([999], 1) == 1
assert sol.findKthPositive([1, 2, 3, 4, 5], 1000) == 1005
assert sol.findKthPositive([1, 1000], 999) == 1001
assert sol.findKthPositive([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 1000) == 1010
assert sol.findKthPositive([1, 2, 4, 5, 7, 8, 10], 4) == 11
assert sol.findKthPositive([3, 4, 5, 6, 7, 8, 9], 2) == 2
