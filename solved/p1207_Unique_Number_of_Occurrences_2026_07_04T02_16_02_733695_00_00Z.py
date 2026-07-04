"""
URL: https://leetcode.com/problems/unique-number-of-occurrences/description/?envType=problem-list-v2&envId=vn57k9wr

1207. Unique Number of Occurrences

Given an array of integers arr, return true if the number of occurrences of
each value in the array is unique or false otherwise.


Example 1:

Input: arr = [1,2,2,1,1,3]
Output: true
Explanation: The value 1 has 3 occurrences, 2 has 2 and 3 has 1. No two values have the same number of occurrences.

Example 2:

Input: arr = [1,2]
Output: false

Example 3:

Input: arr = [-3,0,1,-3,1,1,1,-3,10,0]
Output: true


Constraints:

    1 <= arr.length <= 1000
    -1000 <= arr[i] <= 1000
"""

class Solution:
    def uniqueOccurrences(self, arr: List[int]) -> bool:
        c = Counter(arr).values()
        return len(c) == len(set(c))


sol = Solution()

print(sol.uniqueOccurrences([1, 2, 2, 1, 1, 3]))  # True

assert sol.uniqueOccurrences([1, 2, 2, 1, 1, 3]) == True
assert sol.uniqueOccurrences([1, 2]) == False
assert sol.uniqueOccurrences([-3, 0, 1, -3, 1, 1, 1, -3, 10, 0]) == True
assert sol.uniqueOccurrences([5]) == True
assert sol.uniqueOccurrences([0]) == True
assert sol.uniqueOccurrences([7, 7, 7]) == True
assert sol.uniqueOccurrences([0, 0, 0, 0]) == True
assert sol.uniqueOccurrences([1, 1, 2, 2]) == False
assert sol.uniqueOccurrences([1, 2, 3]) == False
assert sol.uniqueOccurrences([3, 3, 2, 2, 1]) == False
assert sol.uniqueOccurrences([-1, 1, -1, 1]) == False
assert sol.uniqueOccurrences([-1000, -1000, 1000]) == True
assert sol.uniqueOccurrences([-3, -3, -3, -2, -2, -1]) == True
assert sol.uniqueOccurrences([2, 2, 5, 5, 5, 8]) == True
assert sol.uniqueOccurrences([1, 2, 2, 3, 3, 3, 4, 4, 4, 4]) == True
assert sol.uniqueOccurrences([1, 1, 2, 2, 3]) == False
assert sol.uniqueOccurrences([1000] * 4 + [-1000] * 3 + [0] * 2 + [5]) == True
assert sol.uniqueOccurrences([1000, -1000]) == False
assert sol.uniqueOccurrences([1] * 500 + [2] * 500) == False
assert sol.uniqueOccurrences([1] * 501 + [2] * 499) == True
assert sol.uniqueOccurrences([0, -1, 0, -1, 0]) == True
assert sol.uniqueOccurrences([6, 6, 6, 1, 1, 1, 7, 7, 7]) == False