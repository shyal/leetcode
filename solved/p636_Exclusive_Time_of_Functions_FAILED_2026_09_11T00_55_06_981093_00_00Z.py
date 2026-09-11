"""
URL: https://leetcode.com/problems/exclusive-time-of-functions/description/?envType=problem-list-v2&envId=vn57k9wr

636. Exclusive Time of Functions

On a single-threaded CPU, we execute a program containing n functions. Each function has a unique ID between 0 and n - 1.

Function calls are stored in a call stack: when a function call starts, its ID is pushed onto the stack, and when a function call ends, its ID is popped off the stack. The function whose ID is at the top of the stack is the current function being executed. Each time a function starts or ends, we write a log with the ID, whether it started or ended, and the timestamp.

You are given a list logs, where logs[i] represents the i-th log message formatted as a string "{function_id}:{start|end}:{timestamp}". For example, "0:start:3" means a function call with function ID 0 started at the beginning of timestamp 3, and "1:end:2" means a function call with function ID 1 ended at the end of timestamp 2. Note that a function can be called multiple times, possibly recursively.

A function's exclusive time is the sum of execution times for all function calls in the program. For example, if a function is called twice, one call executing for 2 time units and another call executing for 1 time unit, the exclusive time is 2 + 1 = 3.

Return the exclusive time of each function in an array, where the value at the i-th index represents the exclusive time for the function with ID i.

Example 1:

Input: n = 2, logs = ["0:start:0","1:start:2","1:end:5","0:end:6"]
Output: [3,4]
Explanation:
Function 0 starts at the beginning of time 0, then it executes 2 for units of time and reaches the end of time 1.
Function 1 starts at the beginning of time 2, executes for 4 units of time, and ends at the end of time 5.
Function 0 resumes execution at the beginning of time 6 and executes for 1 unit of time.
So function 0 spends 2 + 1 = 3 units of total time executing, and function 1 spends 4 units of total time executing.

    time   0 1 2 3 4 5 6
    fn 0   # # . . . . #    2 + 1 = 3
    fn 1   . . # # # # .    4

    # = running, . = paused or not on the stack

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

    time        0 1 2 3 4 5 6 7
    fn 0 (1st)  # # . . . . . #    2 + 1
    fn 0 (2nd)  . . # # # # . .    4
    fn 0 (3rd)  . . . . . . # .    1
                                   total 8

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

    time        0 1 2 3 4 5 6 7
    fn 0 (1st)  # # . . . . . #    2 + 1
    fn 0 (2nd)  . . # # # # . .    4
    fn 1        . . . . . . # .    1

Constraints:

    1 <= n <= 100
    2 <= logs.length <= 500
    0 <= function_id < n
    0 <= timestamp <= 10^9
    No two start events will happen at the same timestamp.
    No two end events will happen at the same timestamp.
    Each function has an "end" log for each "start" log.
"""

# time   0 1 2 3 4 5 6
# fn 0   # # . . . . #    2 + 1 = 3
# fn 1   . . # # # # .    4


class Solution:
    def exclusiveTime(self, n: int, logs: List[str]) -> List[int]:
        stack = []
        funcs = defaultdict(int)

        for log in logs:
            id, mode, time = log.split(":")
            id = int(id)
            time = int(time)

            if mode == "start":
                if stack:
                    stack[-1]["end"] = time
                stack.append(
                    dict(id=id, mode=mode, time=time, end=0, start=time, total_time=0)
                )
            elif mode == "end":
                curr = stack.pop()
                if stack:
                    stack[-1]["total_time"] += curr["end"] - curr["start"]
                else:
                    print(curr)

        print(stack)


sol = Solution()

print(sol.exclusiveTime(2, ["0:start:0", "1:start:2", "1:end:5", "0:end:6"]))  # [3,4]

# assert sol.exclusiveTime(2, ["0:start:0", "1:start:2", "1:end:5", "0:end:6"]) == [3, 4]
# assert sol.exclusiveTime(
#     1, ["0:start:0", "0:start:2", "0:end:5", "0:start:6", "0:end:6", "0:end:7"]
# ) == [8]
# assert sol.exclusiveTime(
#     2, ["0:start:0", "0:start:2", "0:end:5", "1:start:6", "1:end:6", "0:end:7"]
# ) == [7, 1]

# assert sol.exclusiveTime(1, ["0:start:0", "0:end:0"]) == [1]
# assert sol.exclusiveTime(1, ["0:start:0", "0:end:1000000000"]) == [1000000001]
# assert sol.exclusiveTime(
#     3, ["0:start:0", "1:start:1", "1:end:2", "2:start:3", "2:end:4", "0:end:5"]
# ) == [2, 2, 2]
# assert sol.exclusiveTime(2, ["0:start:0", "0:start:1", "0:end:2", "0:end:3"]) == [4, 0]
# assert sol.exclusiveTime(2, ["0:start:0", "1:start:1", "1:end:1", "0:end:2"]) == [2, 1]
# assert sol.exclusiveTime(2, ["0:start:0", "1:start:1", "1:end:2", "0:end:3"]) == [2, 2]
# assert sol.exclusiveTime(
#     3, ["0:start:0", "1:start:1", "1:end:1", "2:start:2", "2:end:2", "0:end:3"]
# ) == [2, 1, 1]
# assert sol.exclusiveTime(
#     2, ["0:start:0", "0:start:1", "1:start:2", "1:end:3", "0:end:4", "0:end:5"]
# ) == [4, 2]
# assert sol.exclusiveTime(
#     1, ["0:start:0", "0:start:1", "0:start:2", "0:end:3", "0:end:4", "0:end:5"]
# ) == [6]
# assert sol.exclusiveTime(2, ["0:start:0", "1:start:2", "1:end:2", "0:end:3"]) == [3, 1]
# assert sol.exclusiveTime(2, ["0:start:0", "0:end:0", "1:start:1", "1:end:1"]) == [1, 1]
# assert sol.exclusiveTime(1, ["0:start:0", "0:end:0", "0:start:1", "0:end:1"]) == [2]


# FAILED: walked away after 38m 40s; no working solution.
# Judge the moves actually attempted as struggled, not clean.
