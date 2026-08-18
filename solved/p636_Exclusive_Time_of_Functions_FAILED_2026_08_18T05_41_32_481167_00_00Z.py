"""
URL: https://leetcode.com/problems/exclusive-time-of-functions/description/?envType=problem-list-v2&envId=vn57k9wr

636. Exclusive Time of Functions

On a single-threaded CPU, we execute a program containing n functions.
Each function has a unique ID between 0 and n - 1.

Function calls are stored in a call stack: when a function call starts,
its ID is pushed onto the stack, and when a function call ends, its ID
is popped off the stack. The function whose ID is at the top of the
stack is the current function being executed. Each time a function
starts or ends, we write a log with the ID, whether it started or
ended, and the timestamp.

You are given a list logs, where logs[i] represents the ith log message
formatted as a string "{function_id}:{"start" | "end"}:{timestamp}".
For example, "0:start:3" means a function call with function ID 0
started at the beginning of timestamp 3, and "1:end:2" means a function
call with function ID 1 ended at the end of timestamp 2. Note that a
function can be called multiple times, possibly recursively.

A function's exclusive time is the sum of execution times for all
function calls in the program. For example, if a function is called
twice, one call executing for 2 time units and another call executing
for 1 time unit, the exclusive time is 2 + 1 = 3.

Return the exclusive time of each function in an array, where the value
at the ith index represents the exclusive time for the function with
ID i.


Example 1:

Input: n = 2, logs = ["0:start:0","1:start:2","1:end:5","0:end:6"]
Output: [3,4]
Explanation:
Function 0 starts at the beginning of time 0, then it executes 2 for units of time and reaches the end of time 1.
Function 1 starts at the beginning of time 2, executes for 4 units of time, and ends at the end of time 5.
Function 0 resumes execution at the beginning of time 6 and executes for 1 unit of time.
So function 0 spends 2 + 1 = 3 units of total time executing, and function 1 spends 4 units of total time executing.

Example 2:

Input: n = 1, logs = ["0:start:0","0:start:2","0:end:5","0:start:6","0:end:6","0:end:7"]
Output: [8]
Explanation:
Function 0 starts at the beginning of time 0, executes for 2 units of time, and recursively calls itself.
Function 0 (recursive call) starts at the beginning of time 2 and executes for 4 units of time.
Function 0 (initial call) resumes execution then immediately calls itself again.
Function 0 (2nd recursive call) starts at the beginning of time 6 and executes for 1 unit of time.
Function 0 (initial call) resumes execution at the beginning of time 7 and executes for 1 unit of time.
So function 0 spends 2 + 4 + 1 + 1 = 8 units of total time executing.

Example 3:

Input: n = 2, logs = ["0:start:0","0:start:2","0:end:5","1:start:6","1:end:6","0:end:7"]
Output: [7,1]
Explanation:
Function 0 starts at the beginning of time 0, executes for 2 units of time, and recursively calls itself.
Function 0 (recursive call) starts at the beginning of time 2 and executes for 4 units of time.
Function 0 (initial call) resumes execution then immediately calls function 1.
Function 1 starts at the beginning of time 6, executes 1 unit of time, and ends at the end of time 6.
Function 0 resumes execution at the beginning of time 7 and executes for 1 unit of time.
So function 0 spends 2 + 4 + 1 = 7 units of total time executing, and function 1 spends 1 unit of total time executing.


Constraints:

    1 <= n <= 100
    2 <= logs.length <= 500
    0 <= function_id < n
    0 <= timestamp <= 10^9
    No two start events will happen at the same timestamp.
    No two end events will happen at the same timestamp.
    Each function has an "end" log for each "start" log.

    
---

"0:start:0","0:start:2","0:end:5","0:start:6","0:end:6","0:end:7"

0:                              6---6
0:           2-----------------5
0:  0--------                        -----7
0:  0.  1.   2.   3.   4.   5.  6.   7.   8.  

Embarrassing.

"""

class Solution:
    def exclusiveTime(self, n: int, logs: List[str]) -> List[int]:
        class Run:
            def __init__(self, id, start=None, end=None):
                self.id = id
                self.start = start
                self.end = end

            def __str__(self):
                return f'id: {self.id}, start={self.start}, end={self.end}'

            def __repr__(self):
                return str(self)

            def length(self):
                return self.end - self.start + 1

            def print(self):
                print(f"{self.id}: {' '*5* self.start}{self.start}{'-'*max(self.length()*5, 5)}{self.end}")

        stack = []
        events = []
        for log in logs:
            id, event, ts = log.split(':')
            id, ts = int(id), int(ts)
            if event == 'start':
                stack.append(Run(id, start=ts, end=None))
            if event == 'end':
                last = stack.pop()
                last.end = ts
                events.append(last)
        
        events.sort(key=lambda x: x.start)
        eventsLengths = defaultdict(dict)
        for e in events[::-1]:
            if e.id not in eventsLengths:
                eventsLengths[e.id] = {'total': 0}
            eventsLengths[e.id]['total'] += e.length()
            e.print()

        while events:
            event = events.pop()
            parent = events[-1] if events else None
            if parent and parent.end > event.start:
                eventsLengths[parent.id]['total'] -= event.length()

        print(eventsLengths)
        return [*sorted([e['total'] for e in eventsLengths.values()])]



sol = Solution()

# print(sol.exclusiveTime(2, ["0:start:0","0:start:2","0:end:5","1:start:6","1:end:6","0:end:7"])) # 7, 1
print(sol.exclusiveTime(2, ["0:start:0", "1:start:2", "1:end:5", "0:end:6"]))  # [3, 4]

assert sol.exclusiveTime(2, ["0:start:0", "1:start:2", "1:end:5", "0:end:6"]) == [3, 4]
assert sol.exclusiveTime(1, ["0:start:0", "0:start:2", "0:end:5", "0:start:6", "0:end:6", "0:end:7"]) == [8]
assert sol.exclusiveTime(2, ["0:start:0", "0:start:2", "0:end:5", "1:start:6", "1:end:6", "0:end:7"]) == [7, 1]
assert sol.exclusiveTime(1, ["0:start:0", "0:end:0"]) == [1]
assert sol.exclusiveTime(1, ["0:start:5", "0:end:9"]) == [5]
assert sol.exclusiveTime(2, ["0:start:0", "0:end:1", "1:start:5", "1:end:6"]) == [2, 2]
assert sol.exclusiveTime(3, ["0:start:0", "0:end:1"]) == [2, 0, 0]
assert sol.exclusiveTime(3, ["0:start:0", "1:start:1", "2:start:2", "2:end:3", "1:end:4", "0:end:5"]) == [2, 2, 2]
assert sol.exclusiveTime(2, ["0:start:0", "1:start:1", "1:end:2", "1:start:3", "1:end:4", "0:end:5"]) == [2, 4]
assert sol.exclusiveTime(2, ["0:start:0", "1:start:3", "1:end:3", "0:end:10"]) == [10, 1]
assert sol.exclusiveTime(1, ["0:start:1000000000", "0:end:1000000000"]) == [1]
assert sol.exclusiveTime(2, ["1:start:0", "1:end:1", "0:start:2", "0:end:3"]) == [2, 2]
assert sol.exclusiveTime(1, ["0:start:0", "0:start:1", "0:start:2", "0:end:3", "0:end:4", "0:end:5"]) == [6]

# FAILED: walked away after 63m 20s; no working solution.
# Judge the moves actually attempted as struggled, not clean.
