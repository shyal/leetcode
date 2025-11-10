"""
URL: https://leetcode.com/problems/can-make-arithmetic-progression-from-sequence/description/?envType=problem-list-v2&envId=vn57k9wr

1502. Can Make Arithmetic Progression From Sequence

A sequence of numbers is called an arithmetic progression if the difference between any two consecutive elements is the same.

Given an array of numbers arr, return true if the array can be rearranged to form an arithmetic progression. Otherwise, return false.

Example 1:

Input: arr = [3,5,1]
Output: true
Explanation: We can reorder the elements as [1,3,5] or [5,3,1] with differences 2 and -2 respectively, between each consecutive elements.

Example 2:

Input: arr = [1,2,4]
Output: false
Explanation: There is no way to reorder the elements to obtain an arithmetic progression.

Constraints:

    2 <= arr.length <= 1000
    -10^6 <= arr[i] <= 10^6
"""


class Solution:
    def canMakeArithmeticProgression(self, arr: List[int]) -> bool:
        return len(set(b - a for a, b in pairwise(sorted(arr)))) == 1


sol = Solution()

# print(sol.canMakeArithmeticProgression([3, 5, 1]))  # True

assert sol.canMakeArithmeticProgression([3, 5, 1]) == True
assert sol.canMakeArithmeticProgression([1, 2, 4]) == False
assert sol.canMakeArithmeticProgression([1, 3]) == True
assert sol.canMakeArithmeticProgression([1, 1]) == True
assert sol.canMakeArithmeticProgression([2, 2, 2]) == True
assert sol.canMakeArithmeticProgression([1, 1, 2]) == False
assert sol.canMakeArithmeticProgression([-1, -3, -5]) == True
assert sol.canMakeArithmeticProgression([0, -2, 2]) == True
assert sol.canMakeArithmeticProgression([1, 3, 6]) == False
assert sol.canMakeArithmeticProgression([1000000, -1000000]) == True
assert sol.canMakeArithmeticProgression([1000000, 0, -1000000]) == True
assert sol.canMakeArithmeticProgression([1000000, 1, -1000000]) == False
assert sol.canMakeArithmeticProgression([5, 1, 9, 13, 17]) == True
assert sol.canMakeArithmeticProgression([5, 1, 9, 13, 18]) == False
assert sol.canMakeArithmeticProgression([-10, -20, -30, -40]) == True
assert sol.canMakeArithmeticProgression([10, 20, 30, 41]) == False
