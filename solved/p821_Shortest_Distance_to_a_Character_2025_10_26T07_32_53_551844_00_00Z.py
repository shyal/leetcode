from typing import List

"""
URL: https://leetcode.com/problems/shortest-distance-to-a-character/description/?envType=problem-list-v2&envId=vn57k9wr

821. Shortest Distance to a Character

Given a string s and a character c that occurs in s, return an array of integers answer where answer.length == s.length and answer[i] is the distance from index i to the closest occurrence of character c in s.

The distance between two indices i and j is abs(i - j), where abs is the absolute value function.

Example 1:

Input: s = "loveleetcode", c = "e"
Output: [3,2,1,0,1,0,0,1,2,2,1,0]
Explanation: The character 'e' appears at indices 3, 5, 6, and 11 (0-indexed).
The closest occurrence of 'e' for index 0 is at index 3, so the distance is abs(0 - 3) = 3.
The closest occurrence of 'e' for index 1 is at index 3, so the distance is abs(1 - 3) = 2.
For index 4, there is a tie between the 'e' at index 3 and the 'e' at index 5, but the distance is still the same: abs(4 - 3) == abs(4 - 5) = 1.
The closest occurrence of 'e' for index 8 is at index 6, so the distance is abs(8 - 6) = 2.

Example 2:

Input: s = "aaab", c = "b"
Output: [3,2,1,0]

Constraints:

    1 <= s.length <= 10^4
    s[i] and c are lowercase English letters.
    It is guaranteed that c occurs at least once in s.
"""


class Solution:
    def shortestToChar(self, s: str, c: str) -> List[int]:
        last_pos_left = None
        last_pos_right = None
        res = []
        for i in range(len(s)):
            if s[i] == c:
                last_pos_left = i
            dist_from_left = i - last_pos_left if last_pos_left is not None else maxsize
            res.append(dist_from_left)

        for i in range(len(s) - 1, -1, -1):
            if s[i] == c:
                last_pos_right = i
            dist_from_right = (
                last_pos_right - i if last_pos_right is not None else maxsize
            )
            res[i] = min(res[i], dist_from_right)

        return res


sol = Solution()

# print(sol.shortestToChar("loveleetcode", "e"))  # [3,2,1,0,1,0,0,1,2,2,1,0]

assert sol.shortestToChar("loveleetcode", "e") == [3, 2, 1, 0, 1, 0, 0, 1, 2, 2, 1, 0]
assert sol.shortestToChar("aaab", "b") == [3, 2, 1, 0]
assert sol.shortestToChar("a", "a") == [0]
assert sol.shortestToChar("ab", "a") == [0, 1]
assert sol.shortestToChar("ba", "a") == [1, 0]
assert sol.shortestToChar("aaa", "a") == [0, 0, 0]
assert sol.shortestToChar("abcda", "a") == [0, 1, 2, 1, 0]
assert sol.shortestToChar("abcde", "c") == [2, 1, 0, 1, 2]
assert sol.shortestToChar("aaba", "a") == [0, 0, 1, 0]
