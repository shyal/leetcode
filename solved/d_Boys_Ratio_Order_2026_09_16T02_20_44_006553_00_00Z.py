"""
DRILL: Boys Ratio Order
TRAINS: heap-top-k

Given a list classes, where classes[i] = [boys_i, students_i] is a class
with students_i students of whom boys_i are boys, return the classes in
increasing order of the ratio boys_i / students_i. No two classes share a
ratio.

Example 1:

Input: classes = [[3, 4], [1, 2], [2, 3]]
Output: [[1, 2], [2, 3], [3, 4]]
Explanation: The ratios are 0.75, 0.5 and 0.667.

Example 2:

Input: classes = [[1, 5], [4, 5]]
Output: [[1, 5], [4, 5]]

Example 3:

Input: classes = [[2, 2]]
Output: [[2, 2]]

Constraints:

    1 <= classes.length <= 10^5
    1 <= boys_i <= students_i <= 10^5
    All ratios boys_i / students_i are distinct.

    REQUIRED: must build a heap whose items carry the ratio as their first
    element, computed by a function, and pop the classes out in order.
    NO sort, NO sorted, NO key= argument.
"""


class Solution:

    def byRatio(self, classes: List[List[int]]) -> List[List[int]]:
        heap = [[x / y, x, y] for x, y in classes]
        heapify(heap)
        return [heappop(heap)[1:] for _ in classes]


sol = Solution()

print(sol.byRatio([[3, 4], [1, 2], [2, 3]]))  # [[1, 2], [2, 3], [3, 4]]

assert sol.byRatio([[3, 4], [1, 2], [2, 3]]) == [[1, 2], [2, 3], [3, 4]]
assert sol.byRatio([[1, 5], [4, 5]]) == [[1, 5], [4, 5]]
assert sol.byRatio([[2, 2]]) == [[2, 2]]
assert sol.byRatio([[1, 2], [1, 3], [1, 4]]) == [[1, 4], [1, 3], [1, 2]]
assert sol.byRatio([[1, 4], [1, 3], [1, 2]]) == [[1, 4], [1, 3], [1, 2]]
assert sol.byRatio([[5, 5], [1, 100], [50, 99]]) == [[1, 100], [50, 99], [5, 5]]
big = [[1, s] for s in range(2, 100002)]
assert sol.byRatio(big) == big[::-1]
src = open(__file__).read().split("sol = Solution()")[0]
assert "sort" not in src.split('"""')[2] and "key=" not in src.split('"""')[2]
