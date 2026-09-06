"""
DRILL: Count Missing Integers
TRAINS: index-value-gap

Given an array arr of positive integers sorted in a strictly increasing
order, return the number of positive integers below arr[-1] that are
missing from the array.

Example 1:

Input: arr = [2,3,4,7,11]
Output: 6
Explanation: The missing positive integers are [1,5,6,8,9,10].

Example 2:

Input: arr = [1,2,3]
Output: 0

Constraints:

    1 <= arr.length <= 1000
    1 <= arr[i] <= 1000
    arr[i] < arr[j] for 1 <= i < j <= arr.length

    REQUIRED: O(1), no loop. Walking arr and counting gaps one by one is
    the failure mode this drill exists to kill.
"""


class Solution:
    def numMissingIntegers(self, arr: list[int]) -> int:
        return arr[-1] - len(arr)


sol = Solution()

print(sol.numMissingIntegers([2, 3, 4, 7, 11]))  # 6

assert sol.numMissingIntegers([2, 3, 4, 7, 11]) == 6
assert sol.numMissingIntegers([1, 2, 3]) == 0
assert sol.numMissingIntegers([5]) == 4
assert sol.numMissingIntegers([1]) == 0
assert sol.numMissingIntegers([1, 100]) == 98
