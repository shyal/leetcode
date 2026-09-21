"""
URL: https://leetcode.com/problems/task-scheduler/description/?envType=problem-list-v2&envId=vn57k9wr

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

    1 <= tasks.length <= 10^4
    tasks[i] is an uppercase English letter.
    0 <= n <= 100

---

Hmm doesn't seem so complex at first, but with the rating it probably is.

Tasks _can_ be completed in any order, but clearly the cooling is
the primary constraint.

We probably need a mechanism that fetches which tasks can be run.
It would track the next available time at which a task is available..

maybe a heap?



class Solution:
    def leastInterval(self, tasks: List[str], n: int) -> int:
        c = Counter(tasks)
        h = [[-1, v, k] for k, v in c.items()]
        heapify(h)
        res = []
        time = 0
        while h:
            next_time = h[0][0]
            if next_time <= time:
                next_time, count, p = heappop(h)
                res.append(p)
                count -= 1
                if count > 0:
                    heappush(h, [time + n + 1, count, p])
            else:
                res.append("pause")
            time += 1
        print(res)
        return time


This fails a couple of cases.. we need a round robin,
which is needs a special value in the heap to push it
back, or a deque. If we use a deque, we don't need a heap,
just a dict to track the count and the next available time.

So with this:

["Z", "Z", "Z", "Y", "Y", "X", "X", "X", "X"], 2

the heap gives ups:

['Y', 'Z', 'X', 'Y', 'Z', 'X', 'pause', 'Z', 'X', 'pause', 'pause', 'X']

we clearly have 2 pauses too many, so how would we get rid of them:

X Y Z X Y

Ah we should use the most numerous item first?

So that implies a putting the count first.. ok or flipping the count to negative.


Nope we fail on this:

input ["B","C","D","A","A","A","A","G"] 1
expected 8

I give up.

LEETCODE: Wrong Answer (61/72 cases)
"""


class Solution:
    def leastInterval(self, tasks: List[str], n: int) -> int:
        c = Counter(tasks)
        h = [[0, -v, k] for k, v in c.items()]
        heapify(h)
        res = []
        time = 0

        while h:
            next_time = h[0][0]
            if next_time <= time:
                next_time, count, p = heappop(h)
                count = -count
                res.append(p)
                count -= 1
                if count > 0:
                    heappush(h, [time + n + 1, -count, p])
            else:
                res.append("pause")
            time += 1
        print(res)
        return time


sol = Solution()


print(sol.leastInterval(["B", "C", "D", "A", "A", "A", "A", "G"], 1))  # 8
# assert  == 10


print(sol.leastInterval(["A", "A", "A", "B", "B", "B"], 2))  # 8

assert sol.leastInterval(["A", "A", "A", "B", "B", "B"], 2) == 8
assert sol.leastInterval(["A", "C", "A", "B", "D", "B"], 1) == 6
assert sol.leastInterval(["A", "A", "A", "B", "B", "B"], 3) == 10

assert sol.leastInterval(["A"], 0) == 1
assert sol.leastInterval(["A"], 10) == 1
assert sol.leastInterval(["A", "A", "A", "A", "A"], 0) == 5
assert sol.leastInterval(["A", "A", "A", "A", "A"], 4) == 21
assert sol.leastInterval(["A", "B", "C", "D", "E", "F", "G"], 2) == 7
assert sol.leastInterval(["A", "A", "B", "B", "C", "C", "D", "D"], 1) == 8
# assert sol.leastInterval(["A"] * 10000, 100) == 1009900
# assert (
#     sol.leastInterval(["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"] * 1000, 5)
#     == 10000
# )
assert sol.leastInterval(["A", "A", "B", "B", "C", "C", "D", "D", "E", "E"], 0) == 10
assert sol.leastInterval(["A", "B", "A", "B", "A", "B", "A", "B"], 3) == 14
assert (
    sol.leastInterval(
        [
            "A",
            "B",
            "C",
            "D",
            "E",
            "F",
            "G",
            "H",
            "I",
            "J",
            "K",
            "L",
            "M",
            "N",
            "O",
            "P",
            "Q",
            "R",
            "S",
            "T",
            "U",
            "V",
            "W",
            "X",
            "Y",
            "Z",
        ],
        25,
    )
    == 26
)
