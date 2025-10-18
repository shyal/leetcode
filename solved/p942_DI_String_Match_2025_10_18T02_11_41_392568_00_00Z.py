"""
URL: https://leetcode.com/problems/di-string-match/description/?envType=problem-list-v2&envId=vn57k9wr

942. DI String Match

A permutation perm of n + 1 integers of all the integers in the range [0, n] can be represented as a string s of length n where:

        s[i] == 'I' if perm[i] < perm[i + 1], and
        s[i] == 'D' if perm[i] > perm[i + 1].

Given a string s, reconstruct the permutation perm and return it. If there are multiple valid permutations perm, return any of them.


Example 1:
Input: s = "IDID"
Output: [0,4,1,3,2]
Example 2:
Input: s = "III"
Output: [0,1,2,3]
Example 3:
Input: s = "DDI"
Output: [3,2,0,1]


Constraints:

        1 <= s.length <= 105
        s[i] is either 'I' or 'D'.
"""


class Solution:
    def diStringMatch(self, s: str) -> List[int]:
        D = len(s)
        I = 0
        res = []
        for c in s + s[-1]:
            if c == "I":
                res.append(I)
                I += 1
            else:
                res.append(D)
                D -= 1
        return res


sol = Solution()
res = sol.diStringMatch("IDID")
assert res == [0, 4, 1, 3, 2]

res = sol.diStringMatch("III")
assert res == [0, 1, 2, 3]

res = sol.diStringMatch("DDI")
assert res == [3, 2, 0, 1]
