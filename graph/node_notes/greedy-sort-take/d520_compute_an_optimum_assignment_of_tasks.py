# REFERENCE: d520 EPI 17.1 Compute an optimum assignment of tasks
class Solution:
    def optimum_task_assignment(self, task_durations):
        d = sorted(task_durations)
        return [(d[i], d[~i]) for i in range(len(d) // 2)]
