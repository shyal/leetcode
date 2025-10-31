"""
URL: https://leetcode.com/problems/minimum-number-of-chairs-in-a-waiting-room/description/?envType=problem-list-v2&envId=vn57k9wr

3168. Minimum Number of Chairs in a Waiting Room

You are given a string s. Simulate events at each second i:

- If s[i] == 'E', a person enters the waiting room and takes one of the chairs in it.
- If s[i] == 'L', a person leaves the waiting room, freeing up a chair.

Return the minimum number of chairs needed so that a chair is available for every person who enters the waiting room given that it is initially empty.

Example 1:

Input: s = "EEEEEEE"

Output: 7

Explanation:

After each second, a person enters the waiting room and no person leaves it. Therefore, a minimum of 7 chairs is needed.

Example 2:

Input: s = "ELELEEL"

Output: 2

Explanation:

Let's consider that there are 2 chairs in the waiting room. The table below shows the state of the waiting room at each second.

Second | Event | People in the Waiting Room | Available Chairs
0 | Enter | 1 | 1
1 | Leave | 0 | 2
2 | Enter | 1 | 1
3 | Leave | 0 | 2
4 | Enter | 1 | 1
5 | Enter | 2 | 0
6 | Leave | 1 | 1

Example 3:

Input: s = "ELEELEELLL"

Output: 3

Explanation:

Let's consider that there are 3 chairs in the waiting room. The table below shows the state of the waiting room at each second.

Second | Event | People in the Waiting Room | Available Chairs
0 | Enter | 1 | 2
1 | Leave | 0 | 3
2 | Enter | 1 | 2
3 | Enter | 2 | 1
4 | Leave | 1 | 2
5 | Enter | 2 | 1
6 | Enter | 3 | 0
7 | Leave | 2 | 1
8 | Leave | 1 | 2
9 | Leave | 0 | 3

Constraints:

- 1 <= s.length <= 50
- s consists only of the letters 'E' and 'L'.
- s represents a valid sequence of entries and exits.
"""


class Solution:
    def minimumChairs(self, s: str) -> int:
        chairs = 0
        max_needed = 0
        for e in s:
            if e == "E":
                chairs += 1
            else:
                chairs -= 1
            max_needed = max(max_needed, chairs)
        return max_needed


sol = Solution()

# print(sol.minimumChairs("EEEEEEE"))  # 7

assert sol.minimumChairs("EEEEEEE") == 7
assert sol.minimumChairs("ELELEEL") == 2
assert sol.minimumChairs("ELEELEELLL") == 3
assert sol.minimumChairs("E") == 1
assert sol.minimumChairs("L") == 0
assert sol.minimumChairs("LE") == 0
assert sol.minimumChairs("EL") == 1
assert sol.minimumChairs("LLE") == 0
assert sol.minimumChairs("EEELLLEE") == 3
assert sol.minimumChairs("ELELEL") == 1
