"""
URL: https://leetcode.com/problems/delete-greatest-value-in-each-row/description/?envType=daily-question&envId=2023-05-25

2500. Delete Greatest Value in Each Row

You are given an m x n matrix grid consisting of positive integers.

Perform the following operation until grid becomes empty:

    Delete the element with the greatest value from each row. If there is a tie for the greatest value in a row, delete any one of the greatest value elements.
    Add the maximum of deleted elements to the answer.

Note that the number of columns decreases by one after each operation.

Return the answer after performing the operations until grid becomes empty.


Example 1:

Input: grid = [[1,2,4],[3,3,1]]
Output: 8
Explanation: The diagram above shows the removed values in each step.
- In the first operation, we remove 4 from the first row and 3 from the second row (notice that, there are two cells with value 3 in the second row, we can remove any of them). We add max(4,3)=4 to the answer.
- In the second operation, we remove 2 from the first row and 3 from the second row. We add max(2,3)=3 to the answer.
- In the third operation, we remove 1 from the first row and 1 from the second row. We add max(1,1)=1 to the answer.
The final answer = 4 + 3 + 1 = 8.

Example 2:

Input: grid = [[10]]
Output: 10
Explanation: There is only one operation: remove 10 from the only row. The final answer = 10.


Constraints:

    m == grid.length
    n == grid[i].length
    1 <= m, n <= 50
    1 <= grid[i][j] <= 100
"""


class Solution:
    def deleteGreatestValue(self, grid: List[List[int]]) -> int:
        for row in grid:
            heapify(row)

        return sum(max(heappop(row) for row in grid) for _ in range(len(grid[0])))


sol = Solution()

# print(sol.deleteGreatestValue([[1, 2, 4], [3, 3, 1]]))  # 8

assert sol.deleteGreatestValue([[1, 2, 4], [3, 3, 1]]) == 8
assert sol.deleteGreatestValue([[10]]) == 10
assert sol.deleteGreatestValue([[1, 2, 3, 4]]) == 10
assert sol.deleteGreatestValue([[1], [3], [2], [4]]) == 4
assert sol.deleteGreatestValue([[2, 2], [2, 2]]) == 4
assert sol.deleteGreatestValue([[10, 5, 1], [9, 4, 2], [8, 3, 1]]) == 17
assert sol.deleteGreatestValue([[1, 3, 3], [2, 2, 4]]) == 9
assert sol.deleteGreatestValue([[1, 100]]) == 101
assert sol.deleteGreatestValue([[1], [100]]) == 100
