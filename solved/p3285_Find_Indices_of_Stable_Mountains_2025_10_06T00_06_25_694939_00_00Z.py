"""
URL: https://leetcode.com/problems/find-indices-of-stable-mountains/description/?envType=problem-list-v2&envId=xxx

3285. Find Indices of Stable Mountains

There are n mountains in a row, and the height of each mountain is given in the array height where height[i] represents the height of mountain i (0-indexed).

A mountain i (1 <= i < n) is stable if height[i - 1] > threshold.

Return a list of indices (0-indexed) of all stable mountains in ascending order.


Example 1:

Input: height = [1,2,3,4], threshold = 2
Output: [3]
Explanation:
- Mountain 1 has height[0] = 1 which is not greater than threshold = 2.
- Mountain 2 has height[1] = 2 which is not greater than threshold = 2.
- Mountain 3 has height[2] = 3 which is greater than threshold = 2.

Example 2:

Input: height = [10,1,10,1,10], threshold = 3
Output: [1,3]

Example 3:

Input: height = [10,1,10,1,10], threshold = 10
Output: []


Constraints:

    2 <= height.length <= 100
    1 <= height[i] <= 100
    1 <= threshold <= 100
"""


class Solution:
    def stableMountains(self, height: List[int], threshold: int) -> List[int]:
        res = []
        for i in range(1, len(height)):
            if height[i - 1] > threshold:
                res.append(i)
        return res


sol = Solution()

assert sol.stableMountains([1, 2, 3, 4], 2) == [3]
assert sol.stableMountains([10, 1, 10, 1, 10], 3) == [1, 3]
assert sol.stableMountains([10, 1, 10, 1, 10], 10) == []
assert sol.stableMountains([1, 1], 1) == []
assert sol.stableMountains([2, 1], 1) == [1]
assert sol.stableMountains([1, 2], 1) == []
assert sol.stableMountains([100, 100], 99) == [1]
assert sol.stableMountains([100, 100], 100) == []
assert sol.stableMountains([1, 2, 3, 4, 5], 2) == [3, 4]
assert sol.stableMountains([3, 3, 3, 3], 2) == [1, 2, 3]
assert sol.stableMountains([2, 2, 2], 2) == []
assert sol.stableMountains([10, 1, 10, 1, 10, 1, 10], 5) == [1, 3, 5]
assert sol.stableMountains([1, 1, 1, 1, 1], 1) == []
assert sol.stableMountains([100, 100, 100, 100, 100], 99) == [1, 2, 3, 4]
assert sol.stableMountains([5, 1, 5], 4) == [1]
assert sol.stableMountains([99, 100], 99) == []
assert sol.stableMountains([100, 99], 99) == [1]
