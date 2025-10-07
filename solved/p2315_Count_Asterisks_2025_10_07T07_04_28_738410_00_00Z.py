"""
URL: https://leetcode.com/problems/count-asterisks/description/

2315. Count Asterisks

You are given a string s, which contains stars *.

In one operation, you can:

    Choose a star in s.
    Remove the closest non-star character to its left, as well as remove the star itself.

Return the string after all stars have been removed.

Note:

    The input will be generated such that the operation is always possible.
    It can be shown that the resulting string will always be unique.


Example 1:

Input: s = "l|*e*et|c**o|*de|"
Output: 2
Explanation: The considered asterisks are bold below.
- l|*e*et|c**o|*de|
The asterisks in indices 1, 3, 9, 10, and 11 are outside the bars.

No, wait. Actually the problem is to count asterisks that are not between two vertical bars.

More precisely, count * not in any pair of |...|.

Example 2:

Input: s = "iamprogrammer"
Output: 0
Explanation: There are no asterisks.

Example 3:

Input: s = "yo|uar|e**|b|e***au|tifu|l"
Output: 5
Explanation: The considered asterisks are bold below.
yo|uar|e**|b|e***au|tifu|l

Constraints:

    1 <= s.length <= 1000
    s consists of lowercase English letters, vertical bars '|', and asterisks '*'.
    The number of vertical bars '|' is even.
"""


class Solution:
    def countAsterisks(self, s: str) -> int:
        s = s.split("|")
        count = 0
        for c in range(0, len(s), 2):
            count += s[c].count("*")
        return count


sol = Solution()

# print(sol.countAsterisks("l|*e*et|c**o|*de|"))  # 2

assert sol.countAsterisks("l|*e*et|c**o|*de|") == 2
assert sol.countAsterisks("iamprogrammer") == 0
assert sol.countAsterisks("yo|uar|e**|b|e***au|tifu|l") == 5
assert sol.countAsterisks("*") == 1
assert sol.countAsterisks("a") == 0
assert sol.countAsterisks("||") == 0
assert sol.countAsterisks("|*|") == 0
assert sol.countAsterisks("*|*|*") == 2
assert sol.countAsterisks("********") == 8
assert sol.countAsterisks("|*******|") == 0
assert sol.countAsterisks("*||*") == 2
assert sol.countAsterisks("||*") == 1
assert sol.countAsterisks("*|*|*|*|*") == 3
assert sol.countAsterisks("a*b*c") == 2
assert sol.countAsterisks("|a*|b*|c|") == 1
