"""
URL: https://leetcode.com/problems/reorganize-string/description/

767. Reorganize String

Given a string s, rearrange the characters of s so that any two adjacent characters are not the same.

Return any possible rearrangement of s or return "" if not possible.


Example 1:
Input: s = "aab"
Output: "aba"
Example 2:
Input: s = "aaab"
Output: ""


Constraints:

        1 <= s.length <= 500
        s consists of lowercase English letters.
"""


class Solution:

    def reorganizeString(self, S):
        counts = [(-count, letter) for letter, count in Counter(S).items()]
        heapify(counts)
        prev = None
        res = ""
        while counts:
            count, letter = heappop(counts)
            if letter == prev:
                if counts:
                    count1, letter1 = heappop(counts)
                    res += letter1
                    count1 += 1
                    if count1 < 0:
                        heappush(counts, (count1, letter1))
                    prev = letter1
                    heappush(counts, (count, letter))
                else:
                    return ""
            else:
                res += letter
                count += 1
                if count < 0:
                    heappush(counts, (count, letter))
                prev = letter
        return res


sol = Solution()
res = sol.reorganizeString("vvvlo")
assert Counter(res) == Counter("vvvlo")
assert all((res[i] != res[i + 1] for i in range(len(res) - 1)))
res = sol.reorganizeString("aab")
assert len(res) == 3
assert Counter(res) == Counter("aab")
assert all((res[i] != res[i + 1] for i in range(len(res) - 1)))
res = sol.reorganizeString("aaabb")
assert len(res) == 5
assert Counter(res) == Counter("aaabb")
assert all((res[i] != res[i + 1] for i in range(len(res) - 1)))
res = sol.reorganizeString("aaaabbbcc")
assert len(res) == 9
assert Counter(res) == Counter("aaaabbbcc")
assert all((res[i] != res[i + 1] for i in range(len(res) - 1)))
res = sol.reorganizeString("aaaaabbbbccc")
assert len(res) == 12
assert Counter(res) == Counter("aaaaabbbbccc")
assert all((res[i] != res[i + 1] for i in range(len(res) - 1)))
res = sol.reorganizeString("a")
assert len(res) == 1
assert Counter(res) == Counter("a")
assert all((res[i] != res[i + 1] for i in range(len(res) - 1)))
res = sol.reorganizeString("ab")
assert len(res) == 2
assert Counter(res) == Counter("ab")
assert all((res[i] != res[i + 1] for i in range(len(res) - 1)))
res = sol.reorganizeString("abb")
assert len(res) == 3
assert Counter(res) == Counter("abb")
assert all((res[i] != res[i + 1] for i in range(len(res) - 1)))
res = sol.reorganizeString("abcc")
assert len(res) == 4
assert Counter(res) == Counter("abcc")
assert all((res[i] != res[i + 1] for i in range(len(res) - 1)))
res = sol.reorganizeString("vvlo")
assert len(res) == 4
assert Counter(res) == Counter("vvlo")
assert all((res[i] != res[i + 1] for i in range(len(res) - 1)))
res = sol.reorganizeString("aaab")
assert res == ""
res = sol.reorganizeString("aa")
assert res == ""
res = sol.reorganizeString("aaa")
assert res == ""
