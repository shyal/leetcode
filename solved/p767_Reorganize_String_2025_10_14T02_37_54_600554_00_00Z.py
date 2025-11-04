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

---

Failed. Had to look up the solution.

So great solution. We put the counts on a heap, which i'd imagined could be the case,
then we alternate between using the top element, and the prev element.

I'd come close to this solution, but not quite. I didn't think of using a prev
to alternate.

"""


class Solution:
    def reorganizeString(self, S):
        # not my solution.
        # credit: https://leetcode.com/problems/reorganize-string/solutions/113457/simple-python-solution-using-priorityqueue/
        res, c = [], Counter(S)
        pq = [(-value, key) for key, value in c.items()]
        heapify(pq)
        draw_heap(pq)
        prev_count, prev_char = 0, ""
        while pq:
            count, char = heappop(pq)
            draw_heap(pq)
            res += [char]
            if prev_count < 0:
                heappush(pq, (prev_count, prev_char))
                draw_heap(pq)
            count += 1
            prev_count, prev_char = count, char
        res = "".join(res)
        if len(res) != len(S):
            return ""
        return res


sol = Solution()

res = sol.reorganizeString("vvvlo")  # vlvov
assert Counter(res) == Counter("vvvlo")
assert all(res[i] != res[i + 1] for i in range(len(res) - 1))

res = sol.reorganizeString("aab")
assert len(res) == 3
assert Counter(res) == Counter("aab")
assert all(res[i] != res[i + 1] for i in range(len(res) - 1))

res = sol.reorganizeString("aaabb")
assert len(res) == 5
assert Counter(res) == Counter("aaabb")
assert all(res[i] != res[i + 1] for i in range(len(res) - 1))

res = sol.reorganizeString("aaaabbbcc")
assert len(res) == 9
assert Counter(res) == Counter("aaaabbbcc")
assert all(res[i] != res[i + 1] for i in range(len(res) - 1))

res = sol.reorganizeString("aaaaabbbbccc")
assert len(res) == 12
assert Counter(res) == Counter("aaaaabbbbccc")
assert all(res[i] != res[i + 1] for i in range(len(res) - 1))

res = sol.reorganizeString("a")
assert len(res) == 1
assert Counter(res) == Counter("a")
assert all(res[i] != res[i + 1] for i in range(len(res) - 1))

res = sol.reorganizeString("ab")
assert len(res) == 2
assert Counter(res) == Counter("ab")
assert all(res[i] != res[i + 1] for i in range(len(res) - 1))

res = sol.reorganizeString("abb")
assert len(res) == 3
assert Counter(res) == Counter("abb")
assert all(res[i] != res[i + 1] for i in range(len(res) - 1))

res = sol.reorganizeString("abcc")
assert len(res) == 4
assert Counter(res) == Counter("abcc")
assert all(res[i] != res[i + 1] for i in range(len(res) - 1))

res = sol.reorganizeString("vvlo")
assert len(res) == 4
assert Counter(res) == Counter("vvlo")
assert all(res[i] != res[i + 1] for i in range(len(res) - 1))

res = sol.reorganizeString("aaab")
assert res == ""

res = sol.reorganizeString("aa")
assert res == ""

res = sol.reorganizeString("aaa")
assert res == ""
