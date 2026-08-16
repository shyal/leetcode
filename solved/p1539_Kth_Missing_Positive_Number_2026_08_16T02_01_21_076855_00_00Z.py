"""
URL: https://leetcode.com/problems/kth-missing-positive-number/description/?envType=problem-list-v2&envId=vn57k9wr

1539. Kth Missing Positive Number

Given an array arr of positive integers sorted in a strictly increasing order,
and an integer k.

Return the kth positive integer that is missing from this array.


Example 1:

Input: arr = [2,3,4,7,11], k = 5
Output: 9
Explanation: The missing positive integers are [1,5,6,8,9,10,12,13,...].
The 5th missing positive integer is 9.

Example 2:

Input: arr = [1,2,3,4], k = 2
Output: 6
Explanation: The missing positive integers are [5,6,7,...].
The 2nd missing positive integer is 6.


Constraints:

    1 <= arr.length <= 1000
    1 <= arr[i] <= 1000
    1 <= k <= 1000
    arr[i] < arr[j] for 1 <= i < j <= arr.length


Follow up:

Could you solve this problem in less than O(n) complexity?

---

Not happy about needing this break statement:

if mid >= len(arr):
    break

Other than that, felt like a relatively clean solve.

"""


class Solution:
    def findKthPositive(self, arr: List[int], k: int) -> int:
        left, right = 0, len(arr)
        while left <= right:
            mid = (left + right) // 2
            if mid >= len(arr):
                break
            missing = arr[mid] - mid - 1
            if missing < k:
                left = mid + 1
            else:
                right = mid - 1
        return left + k


sol = Solution()

print(sol.findKthPositive([2, 3, 4, 7, 11], 5))  # 9

# assert sol.findKthPositive([2, 3, 4, 7, 11], 5) == 9
# assert sol.findKthPositive([1, 2, 3, 4], 2) == 6
# assert sol.findKthPositive([1], 1) == 2
# assert sol.findKthPositive([2], 1) == 1
# assert sol.findKthPositive([1], 1000) == 1001
# assert sol.findKthPositive([1000], 1000) == 1001
# assert sol.findKthPositive([1000], 999) == 999
# assert sol.findKthPositive([2, 3, 4, 7, 11], 1) == 1
# assert sol.findKthPositive([2, 3, 4, 7, 11], 4) == 8
# assert sol.findKthPositive([2, 3, 4, 7, 11], 6) == 10
# assert sol.findKthPositive([2, 3, 4, 7, 11], 7) == 12
# assert sol.findKthPositive([3, 4, 5], 2) == 2
# assert sol.findKthPositive([3, 4, 5], 3) == 6
# assert sol.findKthPositive([5, 6, 7, 8, 9], 4) == 4
# assert sol.findKthPositive([5, 6, 7, 8, 9], 5) == 10
# assert sol.findKthPositive([5, 6, 7, 8, 9], 9) == 14
# assert sol.findKthPositive([2, 4, 6, 8], 3) == 5
# assert sol.findKthPositive([2, 4, 6, 8], 4) == 7
# assert sol.findKthPositive([2, 4, 6, 8], 5) == 9
# assert sol.findKthPositive([1, 3], 1) == 2
# assert sol.findKthPositive([1, 2, 3, 4, 5, 6, 7], 1) == 8
# assert sol.findKthPositive([7], 6) == 6
# assert sol.findKthPositive([7], 7) == 8
# assert sol.findKthPositive(list(range(1, 1001)), 1000) == 2000
# assert sol.findKthPositive([1, 1000], 998) == 999
# assert sol.findKthPositive([1, 1000], 999) == 1001