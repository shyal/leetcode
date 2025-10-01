"""
URL: https://leetcode.com/problems/positions-of-large-groups/description/

830. Positions of Large Groups

In a string s of lowercase letters, these letters form consecutive groups of the same character.

For example, a string like s = "abbxxxxzyy" has the groups "a", "bb", "xxxx", "z", and "yy".

A group is identified by an interval [start, end], where start and end denote the start and end indices (inclusive) of the group. In the above example, "xxxx" has the interval [3,6].

A group is considered large if it has 3 or more characters.

Return the intervals of every large group sorted in increasing order by start index.


Example 1:

Input: s = "abbxxxxzzy"
Output: [[3,6]]
Explanation: "xxxx" is the only large group with start index 3 and end index 6.

Example 2:

Input: s = "abc"
Output: []
Explanation: We have groups "a", "b", and "c", none of which are large groups.

Example 3:

Input: s = "abcdddeeeeaabbbcd"
Output: [[3,5],[6,9],[12,14]]
Explanation: The large groups are "ddd", "eeee", and "bbb".


Constraints:

        1 <= s.length <= 1000
        s contains lowercase English letters only.
"""

from itertools import groupby
from collections import namedtuple


class Solution:
    def largeGroupPositions(self, s: str) -> List[List[int]]:
        G = groupby(s)
        Interval = namedtuple("Interval", ["chars", "interval"])
        intervals = []
        i = 0
        for letter, it in G:
            val = "".join(it)
            if len(val) >= 3:
                interval = Interval(val, [i, i + len(val) - 1])
                intervals.append(interval)
            i += len(val)
        intervals.sort(key=lambda x: x.interval[0])
        return [interval.interval for interval in intervals]


sol = Solution()

res = sol.largeGroupPositions(s="abbxxxxzzy")
assert res == [[3, 6]]

res = sol.largeGroupPositions(s="abc")
assert res == []

res = sol.largeGroupPositions(s="abcdddeeeeaabbbcd")
assert res == [[3, 5], [6, 9], [12, 14]]

res = sol.largeGroupPositions(s="")
assert res == []

res = sol.largeGroupPositions(s="abcabcabcabcabcabcabcabcabcabcabcabcabcaaa")
assert res == [[39, 41]]
