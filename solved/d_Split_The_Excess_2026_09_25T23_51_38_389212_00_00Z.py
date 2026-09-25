"""
DRILL: Split The Excess
TRAINS: dp-1d-rolling

Given a list row of amounts, return a list new_row of len(row) + 1 amounts.
Every amount in new_row starts at 0. When row[c] is more than 1, half of the
excess row[c] - 1 goes to new_row[c] and the other half to new_row[c + 1].
An amount of 1 or less sends nothing.

Example 1:

Input: row = [10]
Output: [4.5, 4.5]

Example 2:

Input: row = [1.75, 3.5, 1.75]
Output: [0.375, 1.625, 1.625, 0.375]
Explanation: new_row[1] gets 0.375 from row[0] and 1.25 from row[1].

Example 3:

Input: row = [0.375, 1.625, 1.625, 0.375]
Output: [0, 0.3125, 0.625, 0.3125, 0]
Explanation: row[0] and row[3] are under 1 and send nothing.

Constraints:

    1 <= len(row) <= 100
    0 <= row[c] <= 10^9

    REQUIRED: O(len(row)) time, one pass over row. Each amount sends to
    both of its targets in the same step. NO closed-form guess.
---
The mental model i was lacking here is that i was trying to operate
in the resulting row, while in fact we are operating in the row itself
so instead of taking from up, we're pouring down
"""


# mu 0.4
# def nextRow(row: [float]) -> [float]
#   res = table(len(row) + 1)
#   for i, amt in row
#     excess = (amt - 1) / 2
#     if excess > 0
#       res[i] += excess
#       res[i + 1] += excess
#   res

def table(*dims, fill=0):
    if len(dims) == 1:
        return [fill] * dims[0]
    if len(dims) == 2:
        return [[fill] * dims[1] for _ in range(dims[0])]
    return [table(*dims[1:], fill=fill) for _ in range(dims[0])]


class Solution:
    def nextRow(self, row: list[float]) -> list[float]:
        res = table(len(row) + 1)
        for i, amt in enumerate(row):
            excess = (amt - 1) / 2
            if excess > 0:
                res[i] += excess
                res[i + 1] += excess
        return res


sol = Solution()
print(sol.nextRow([10]))
assert sol.nextRow([10]) == [4.5, 4.5]
assert sol.nextRow([1.75, 3.5, 1.75]) == [0.375, 1.625, 1.625, 0.375]
assert sol.nextRow([0.375, 1.625, 1.625, 0.375]) == [0, 0.3125, 0.625, 0.3125, 0]
assert sol.nextRow([1]) == [0, 0]
assert sol.nextRow([0]) == [0, 0]
assert sol.nextRow([5, 1]) == [2, 2, 0]
assert sol.nextRow([1, 5]) == [0, 2, 2]
assert sol.nextRow([3, 1, 3]) == [1, 1, 1, 1]
assert sol.nextRow([1, 1, 7, 1, 1]) == [0, 0, 3, 3, 0, 0]
assert sol.nextRow([10 ** 9]) == [499999999.5, 499999999.5]
