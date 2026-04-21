"""
URL: https://leetcode.com/problems/first-unique-character-in-a-string/description/?envType=problem-list-v2&envId=vn57k9wr

387. First Unique Character in a String

Given a string s, find the first non-repeating character in it and return its
index. If it does not exist, return -1.


Example 1:

Input: s = "leetcode"
Output: 0
Explanation: The character 'l' at index 0 is the first character that does not
occur at any other index.

Example 2:

Input: s = "loveleetcode"
Output: 2

Example 3:

Input: s = "aabb"
Output: -1


Constraints:

    1 <= s.length <= 10^5
    s consists of only lowercase English letters.
"""


class Solution:
    def firstUniqChar(self, s: str) -> int:
        counts = Counter(s)
        for pos, letter in enumerate(s):
            count = counts[letter]
            if count == 1:
                return pos
        return -1


sol = Solution()

# print(sol.firstUniqChar("aabbc"))  # 0

assert sol.firstUniqChar("leetcode") == 0
assert sol.firstUniqChar("loveleetcode") == 2
assert sol.firstUniqChar("aabb") == -1
assert sol.firstUniqChar("a") == 0
assert sol.firstUniqChar("aa") == -1
assert sol.firstUniqChar("ab") == 0
assert sol.firstUniqChar("aabbc") == 4
assert sol.firstUniqChar("aabbcc") == -1
assert sol.firstUniqChar("abcabc") == -1
assert sol.firstUniqChar("abcdef") == 0
assert sol.firstUniqChar("aabbccddeeffg") == 12
assert sol.firstUniqChar("z") == 0
assert sol.firstUniqChar("zz") == -1
assert sol.firstUniqChar("dddccdbba") == 8
assert sol.firstUniqChar("aabbccd") == 6
assert sol.firstUniqChar("a" * 100000) == -1
assert sol.firstUniqChar("a" * 99999 + "b") == 99999