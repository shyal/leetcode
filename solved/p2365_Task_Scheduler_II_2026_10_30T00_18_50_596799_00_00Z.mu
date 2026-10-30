# URL: https://leetcode.com/problems/task-scheduler-ii/description/?envType=problem-list-v2&envId=vn57k9wr
#
# 2365. Task Scheduler II
#
# You are given a 0-indexed array of positive integers tasks, representing tasks that need to be completed in order, where tasks[i] represents the type of the iᵗʰ task.
#
# You are also given a positive integer space, which represents the minimum number of days that must pass after the completion of a task before another task of the same type can be performed.
#
# Each day, until all tasks have been completed, you must either:
# - Complete the next task from tasks, or
# - Take a break.
#
# Return the minimum number of days needed to complete all tasks.
#
# Example 1:
#
# Input: tasks = [1,2,1,2,3,1], space = 3
# Output: 9
# Explanation:
# One way to complete all tasks in 9 days is as follows:
# Day 1: Complete the 0th task.
# Day 2: Complete the 1st task.
# Day 3: Take a break.
# Day 4: Take a break.
# Day 5: Complete the 2nd task.
# Day 6: Complete the 3rd task.
# Day 7: Take a break.
# Day 8: Complete the 4th task.
# Day 9: Complete the 5th task.
# It can be shown that the tasks cannot be completed in less than 9 days.
#
# Example 2:
#
# Input: tasks = [5,8,8,5], space = 2
# Output: 6
# Explanation:
# One way to complete all tasks in 6 days is as follows:
# Day 1: Complete the 0th task.
# Day 2: Complete the 1st task.
# Day 3: Take a break.
# Day 4: Take a break.
# Day 5: Complete the 2nd task.
# Day 6: Complete the 3rd task.
# It can be shown that the tasks cannot be completed in less than 6 days.
#
# Constraints:
#
#     1 <= tasks.length <= 10^5
#     1 <= tasks[i] <= 10^9
#     1 <= space <= tasks.length
#
# ---
# 
# 
#   1 2     1 2 3   1
# 1   - - -   - - -
# 2     - - -   - - -
# t 1 2 3 4 5 6 7 8 9
# LEETCODE: Accepted (118 ms, 39.5 MB)

# mu 0.14

class Solution
  def taskSchedulerII(tasks: [int], space: int) -> int
    next_run = {}
    t = 0
    tasks = deque(tasks)
    while tasks
      curr = tasks.popleft()
      if curr in next_run
        wait = next_run[curr] - t
        if wait > 0
          t += wait + 1
        else
          t += 1
      else
        t += 1
      next_run[curr] = t + space
    t



sol = Solution()


print(sol.taskSchedulerII([5, 8, 8, 5], 2)) # 6


# print(sol.taskSchedulerII([1, 2, 1, 2, 3, 1], 3))  # 9

assert sol.taskSchedulerII([1, 2, 1, 2, 3, 1], 3) == 9
assert sol.taskSchedulerII([5, 8, 8, 5], 2) == 6
assert sol.taskSchedulerII([1], 1) == 1
assert sol.taskSchedulerII([1, 1, 1, 1], 1) == 7
assert sol.taskSchedulerII([1, 1, 1, 1], 0) == 4
assert sol.taskSchedulerII([1, 2, 3, 4, 5], 1) == 5
assert sol.taskSchedulerII([1, 2, 3, 1, 2, 3], 2) == 6
assert sol.taskSchedulerII([10 ** 9, 10 ** 9, 10 ** 9], 1) == 5
assert sol.taskSchedulerII([1] * 100000, 99999) == 9999900001
assert sol.taskSchedulerII([i for i in 1..<100001], 1) == 100000
assert sol.taskSchedulerII([1, 2, 1, 2, 1, 2, 1, 2], 3) == 14
assert sol.taskSchedulerII([2, 2, 2, 2, 2], 4) == 21
assert sol.taskSchedulerII([1, 2, 3, 4, 5, 1, 2, 3, 4, 5], 5) == 11
assert sol.taskSchedulerII([1, 1, 2, 2, 3, 3, 4, 4, 5, 5], 0) == 10
