"""
EPI 12.7 Find smallest subarray sequentially covering all values

Given a list of strings paragraph and a list of distinct strings
keywords, return a pair (start, end) such that keywords is a
subsequence of paragraph[start:end + 1], and end - start is as small as
possible. A subsequence keeps the order: keywords[0] comes first, then
keywords[1], and so on, with other words allowed in between. When
several pairs have the smallest length, return any of them. Return
(-1, -1) when no subarray has keywords as a subsequence.

Example 1:

Input: paragraph = ["a", "b", "x", "c", "a", "b", "c"],
       keywords = ["a", "b", "c"]
Output: (4, 6)
Explanation: the subarray from index 0 to index 3 has "a", "b", "c" in
order too, but it is longer.

Example 2:

Input: paragraph = ["c", "b", "a"], keywords = ["a", "b", "c"]
Output: (-1, -1)
Explanation: every keyword is present, but not in the order of keywords.

Example 3:

Input: paragraph = ["b", "a", "c", "a", "b", "c"], keywords = ["a", "b", "c"]
Output: (3, 5)
Explanation: ["b", "a", "c"] at index 0 contains every keyword, but not
in order.

Constraints:

    0 <= len(paragraph) <= 10^5
    1 <= len(keywords) <= 10^3
    The keywords are distinct.
    Each string is a nonempty string of lowercase letters or digits.

    REQUIRED: O(n) time, where n is the length of paragraph, and O(m)
    extra space, where m is the length of keywords.
"""


class Solution:
    def find_smallest_sequentially_covering_subset(self, paragraph: list[str], keywords: list[str]) -> tuple[int, int]:
        pass


sol = Solution()

print(sol.find_smallest_sequentially_covering_subset(["a", "b", "x", "c", "a", "b", "c"], ["a", "b", "c"]))  # (4, 6)

# assert sol.find_smallest_sequentially_covering_subset(["a", "b", "x", "c", "a", "b", "c"], ["a", "b", "c"]) == (4, 6)
# assert sol.find_smallest_sequentially_covering_subset(["c", "b", "a"], ["a", "b", "c"]) == (-1, -1)
# assert sol.find_smallest_sequentially_covering_subset(["b", "a", "c", "a", "b", "c"], ["a", "b", "c"]) == (3, 5)
# assert sol.find_smallest_sequentially_covering_subset([], ["a"]) == (-1, -1)
# assert sol.find_smallest_sequentially_covering_subset(["a"], ["a"]) == (0, 0)
# assert sol.find_smallest_sequentially_covering_subset(["b", "a"], ["a", "b"]) == (-1, -1)
# assert sol.find_smallest_sequentially_covering_subset(["a", "b", "b", "a"], ["a", "b"]) == (0, 1)
# assert sol.find_smallest_sequentially_covering_subset(["a", "x", "a", "b"], ["a", "b"]) == (2, 3)
# assert sol.find_smallest_sequentially_covering_subset(["a", "x", "b", "y", "a", "b"], ["a", "b"]) == (4, 5)
# assert sol.find_smallest_sequentially_covering_subset(["a", "b", "a", "b"], ["a", "b"]) in [(0, 1), (2, 3)]
# assert sol.find_smallest_sequentially_covering_subset(["a", "c", "b", "c", "a", "b", "c"], ["a", "b", "c"]) == (4, 6)
# assert sol.find_smallest_sequentially_covering_subset(["a", "b", "a", "x", "c"], ["a", "b", "c"]) == (0, 4)
# assert sol.find_smallest_sequentially_covering_subset(["x"] * 10 ** 5 + ["a", "b"], ["a", "b"]) == (10 ** 5, 10 ** 5 + 1)
# assert sol.find_smallest_sequentially_covering_subset(["a"] + ["x"] * 10 ** 5 + ["b"], ["a", "b"]) == (0, 10 ** 5 + 1)
# assert sol.find_smallest_sequentially_covering_subset(["b"] * 10 ** 5 + ["a"], ["a", "b"]) == (-1, -1)
# keywords = [str(i) for i in range(1000)]
# r = sol.find_smallest_sequentially_covering_subset(keywords * 100, keywords)
# assert r[1] - r[0] == 999 and r[0] % 1000 == 0
