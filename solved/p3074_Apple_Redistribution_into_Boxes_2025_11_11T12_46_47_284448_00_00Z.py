"""
URL: https://leetcode.com/problems/apple-redistribution-into-boxes/description/?envType=problem-list-v2&envId=vn57k9wr

3074. Apple Redistribution into Boxes

You are given an array apple of size n and an array capacity of size m.

There are n packs where the ith pack contains apple[i] apples. There are m boxes as well, and the ith box has a capacity of capacity[i] apples.

Return the minimum number of boxes you need to select to redistribute these n packs of apples into boxes.

Note that, apples from the same pack can be distributed into different boxes.

Example 1:

Input: apple = [1,3,2], capacity = [4,3,1,5,2]
Output: 2
Explanation: We will use boxes with capacities 4 and 5.
It is possible to distribute the apples as the total capacity is greater than or equal to the total number of apples.

Example 2:

Input: apple = [5,5,5], capacity = [2,4,2,7]
Output: 4
Explanation: We will need to use all the boxes.

Constraints:

    1 <= n == apple.length <= 50
    1 <= m == capacity.length <= 50
    1 <= apple[i], capacity[i] <= 50
    The input is generated such that it's possible to redistribute packs of apples into boxes.

"""


class Solution:
    def minimumBoxes(self, apple: List[int], capacity: List[int]) -> int:
        capacity.sort(reverse=True)
        num_apples = sum(apple)
        _sum = 0
        for i, c in enumerate(capacity):
            _sum += c
            if _sum >= num_apples:
                return i + 1
        return -1


sol = Solution()

# print(sol.minimumBoxes([1, 3, 2], [4, 3, 1, 5, 2]))  # 2

assert sol.minimumBoxes([1, 3, 2], [4, 3, 1, 5, 2]) == 2
assert sol.minimumBoxes([5, 5, 5], [2, 4, 2, 7]) == 4
assert sol.minimumBoxes([1], [1]) == 1
assert sol.minimumBoxes([2], [1, 1]) == 2
assert sol.minimumBoxes([1, 1, 1], [10]) == 1
assert sol.minimumBoxes([5], [1, 2, 3, 4]) == 2
assert sol.minimumBoxes([50], [50]) == 1
assert sol.minimumBoxes([50], [49, 1]) == 2
assert sol.minimumBoxes([1] * 50, [50]) == 1
assert sol.minimumBoxes([1] * 50, [1] * 50) == 50
assert sol.minimumBoxes([50] * 50, [50] * 50) == 50
assert sol.minimumBoxes([10, 20, 30], [15, 25, 35]) == 2
# assert sol.minimumBoxes([1, 2, 3, 4, 5], [5, 4, 3, 2, 1]) == 3
