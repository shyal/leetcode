"""
EPI 16.2 Compute the Levenshtein distance

Given strings A and B, return the least number of edits that turn A into
B. An edit inserts a character, deletes a character, or replaces a
character with another.

Example 1:

Input: A = "kitten", B = "sitting"
Output: 3
Explanation: replace k with s, replace e with i, insert g at the end.

Example 2:

Input: A = "flaw", B = "lawn"
Output: 2
Explanation: delete the f, insert n at the end.

Example 3:

Input: A = "", B = "abc"
Output: 3

Constraints:

    0 <= len(A), len(B) <= 1000
    A and B hold only lowercase letters.

    REQUIRED: O(len(A) * len(B)) time. NO search over sequences of
    edits.
"""


class Solution:
    def levenshtein_distance(self, A: str, B: str) -> int:
        pass


sol = Solution()

print(sol.levenshtein_distance("kitten", "sitting"))  # 3

# assert sol.levenshtein_distance("kitten", "sitting") == 3
# assert sol.levenshtein_distance("flaw", "lawn") == 2
# assert sol.levenshtein_distance("", "abc") == 3
# assert sol.levenshtein_distance("abc", "") == 3
# assert sol.levenshtein_distance("", "") == 0
# assert sol.levenshtein_distance("a", "a") == 0
# assert sol.levenshtein_distance("a", "b") == 1
# assert sol.levenshtein_distance("horse", "ros") == 3
# assert sol.levenshtein_distance("intention", "execution") == 5
# assert sol.levenshtein_distance("abcdef", "azced") == 3
# assert sol.levenshtein_distance("ab" * 500, "ba" * 500) == 2
# assert sol.levenshtein_distance("a" * 1000, "b" * 1000) == 1000
# assert sol.levenshtein_distance("abc" * 300, "abd" * 300) == 300
# assert sol.levenshtein_distance("x" * 1000, "") == 1000
