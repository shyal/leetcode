"""
EPI 6.4 Replace and remove

Given a list s of single characters and an integer size, where the
string is s[0] to s[size - 1], change s in place: delete each 'b' and
replace each 'a' with two 'd's. Return the length n of the result. The
result is s[0] to s[n - 1]. The entries of s after the string are ""
and give the room the result needs.

Example 1:

Input: size = 4, s = ["a", "c", "a", "b", ""]
Output: 5, and s[:5] == ["d", "d", "c", "d", "d"]

Example 2:

Input: size = 3, s = ["b", "b", "b"]
Output: 0

Example 3:

Input: size = 2, s = ["c", "a", ""]
Output: 3, and s[:3] == ["c", "d", "d"]

Constraints:

    0 <= size <= len(s) <= 2 * 10^5
    s[0] to s[size - 1] are lowercase letters.
    len(s) is at least the length of the result.

    REQUIRED: O(n) time, O(1) extra space, where n is len(s). NO new
    list, NO insert(), NO del or pop(), NO slice assignment.
"""


class Solution:
    def replace_and_remove(self, size: int, s: list[str]) -> int:
        pass


sol = Solution()

s = ["a", "c", "a", "b", ""]
n = sol.replace_and_remove(4, s)
print(n, s[:n])  # 5 ['d', 'd', 'c', 'd', 'd']

# s = ["a", "c", "a", "b", ""]
# n = sol.replace_and_remove(4, s)
# assert n == 5 and s[:n] == ["d", "d", "c", "d", "d"]
# s = ["b", "b", "b"]
# n = sol.replace_and_remove(3, s)
# assert n == 0
# s = ["c", "a", ""]
# n = sol.replace_and_remove(2, s)
# assert n == 3 and s[:n] == ["c", "d", "d"]
# s = []
# n = sol.replace_and_remove(0, s)
# assert n == 0
# s = ["a", ""]
# n = sol.replace_and_remove(1, s)
# assert n == 2 and s == ["d", "d"]
# s = ["x"]
# n = sol.replace_and_remove(1, s)
# assert n == 1 and s == ["x"]
# s = ["b", "a"]
# n = sol.replace_and_remove(2, s)
# assert n == 2 and s == ["d", "d"]
# s = ["a", "b"]
# n = sol.replace_and_remove(2, s)
# assert n == 2 and s == ["d", "d"]
# s = ["c", "c", "a", "z", "z"]
# n = sol.replace_and_remove(3, s)
# assert n == 4 and s[:n] == ["c", "c", "d", "d"]
# s = ["a", "a", "a", "", "", ""]
# n = sol.replace_and_remove(3, s)
# assert n == 6 and s == ["d"] * 6
# s = list("bcabda") + [""] * 2
# n = sol.replace_and_remove(6, s)
# assert n == 6 and s[:n] == list("cddddd")
# s = list("ab" * 50000)
# n = sol.replace_and_remove(100000, s)
# assert n == 100000 and s == ["d"] * 100000
# s = list("a" * 100000) + [""] * 100000
# n = sol.replace_and_remove(100000, s)
# assert n == 200000 and s == ["d"] * 200000
# s = list("cab" * 30000) + [""] * 30000
# n = sol.replace_and_remove(90000, s)
# assert s[:n] == list("cdd" * 30000)
