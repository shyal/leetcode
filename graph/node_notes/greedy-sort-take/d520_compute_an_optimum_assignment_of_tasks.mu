# REFERENCE: d520 EPI 17.1 Compute an optimum assignment of tasks
class Solution
  def optimum_task_assignment(task_durations: [int]) -> [(int, int)]
    d = sort task_durations
    [(d[i], d[-1 - i]) for i in 0..<len(d) // 2]
