"""
URL: https://leetcode.com/problems/crawler-log-folder/description/?envType=problem-list-v2&envId=vn57k9wr

1598. Crawler Log Folder

The Leetcode file system keeps a log each time some user performs a change folder operation.

The operations are described below:

- "../" : Move to the parent folder of the current folder. (If you are already in the main folder, remain in the same folder).

- "./" : Remain in the same folder.

- "x/" : Move to the child folder named x (This folder is guaranteed to always exist).

You are given a list of strings logs where logs[i] is the operation performed by the user at the i-th step.

The file system starts in the main folder, then the operations in logs are performed.

Return the minimum number of operations needed to go back to the main folder after the change folder operations.

Example 1:

Input: logs = ["d1/","d2/","../","d21/","./"]
Output: 2
Explanation: Use this change folder operation "../" 2 times and go back to the main folder.

Example 2:

Input: logs = ["d1/","d2/","./","d3/","../","d31/"]
Output: 3

Example 3:

Input: logs = ["d1/","../","../","../"]
Output: 0

Constraints:

- 1 <= logs.length <= 10^3
- 2 <= logs[i].length <= 10
- logs[i] contains lowercase English letters, digits, '.', and '/'.
- logs[i] follows the format described in the statement.
- Folder names consist of lowercase English letters and digits.
"""


class Solution:
    def minOperations(self, logs: List[str]) -> int:
        curr = []
        for l in logs:
            if l == "../":
                if curr:
                    curr.pop()
                else:
                    pass
            elif l == "./":
                pass
            else:
                curr.append(l)
        return len(curr)


sol = Solution()

# print(sol.minOperations(["d1/", "d2/", "../", "d21/", "./"]))  # 2

assert sol.minOperations(["d1/", "d2/", "../", "d21/", "./"]) == 2
assert sol.minOperations(["d1/", "d2/", "./", "d3/", "../", "d31/"]) == 3
assert sol.minOperations(["d1/", "../", "../", "../"]) == 0
assert sol.minOperations(["../"]) == 0
assert sol.minOperations(["./"]) == 0
assert sol.minOperations(["a/"]) == 1
assert sol.minOperations(["a/", "../"]) == 0
assert sol.minOperations(["a/", "../", "../"]) == 0
assert sol.minOperations(["a/", "b/", "c/", "../", "../"]) == 1
assert sol.minOperations(["./", "./", "./"]) == 0
assert (
    sol.minOperations(
        ["d1/", "d2/", "./", "d3/", "../", "d31/", "../", "../", "../", "../"]
    )
    == 0
)
assert sol.minOperations(["a1b2/"]) == 1
assert sol.minOperations(["1a/", "../"]) == 0
assert (
    sol.minOperations(["d1/", "d2/", "d3/", "d4/", "../", "../", "../", "../", "../"])
    == 0
)
assert sol.minOperations(["d1/", "./", "../", "./", "d2/"]) == 1
