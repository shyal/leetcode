"""
Given two strings str1 and str2, return their deletion distance: the
smallest number of characters to delete, from either string, so that
the two strings become equal.

Example 1:

Input: str1 = "heat", str2 = "hit"
Output: 3
Explanation: delete 'e' and 'a' from "heat" and 'i' from "hit". Both
become "ht". No two deletions make them equal.

Example 2:

Input: str1 = "ab", str2 = "ba"
Output: 2
Explanation: the strings hold the same letters, but in a different
order. Delete 'a' from each, or 'b' from each.

Example 3:

Input: str1 = "some", str2 = "thing"
Output: 9
Explanation: no letter is shared, so every character goes.

Constraints:

    0 <= len(str1), len(str2) <= 200
    str1 and str2 consist of lowercase English letters.

    REQUIRED: O(len(str1) * len(str2)) time. NO enumeration of
    subsequences.
"""


class Solution:
    def deletion_distance(self, str1: str, str2: str) -> int:
        pass


sol = Solution()

print(sol.deletion_distance("heat", "hit"))  # 3

# assert sol.deletion_distance("heat", "hit") == 3
# assert sol.deletion_distance("ab", "ba") == 2
# assert sol.deletion_distance("some", "thing") == 9
# assert sol.deletion_distance("", "") == 0
# assert sol.deletion_distance("", "hit") == 3
# assert sol.deletion_distance("neat", "") == 4
# assert sol.deletion_distance("hot", "not") == 2
# assert sol.deletion_distance("abc", "adbc") == 1
# assert sol.deletion_distance("awesome", "awesome") == 0
# assert sol.deletion_distance("dog", "frog") == 3
# assert sol.deletion_distance("a", "a") == 0
# assert sol.deletion_distance("a", "b") == 2
# assert sol.deletion_distance("abcde", "ace") == 2
# assert sol.deletion_distance("aaaa", "aa") == 2
# assert sol.deletion_distance("a" * 200, "a" * 200) == 0
# assert sol.deletion_distance("a" * 200, "b" * 200) == 400
# assert sol.deletion_distance("ab" * 100, "ba" * 100) == 2
