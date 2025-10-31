"""
URL: https://leetcode.com/problems/count-substrings-that-satisfy-k-constraint-i/description/?envType=problem-list-v2&envId=vn57k9wr

3258. Count Substrings That Satisfy K-Constraint I

You are given a binary string s and an integer k.

A binary string satisfies the k-constraint if either of the following conditions holds:

- The number of 0's in the string is at most k.

- The number of 1's in the string is at most k.

Return an integer denoting the number of substrings of s that satisfy the k-constraint.

Example 1:

Input: s = "10101", k = 1
Output: 12
Explanation: Every substring of s except the substrings "1010", "10101", and "0101" satisfies the k-constraint.

Example 2:

Input: s = "1010101", k = 2
Output: 25
Explanation: Every substring of s except the substrings with a length greater than 5 satisfies the k-constraint.

Example 3:

Input: s = "11111", k = 1
Output: 15
Explanation: All substrings of s satisfy the k-constraint.

Constraints:

- 1 <= s.length <= 50
- 1 <= k <= s.length
- s[i] is either '0' or '1'.
"""


class Solution:
    def countKConstraintSubstrings(self, s: str, k: int) -> int:
        count = 0
        for i in range(len(s)):
            for j in range(i, len(s)):
                satisfies_k = lambda x: x.count("1") <= k or x.count("0") <= k
                sat = satisfies_k(s[i : j + 1])
                count += sat
        return count


sol = Solution()

# print(sol.countKConstraintSubstrings("10101", 1))  # 12

assert sol.countKConstraintSubstrings("10101", 1) == 12
assert sol.countKConstraintSubstrings("1010101", 2) == 25
assert sol.countKConstraintSubstrings("11111", 1) == 15
assert sol.countKConstraintSubstrings("0", 1) == 1
assert sol.countKConstraintSubstrings("1", 1) == 1
assert sol.countKConstraintSubstrings("00", 1) == 3
assert sol.countKConstraintSubstrings("11", 1) == 3
assert sol.countKConstraintSubstrings("010", 1) == 6
assert sol.countKConstraintSubstrings("1010", 1) == 9
assert sol.countKConstraintSubstrings("0011", 1) == 9
assert sol.countKConstraintSubstrings("1010101", 1) == 18
assert sol.countKConstraintSubstrings("10101", 3) == 15
assert sol.countKConstraintSubstrings("000111", 1) == 17
assert sol.countKConstraintSubstrings("000111", 2) == 20
assert sol.countKConstraintSubstrings("000111", 3) == 21
