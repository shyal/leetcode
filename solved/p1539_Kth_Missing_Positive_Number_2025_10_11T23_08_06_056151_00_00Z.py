"""
URL: https://leetcode.com/problems/kth-missing-positive-number/

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

---

Ok so solving this problem in less than O(n) is possible
but non trivial.

The first element of the array alreasy tells us how many values
are missing from the front of the array.

So we can deduct that from k.

Then we can compute the number of missing elements between two pointers
by comparing the delta of their values with the delta of their indices.

e.g if L is at val 2, and M is at val 4, but their indices are 0 and 2,
there are no missing values. In which case is k = 2, we can go right, because
the missing value has to be on the right side.

Interesting problem, but it feels quite hard right now. Will revisit later.

"""


class Solution:
    def findKthPositive(self, arr: List[int], k: int) -> int:
        # not my solution
        left, right = 0, len(arr) - 1
        while left <= right:
            mid = (left + right) // 2
            missing = arr[mid] - mid - 1
            if missing < k:
                left = mid + 1
            else:
                right = mid - 1
        return left + k


sol = Solution()

print(sol.findKthPositive([2, 3, 4, 7, 11], 5))

# assert sol.findKthPositive([2, 3, 4, 7, 11], 5) == 9
# assert sol.findKthPositive([1,2,3,4], 2) == 6
# assert sol.findKthPositive([1], 1) == 2
# assert sol.findKthPositive([5], 1) == 1
# assert sol.findKthPositive([5], 4) == 4
# assert sol.findKthPositive([5], 5) == 6
# assert sol.findKthPositive([1,3], 1) == 2
# assert sol.findKthPositive([1,3], 2) == 4
# assert sol.findKthPositive([1000], 1000) == 1001
# assert sol.findKthPositive([1000], 999) == 999
# assert sol.findKthPositive([1,2], 1) == 3
# assert sol.findKthPositive([3,10], 2) == 2
# assert sol.findKthPositive([3,10], 3) == 4
