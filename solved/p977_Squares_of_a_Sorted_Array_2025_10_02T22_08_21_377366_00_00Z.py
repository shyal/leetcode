"""
URL: https://leetcode.com/problems/squares-of-a-sorted-array/description/

977. Squares of a Sorted Array

Given an integer array nums sorted in non-decreasing order, return an array of the squares of each number sorted in non-decreasing order.


Example 1:

Input: nums = [-4,-1,0,3,10]
Output: [0,1,9,16,100]
Explanation: After squaring, the array becomes [16,1,0,9,100].
After sorting, it becomes [0,1,9,16,100].

Example 2:

Input: nums = [-7,-3,2,3,11]
Output: [4,9,9,49,121]


Constraints:

    1 <= nums.length <= 104
    -104 <= nums[i] <= 104
    nums is sorted in non-decreasing order.


Follow up: Squaring each element and sorting the new array is very trivial, could you find an O(n) solution using a different approach?

---

I'm trying to think of the followup:

[-4, -1, 0, 3, 10]
[16, 1, 0, 9, 100]

What i'm noticing is that since we're squaring, we can ignore the sign. But i still can't quite figure
how to sort those elements in O(n).

Oh ok we can look for where the elements go from negative to positive, then merge them.

         v
[-4, -1, 0, 3, 10]

right: 0, 3, 10
left: -1, -4

merged: 0, -1, 3, -4, 10

I'm not really happy with how i merged the arrays. Would be great to revisit some array
problems that force me to merge things in place.

"""


class Solution:

    def bruteForce(self, nums: List[int]) -> List[int]:
        squared = [x**2 for x in nums]
        return [*sorted(squared)]

    def take(self, A, B, a, b):
        if a < len(A) and b < len(B):
            if A[a] < B[b]:
                return A[a], a + 1, b
            else:
                return B[b], a, b + 1
        elif a == len(A) and b < len(B):
            return B[b], a, b + 1
        elif b == len(B) and a < len(A):
            return A[a], a + 1, b
        return None, None, None

    def sortedSquares(self, nums: List[int]) -> List[int]:
        i = bisect_left(nums, 0)
        left = [-x for x in nums[:i][::-1]]
        right = nums[i:]
        arr = []
        a, b = 0, 0
        while True:
            val, a, b = self.take(left, right, a, b)
            if val is None:
                break
            arr.append(val)
        return [x**2 for x in arr]


sol = Solution()

assert sol.sortedSquares([-4, -1, 0, 3, 10]) == [0, 1, 9, 16, 100]
assert sol.sortedSquares([-7, -3, 2, 3, 11]) == [4, 9, 9, 49, 121]
assert sol.sortedSquares([0]) == [0]
assert sol.sortedSquares([1]) == [1]
assert sol.sortedSquares([-1]) == [1]
assert sol.sortedSquares([-5, -4, -2]) == [4, 16, 25]
assert sol.sortedSquares([1, 2, 3]) == [1, 4, 9]
assert sol.sortedSquares([-2, -2, 0, 2, 2]) == [0, 4, 4, 4, 4]
assert sol.sortedSquares([-10000, 0, 10000]) == [0, 100000000, 100000000]
assert sol.sortedSquares([-3, -2, -1]) == [1, 4, 9]
assert sol.sortedSquares([2, 4, 5]) == [4, 16, 25]
assert sol.sortedSquares([0, 0, 1]) == [0, 0, 1]
assert sol.sortedSquares([-3, -2, 0, 0]) == [0, 0, 4, 9]
