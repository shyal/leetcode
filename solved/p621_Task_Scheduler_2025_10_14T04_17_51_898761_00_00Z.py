"""
URL: https://leetcode.com/problems/task-scheduler/description/

621. Task Scheduler

You are given an array of CPU tasks, each labeled with a letter from A to Z, and a number n. Each CPU interval can be idle or allow the completion of one task. Tasks can be completed in any order, but there's a constraint: there has to be a gap of at least n intervals between two tasks with the same label.

Return the minimum number of CPU intervals required to complete all tasks.


Example 1:

Input: tasks = ["A","A","A","B","B","B"], n = 2

Output: 8

Explanation: A possible sequence is: A -> B -> idle -> A -> B -> idle -> A -> B.

After completing task A, you must wait two intervals before doing A again. The same applies to task B. In the 3rd interval, neither A nor B can be done, so you idle. By the 4th interval, you can do A again as 2 intervals have passed.

Example 2:

Input: tasks = ["A","C","A","B","D","B"], n = 1

Output: 6

Explanation: A possible sequence is: A -> B -> C -> D -> A -> B.

With a cooling interval of 1, you can repeat a task after just one other task.

Example 3:

Input: tasks = ["A","A","A", "B","B","B"], n = 3

Output: 10

Explanation: A possible sequence is: A -> B -> idle -> idle -> A -> B -> idle -> idle -> A -> B.

There are only two types of tasks, A and B, which need to be separated by 3 intervals. This leads to idling twice between repetitions of these tasks.


Constraints:

        1 <= tasks.length <= 104
        tasks[i] is an uppercase English letter.
        0 <= n <= 100
---

Alright so i guess we need to put the counts on a min heap, containing the (cooloff, count, char).
The cooloff is when we'll be able to use the task next (i.e current time + n).
So we pop the min from the heap, use it, decrement it, and increment its cooloff.
Then the next task available will have the smallest cooloff period.
If no task is available, we add a count of one to the time taken.

Hmm i got close. But not all tests are passing. So i'll look at the solution.

"""


class Solution:
    def leastInterval(self, tasks: List[str], n: int) -> int:
        # Not my solution
        if not tasks:
            return 0
        freq = Counter(tasks)
        max_heap = [-count for count in freq.values()]
        heapify(max_heap)
        time = 0
        cooldown = deque()
        while max_heap or cooldown:
            time += 1
            while cooldown and cooldown[0][0] <= time:
                heappush(max_heap, cooldown.popleft()[1])
            if max_heap:
                remaining = heappop(max_heap) + 1
                if remaining:
                    cooldown.append((time + n + 1, remaining))
        return time


sol = Solution()


res = sol.leastInterval(tasks=["B", "C", "D", "A", "A", "A", "A", "G"], n=1)
print(res)
assert res == 8

res = sol.leastInterval(tasks=["A", "A", "A", "B", "B", "B"], n=2)
assert res == 8

res = sol.leastInterval(tasks=["A", "C", "A", "B", "D", "B"], n=1)
assert res == 6

res = sol.leastInterval(tasks=["A", "A", "A", "B", "B", "B"], n=3)
assert res == 10

res = sol.leastInterval(tasks=["A"], n=0)
assert res == 1

res = sol.leastInterval(tasks=["A"], n=5)
assert res == 1

res = sol.leastInterval(tasks=["A", "A"], n=0)
assert res == 2

res = sol.leastInterval(tasks=["A", "A"], n=1)
assert res == 3

res = sol.leastInterval(tasks=["A", "A", "A", "A"], n=2)
assert res == 10

res = sol.leastInterval(tasks=["A", "A", "A", "B", "B", "B", "C", "C", "C"], n=2)
assert res == 9

res = sol.leastInterval(tasks=["A", "A", "A", "B", "B", "B", "C", "C", "C"], n=3)
assert res == 11

res = sol.leastInterval(tasks=["A", "B", "C", "D", "E", "F"], n=10)
assert res == 6

res = sol.leastInterval(tasks=["A", "A", "A", "A", "A", "B"], n=1)
assert res == 9

res = sol.leastInterval(tasks=["A", "A", "A"], n=0)
assert res == 3

res = sol.leastInterval(tasks=["A", "B"], n=100)
assert res == 2

res = sol.leastInterval(tasks=["A", "A"], n=100)
assert res == 102
