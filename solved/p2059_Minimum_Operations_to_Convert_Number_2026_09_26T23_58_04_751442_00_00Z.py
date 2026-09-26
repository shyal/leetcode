"""
URL: https://leetcode.com/problems/minimum-operations-to-convert-number/description/?envType=problem-list-v2&envId=vn57k9wr

2059. Minimum Operations to Convert Number

You are given a 0-indexed integer array nums containing distinct numbers, an integer start, and an integer goal. There is an integer x that is initially set to start, and you want to perform operations on x such that it is converted to goal. You can perform the following operation repeatedly on the number x:

If 0 <= x <= 1000, then for any index i in the array (0 <= i < nums.length), you can set x to any of the following:

- x + nums[i]
- x - nums[i]
- x ^ nums[i] (bitwise-XOR)

Note that you can use each nums[i] any number of times in any order. Operations that set x to be out of the range 0 <= x <= 1000 are valid, but no more operations can be done afterward.

Return the minimum number of operations needed to convert x = start into goal, and -1 if it is not possible.

Example 1:

Input: nums = [2,4,12], start = 2, goal = 12
Output: 2
Explanation: We can go from 2 → 14 → 12 with the following 2 operations.
- 2 + 12 = 14
- 14 - 2 = 12

Example 2:

Input: nums = [3,5,7], start = 0, goal = -4
Output: 2
Explanation: We can go from 0 → 3 → -4 with the following 2 operations.
- 0 + 3 = 3
- 3 - 7 = -4
Note that the last operation sets x out of the range 0 <= x <= 1000, which is valid.

Example 3:

Input: nums = [2,8,16], start = 0, goal = 1
Output: -1
Explanation: There is no way to convert 0 into 1.

Constraints:

    1 <= nums.length <= 1000
    -10^9 <= nums[i], goal <= 10^9
    0 <= start <= 1000
    start != goal
    All the integers in nums are distinct.
---
Learning

LEETCODE: Accepted (3689 ms, 191.3 MB)
"""


# mu 0.5
# def minimumOperations(nums: [int], start: int, goal: int) -> int
#   q = deque([start])
#   for (d, x) in levels(q, seen=set())
#     if x == goal
#       return d
#     if 0 <= x <= 1000
#       for n in nums
#         for op in [x + n, x - n, x ^ n]
#           q <- op
#   -1

def _holds(v, eq=None, lt=None, lte=None, gt=None, gte=None):
    return (
        (eq is None or v == eq)
        and (lt is None or v < lt)
        and (lte is None or v <= lte)
        and (gt is None or v > gt)
        and (gte is None or v >= gte)
    )


def levels(
    q, grid=None, seen=None, grouped=False, eq=None, lt=None, lte=None, gt=None, gte=None
):
    bare = eq is None and lt is None and lte is None and gt is None and gte is None
    row = list.__getitem__ if isinstance(grid, list) else lambda g, i: g[i]
    d = 0
    while q:
        level = []
        for _ in range(len(q)):
            x = q.popleft()
            if seen is not None and x in seen:
                continue
            if not bare:
                v = x if grid is None else row(grid, x[0])[x[1]]
                if not _holds(v, eq, lt, lte, gt, gte):
                    continue
            if seen is not None:
                seen.add(x)
            if grouped:
                level.append(x)
            else:
                yield d, x
        if grouped and level:
            yield d, level
        d += 1


class Solution:
    def minimumOperations(self, nums: list[int], start: int, goal: int) -> int:
        q = deque([start])
        for (d, x) in levels(q, seen=set()):
            if x == goal:
                return d
            if 0 <= x <= 1000:
                for n in nums:
                    for op in [x + n, x - n, x ^ n]:
                        q.append(op)
        return -1


sol = Solution()
print(sol.minimumOperations([2, 4, 12], 2, 12))
assert sol.minimumOperations([2, 4, 12], 2, 12) == 2
assert sol.minimumOperations([3, 5, 7], 0, -4) == 2
assert sol.minimumOperations([2, 8, 16], 0, 1) == -1
assert sol.minimumOperations([1], 0, 1000) == 1000
assert sol.minimumOperations([1000], 1000, 0) == 1
assert sol.minimumOperations([0], 500, 500) == 0
assert sol.minimumOperations([1, 2, 3], 0, -1000000000) == -1
assert sol.minimumOperations([1, 2, 3], 0, 1000000000) == -1
assert sol.minimumOperations([1, 1, 1], 0, 3) == 3
assert sol.minimumOperations([999], 0, 999) == 1
assert sol.minimumOperations([500, 500], 0, 1000) == 2
assert sol.minimumOperations([1, 2, 3], 1000, 0) == 334
assert sol.minimumOperations([10 ** 9], 0, 10 ** 9) == 1
assert sol.minimumOperations([-1, -2, -3], 0, -6) == 3
assert sol.minimumOperations([0, 1, 2], 0, 2) == 1
