"""
EPI 12.5 Find the nearest repeated entries in an array

Given a list of strings words, return the smallest distance j - i over
all index pairs (i, j) such that i < j and words[i] == words[j]. Return
-1 when no word appears twice.

Example 1:

Input: words = ["red", "blue", "green", "blue", "red"]
Output: 2
Explanation: "blue" is at indices 1 and 3. "red" is at indices 0 and 4.

Example 2:

Input: words = ["a", "b", "c"]
Output: -1

Example 3:

Input: words = ["x", "y", "x", "x"]
Output: 1
Explanation: the last two "x" are next to each other.

Constraints:

    0 <= len(words) <= 10^5
    Each word is a nonempty string of lowercase letters or digits.

    REQUIRED: O(n) time, where n is the length of words. NO sorting.
"""


class Solution:
    def find_nearest_repetition(self, words: list[str]) -> int:
        pass


sol = Solution()

print(sol.find_nearest_repetition(["red", "blue", "green", "blue", "red"]))  # 2

# assert sol.find_nearest_repetition(["red", "blue", "green", "blue", "red"]) == 2
# assert sol.find_nearest_repetition(["a", "b", "c"]) == -1
# assert sol.find_nearest_repetition(["x", "y", "x", "x"]) == 1
# assert sol.find_nearest_repetition([]) == -1
# assert sol.find_nearest_repetition(["a"]) == -1
# assert sol.find_nearest_repetition(["a", "a"]) == 1
# assert sol.find_nearest_repetition(["a", "b", "a"]) == 2
# assert sol.find_nearest_repetition(["a", "a", "b", "c", "b"]) == 1
# assert sol.find_nearest_repetition(["a", "b", "c", "a", "b", "b"]) == 1
# assert sol.find_nearest_repetition(["p", "q", "r", "s", "p", "q", "r", "s"]) == 4
# assert sol.find_nearest_repetition(["a", "b", "a", "c", "c", "a"]) == 1
# assert sol.find_nearest_repetition([str(i) for i in range(10 ** 5)]) == -1
# assert sol.find_nearest_repetition([str(i % 1000) for i in range(10 ** 5)]) == 1000
# assert sol.find_nearest_repetition([str(i) for i in range(10 ** 5 - 1)] + ["0"]) == 10 ** 5 - 1
