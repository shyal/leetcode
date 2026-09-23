"""
DRILL: Count AB Subsequences
TRAINS: dp-1d-rolling

Given a string s, return the number of subsequences of s that equal "ab".
That is the number of index pairs i < j with s[i] == "a" and s[j] == "b".

Example 1:

Input: s = "aabab"
Output: 5
Explanation: the b at index 2 pairs with two a's before it, and the b at
index 4 pairs with three.

Example 2:

Input: s = "abcab"
Output: 3

Example 3:

Input: s = "bbaa"
Output: 0
Explanation: every a comes after every b.

Constraints:

    1 <= len(s) <= 10^5
    s consists of lowercase English letters.

    REQUIRED: O(len(s)) time, one pass. Pairing every b with every earlier
    index is the fail. NO nested loop.
"""


class Solution:
    def countAB(self, s: str) -> int:
        count = 0
        a = 0
        for c in s:
            if c == "a":
                a += 1
            elif c == "b":
                count += a
        return count


sol = Solution()

print(sol.countAB("aabab"))  # 5

assert sol.countAB("aabab") == 5
assert sol.countAB("abcab") == 3
assert sol.countAB("bbaa") == 0
assert sol.countAB("ab") == 1
assert sol.countAB("a") == 0
assert sol.countAB("b") == 0
assert sol.countAB("ba") == 0
assert sol.countAB("abbb") == 3
assert sol.countAB("aaab") == 3
assert sol.countAB("xaybz") == 1
assert sol.countAB("a" * 50000 + "b" * 50000) == 2500000000
