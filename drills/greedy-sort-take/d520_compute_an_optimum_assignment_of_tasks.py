"""
EPI 17.1 Compute an optimum assignment of tasks

Given a list task_durations of even length, return a list of pairs (a, b)
that uses each duration exactly once and makes the largest pair sum a + b
as small as possible. Each pair is the two tasks of one worker, and a + b
is the time that worker needs.

Example 1:

Input: task_durations = [3, 8, 1, 6, 5, 2]
Output: [(1, 8), (2, 6), (3, 5)]
Explanation: the pair sums are 9, 8 and 8, so the largest is 9. The
pairs (1, 2), (3, 5), (6, 8) give a largest sum of 14.

Example 2:

Input: task_durations = [7, 7]
Output: [(7, 7)]

Example 3:

Input: task_durations = []
Output: []

Constraints:

    0 <= len(task_durations) <= 10^5, and len(task_durations) is even.
    1 <= task_durations[i] <= 10^9
    Any list of pairs with the smallest largest sum is correct, in any order.

    REQUIRED: O(n log n) time for n tasks.
"""


class Solution:
    def optimum_task_assignment(self, task_durations: list[int]) -> list[tuple[int, int]]:
        pass


sol = Solution()

print(sol.optimum_task_assignment([3, 8, 1, 6, 5, 2]))  # [(1, 8), (2, 6), (3, 5)]

# check = lambda A, best: (r := sol.optimum_task_assignment(A[:])) is not None and all(len(p) == 2 for p in r) and sorted(x for p in r for x in p) == sorted(A) and max((a + b for a, b in r), default=0) == best
# assert check([3, 8, 1, 6, 5, 2], 9)
# assert check([7, 7], 14)
# assert check([], 0)
# assert check([1, 2, 3, 4], 5)
# assert check([5, 1, 9, 2, 8, 3, 7, 4], 10)
# assert check([10, 1, 1, 1], 11)
# assert check([4, 4, 4, 4], 8)
# assert check([1, 1000000000], 1000000001)
# assert check([1, 2, 3, 4, 5, 6, 7, 100], 101)
# assert check([9, 9, 1, 1, 5, 5], 10)
# assert check([2, 3], 5)
# assert check(list(range(1, 100001)), 100001)
# assert check(list(range(100000, 0, -1)), 100001)
# assert check([i % 1000 + 1 for i in range(100000)], 1001)
# assert check([1] * 99998 + [10**9, 10**9], 10**9 + 1)
