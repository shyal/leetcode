"""
URL: https://leetcode.com/problems/find-the-k-th-character-in-string-game-i/description/?envType=problem-list-v2&envId=game

3304. Find the K-th Character in String Game I

Alice is playing a game to construct a string. The string starts as "a". In each step, Alice takes the current string S, creates a new string T by incrementing each character in S by 1 (where 'z' wraps around to 'a'), and appends T to S.

The process continues indefinitely, creating an infinite string in the limit. Given an integer k, return the k-th (1-indexed) character in this infinite string.


Example 1:

Input: k = 5
Output: "b"
Explanation:
- "a"
- "ab"
- "abbc"
- "abbcbccd"
The 5th character is 'b'.

Example 2:

Input: k = 10
Output: "c"
Explanation:
Continuing the process, the string becomes "abbcbccdbccdcdde" at the next step, and the 10th character is 'c'.


Constraints:

    1 <= k <= 500
"""


class Solution:
    def kthCharacter(self, k: int) -> str:
        L = ascii_letters
        pos = {v: i for i, v in enumerate(L)}
        S = "a"
        for _ in range(10):
            T = "".join(L[(pos[x] + 1) % 26] for x in S)
            S += T
        return S[k - 1]


sol = Solution()

# print(sol.kthCharacter(500))  # 'b'

assert sol.kthCharacter(5) == "b"
assert sol.kthCharacter(10) == "c"
assert sol.kthCharacter(1) == "a"
assert sol.kthCharacter(2) == "b"
assert sol.kthCharacter(3) == "b"
assert sol.kthCharacter(4) == "c"
assert sol.kthCharacter(8) == "d"
assert sol.kthCharacter(9) == "b"
assert sol.kthCharacter(16) == "e"
