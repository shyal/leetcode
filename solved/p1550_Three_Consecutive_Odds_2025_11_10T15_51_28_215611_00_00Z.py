"""
URL: https://leetcode.com/problems/three-consecutive-odds/description/?envType=problem-list-v2&envId=vn57k9wr

1550. Three Consecutive Odds

Given an integer array arr, return true if there are three consecutive odd numbers in the array. Otherwise, return false.


Example 1:

Input: arr = [2,6,4,1]
Output: false
Explanation: There are no three consecutive odds.

Example 2:

Input: arr = [1,2,34,3,4,5,7,23,12]
Output: true
Explanation: [5,7,23] are three consecutive odds.


Constraints:

    1 <= arr.length <= 1000
    1 <= arr[i] <= 1000
"""


class Solution:
    def threeConsecutiveOdds(self, arr: List[int]) -> bool:
        return any(
            len(list(v)) >= 3 for k, v in groupby(arr, key=lambda x: x % 2 != 0) if k
        )


sol = Solution()

# print(sol.threeConsecutiveOdds([2, 6, 4, 1]))  # false

assert sol.threeConsecutiveOdds([2, 6, 4, 1]) == False
assert sol.threeConsecutiveOdds([1, 2, 34, 3, 4, 5, 7, 23, 12]) == True
assert sol.threeConsecutiveOdds([1]) == False
assert sol.threeConsecutiveOdds([1, 3]) == False
assert sol.threeConsecutiveOdds([1, 3, 5]) == True
assert sol.threeConsecutiveOdds([2, 4, 6]) == False
assert sol.threeConsecutiveOdds([1, 3, 5, 7]) == True
assert sol.threeConsecutiveOdds([2, 1, 3, 5, 4]) == True
assert sol.threeConsecutiveOdds([1, 3, 2, 5, 7, 9]) == True
assert sol.threeConsecutiveOdds([2, 4, 6, 8, 10]) == False
assert sol.threeConsecutiveOdds([2, 4, 1, 3]) == False
assert sol.threeConsecutiveOdds([1, 3, 5, 2]) == True
assert sol.threeConsecutiveOdds([2, 1, 4]) == False
assert sol.threeConsecutiveOdds([1, 2, 3, 4, 5]) == False
assert sol.threeConsecutiveOdds([999, 997, 995, 2, 4]) == True
assert sol.threeConsecutiveOdds([1000, 998, 996]) == False
