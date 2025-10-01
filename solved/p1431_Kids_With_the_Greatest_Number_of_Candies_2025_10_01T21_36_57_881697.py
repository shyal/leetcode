"""
1431. Kids With the Greatest Number of Candies
Easy
There are n kids with candies. You are given an integer array candies, where each candies[i] represents the number of candies the ith kid has, and an integer extraCandies, denoting the number of extra candies that you have.

Return a boolean array result of length n, where result[i] is true if, after giving the ith kid all the extraCandies, they will have the greatest number of candies among all the kids, or false otherwise.

Note that multiple kids can have the greatest number of candies.

 

Example 1:

Input: candies = [2,3,5,1,3], extraCandies = 3
Output: [true,true,true,false,true] 
Explanation: If you give all extraCandies to:
- Kid 1, they will have 2 + 3 = 5 candies, which is the greatest among the kids.
- Kid 2, they will have 3 + 3 = 6 candies, which is the greatest among the kids.
- Kid 3, they will have 5 + 3 = 8 candies, which is the greatest among the kids.
- Kid 4, they will have 1 + 3 = 4 candies, which is not the greatest among the kids.
- Kid 5, they will have 3 + 3 = 6 candies, which is the greatest among the kids.
Example 2:

Input: candies = [4,2,1,1,2], extraCandies = 1
Output: [true,false,false,false,false] 
Explanation: There is only 1 extra candy.
Kid 1 will always have the greatest number of candies, even if a different kid is given the extra candy.
Example 3:

Input: candies = [12,1,12], extraCandies = 10
Output: [true,false,true]
 

Constraints:

n == candies.length
2 <= n <= 100
1 <= candies[i] <= 100
1 <= extraCandies <= 50
"""


class Solution:
    def kidsWithCandies(self, candies: List[int], extraCandies: int) -> List[bool]:
        _max = max(candies)
        return [x + extraCandies >= _max for x in candies]


sol = Solution()

true = True
false = False

# Existing test cases
assert sol.kidsWithCandies(candies=[2, 3, 5, 1, 3], extraCandies=3) == [
    True,
    True,
    True,
    False,
    True,
]
assert sol.kidsWithCandies(candies=[4, 2, 1, 1, 2], extraCandies=1) == [
    True,
    False,
    False,
    False,
    False,
]
assert sol.kidsWithCandies(candies=[12, 1, 12], extraCandies=10) == [True, False, True]

# Edge case: Minimum n=2, equal candies, minimal extra
assert sol.kidsWithCandies(candies=[1, 1], extraCandies=1) == [True, True]

# Edge case: Minimum n=2, different candies, extra insufficient for smaller
assert sol.kidsWithCandies(candies=[1, 100], extraCandies=1) == [False, True]

# Edge case: All candies equal, extra=1
assert sol.kidsWithCandies(candies=[50, 50, 50, 50], extraCandies=1) == [
    True,
    True,
    True,
    True,
]

# Edge case: All candies minimal (1), extra maximal (50)
assert sol.kidsWithCandies(candies=[1, 1, 1], extraCandies=50) == [True, True, True]

# Edge case: Candies maximal (100), extra minimal (1)
assert sol.kidsWithCandies(candies=[100, 100], extraCandies=1) == [True, True]

# Edge case: Extra makes all able to reach or exceed max
assert sol.kidsWithCandies(candies=[1, 2, 3], extraCandies=2) == [True, True, True]

# Edge case: Extra insufficient for some, sufficient for others
assert sol.kidsWithCandies(candies=[1, 2, 3], extraCandies=1) == [False, True, True]

# Edge case: Multiple max values, extra=1
assert sol.kidsWithCandies(candies=[5, 3, 5, 4], extraCandies=1) == [
    True,
    False,
    True,
    True,
]


