"""
EPI 12.6 Find the smallest subarray covering all values

Given a list of strings paragraph and a set of strings keywords, return
a pair (start, end) such that paragraph[start:end + 1] contains every
keyword, and end - start is as small as possible. When several pairs
have the smallest length, return any of them. Return (-1, -1) when no
subarray contains every keyword.

Example 1:

Input: paragraph = ["b", "x", "a", "y", "c", "a", "b"],
       keywords = {"a", "b", "c"}
Output: (4, 6)
Explanation: ["c", "a", "b"] has all three keywords. The subarray from
index 0 to index 4 has them too, but it is longer.

Example 2:

Input: paragraph = ["a", "b", "a"], keywords = {"a", "b"}
Output: (0, 1) or (1, 2)

Example 3:

Input: paragraph = ["a", "c"], keywords = {"a", "b"}
Output: (-1, -1)

Constraints:

    0 <= len(paragraph) <= 10^5
    1 <= len(keywords) <= 10^3
    Each string is a nonempty string of lowercase letters or digits.

    REQUIRED: O(n) time, where n is the length of paragraph.
"""


class Solution:
    def find_smallest_subarray_covering_set(self, paragraph: list[str], keywords: set[str]) -> tuple[int, int]:
        pass


sol = Solution()

print(sol.find_smallest_subarray_covering_set(["b", "x", "a", "y", "c", "a", "b"], {"a", "b", "c"}))  # (4, 6)

# assert sol.find_smallest_subarray_covering_set(["b", "x", "a", "y", "c", "a", "b"], {"a", "b", "c"}) == (4, 6)
# assert sol.find_smallest_subarray_covering_set(["a", "b", "a"], {"a", "b"}) in [(0, 1), (1, 2)]
# assert sol.find_smallest_subarray_covering_set(["a", "c"], {"a", "b"}) == (-1, -1)
# assert sol.find_smallest_subarray_covering_set([], {"a"}) == (-1, -1)
# assert sol.find_smallest_subarray_covering_set(["a"], {"a"}) == (0, 0)
# assert sol.find_smallest_subarray_covering_set(["x", "a"], {"a"}) == (1, 1)
# assert sol.find_smallest_subarray_covering_set(["a", "a", "a", "b"], {"a", "b"}) == (2, 3)
# assert sol.find_smallest_subarray_covering_set(["a", "x", "x", "b", "a", "b"], {"a", "b"}) in [(3, 4), (4, 5)]
# assert sol.find_smallest_subarray_covering_set(["a", "b", "c", "x", "x", "a", "x", "b"], {"a", "b", "c"}) == (0, 2)
# assert sol.find_smallest_subarray_covering_set(["a", "x", "b", "x", "x", "c", "b", "a"], {"a", "b", "c"}) == (5, 7)
# assert sol.find_smallest_subarray_covering_set(["b", "a", "x", "a", "c", "x", "b"], {"a", "b", "c"}) == (3, 6)
# assert sol.find_smallest_subarray_covering_set(["x"] * 10 ** 5 + ["a", "b"], {"a", "b"}) == (10 ** 5, 10 ** 5 + 1)
# assert sol.find_smallest_subarray_covering_set(["a"] + ["x"] * 10 ** 5 + ["b"], {"a", "b"}) == (0, 10 ** 5 + 1)
# r = sol.find_smallest_subarray_covering_set(["a", "b"] * 50000, {"a", "b"})
# assert r[1] - r[0] == 1 and {r[0] % 2, r[1] % 2} == {0, 1}
# keywords = {str(i) for i in range(1000)}
# r = sol.find_smallest_subarray_covering_set([str(i % 1000) for i in range(10 ** 5)], keywords)
# assert r[1] - r[0] == 999
