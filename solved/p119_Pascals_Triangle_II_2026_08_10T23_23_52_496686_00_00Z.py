"""
URL: https://leetcode.com/problems/pascals-triangle-ii/description/?envType=problem-list-v2&envId=vn57k9wr

119. Pascal's Triangle II

Given an integer rowIndex, return the rowIndex-th (0-indexed) row of the
Pascal's triangle.

In Pascal's triangle, each number is the sum of the two numbers directly
above it as shown:

    https://upload.wikimedia.org/wikipedia/commons/0/0d/PascalTriangleAnimated2.gif


Example 1:

Input: rowIndex = 3
Output: [1,3,3,1]

Example 2:

Input: rowIndex = 0
Output: [1]

Example 3:

Input: rowIndex = 1
Output: [1,1]


Constraints:

    0 <= rowIndex <= 33


Follow up: Could you optimize your algorithm to use only O(rowIndex) extra space?
"""


class Solution:
    def getRow(self, rowIndex: int) -> List[int]:
        vals = [1]
        for _ in range(rowIndex):
            vals = [1] + [*map(lambda a: a[0] + a[1], zip(vals[1:], vals[:-1]))] + [1]
        return vals
        


def _expected_row(n: int) -> List[int]:
    row = [1]
    for k in range(n):
        row.append(row[-1] * (n - k) // (k + 1))
    return row


sol = Solution()

assert sol.getRow(3) == [1, 3, 3, 1]
assert sol.getRow(0) == [1]
assert sol.getRow(1) == [1, 1]

assert sol.getRow(2) == [1, 2, 1]
assert sol.getRow(4) == [1, 4, 6, 4, 1]
assert sol.getRow(5) == [1, 5, 10, 10, 5, 1]
assert sol.getRow(6) == [1, 6, 15, 20, 15, 6, 1]
assert sol.getRow(10) == [1, 10, 45, 120, 210, 252, 210, 120, 45, 10, 1]

for _n in range(34):
    _row = sol.getRow(_n)
    assert _row == _expected_row(_n)
    assert len(_row) == _n + 1
    assert _row[0] == 1 and _row[-1] == 1
    assert _row == _row[::-1]
    assert sum(_row) == 2 ** _n
    assert all(isinstance(_v, int) and _v > 0 for _v in _row)

for _n in range(1, 34):
    _prev = sol.getRow(_n - 1)
    _cur = sol.getRow(_n)
    assert all(_cur[_j] == _prev[_j - 1] + _prev[_j] for _j in range(1, _n))

assert sol.getRow(33)[:4] == [1, 33, 528, 5456]
assert max(sol.getRow(33)) == 1166803110
assert len(sol.getRow(33)) == 34
assert sum(sol.getRow(33)) == 2 ** 33

_mutated = sol.getRow(5)
_mutated[0] = 99
_mutated.append(99)
assert sol.getRow(5) == [1, 5, 10, 10, 5, 1]
assert sol.getRow(0) is not sol.getRow(0)

assert Solution().getRow(7) == sol.getRow(7)
assert sol.getRow(4) == sol.getRow(4)