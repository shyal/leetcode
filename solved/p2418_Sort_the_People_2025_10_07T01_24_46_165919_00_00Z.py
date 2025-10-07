"""
URL: https://leetcode.com/problems/sort-the-people/description/

2418. Sort the People

You are given an array of strings names, and an array heights that consists of distinct positive integers. Both arrays are of length n.

For each index i, names[i] and heights[i] denote the name and height of the i-th person.

Return names sorted in descending order by the people's heights.


Example 1:

Input: names = ["Mary","John","Emma"], heights = [180,165,170]
Output: ["Mary","Emma","John"]
Explanation: Mary is the tallest, followed by Emma and John.

Example 2:

Input: names = ["Alice","Bob","Bob"], heights = [155,185,150]
Output: ["Bob","Alice","Bob"]
Explanation: First Bob is the tallest, followed by Alice and second Bob.


Constraints:

    n == names.length == heights.length
    1 <= n <= 1000
    1 <= names[i].length <= 20
    1 <= heights[i] <= 10^5
    All the values of heights are distinct.
"""


class Solution:
    def sortPeople(self, names: List[str], heights: List[int]) -> List[str]:
        enum = [*enumerate(names)]
        enum.sort(key=lambda x: heights[x[0]])
        return [x[1] for x in enum][::-1]


sol = Solution()

assert sol.sortPeople(["Mary", "John", "Emma"], [180, 165, 170]) == [
    "Mary",
    "Emma",
    "John",
]
assert sol.sortPeople(["Alice", "Bob", "Bob"], [155, 185, 150]) == [
    "Bob",
    "Alice",
    "Bob",
]
assert sol.sortPeople(["Alice"], [100]) == ["Alice"]
assert sol.sortPeople(["A", "B"], [1, 2]) == ["B", "A"]
assert sol.sortPeople(["A", "B"], [2, 1]) == ["A", "B"]
assert sol.sortPeople(["Short", "Tall", "Medium"], [1, 100000, 50000]) == [
    "Tall",
    "Medium",
    "Short",
]
assert sol.sortPeople(["X", "Y", "X"], [100, 200, 150]) == ["Y", "X", "X"]
