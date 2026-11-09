"""
EPI 17.5 Find the majority element

Given an iterator stream of strings in which a string occurs more than
half of the time, return that string. The iterator can be read only once.
Use the Boyer-Moore majority vote algorithm.

Example 1:

Input: stream = iter(["b", "a", "c", "a", "a", "b", "a", "a", "c", "a"])
Output: "a"
Explanation: "a" occurs 6 times out of 10.

Example 2:

Input: stream = iter(["x"])
Output: "x"

Example 3:

Input: stream = iter(["p", "q", "q"])
Output: "q"

Constraints:

    1 <= number of strings in stream <= 10^6
    A string occurs more than half of the time.

    REQUIRED: O(n) time and O(1) extra space for n strings. NO Counter,
    NO dict, NO list of the strings.
"""


class Solution:
    def majority_search(self, stream: Iterator[str]) -> str:
        pass


sol = Solution()

print(sol.majority_search(iter(["b", "a", "c", "a", "a", "b", "a", "a", "c", "a"])))  # a

# assert sol.majority_search(iter(["b", "a", "c", "a", "a", "b", "a", "a", "c", "a"])) == "a"
# assert sol.majority_search(iter(["x"])) == "x"
# assert sol.majority_search(iter(["p", "q", "q"])) == "q"
# assert sol.majority_search(iter(["q", "q", "p"])) == "q"
# assert sol.majority_search(iter(["q", "p", "q"])) == "q"
# assert sol.majority_search(iter(["m", "m"])) == "m"
# assert sol.majority_search(iter(["a", "b", "c", "d", "e", "e", "e", "e", "e"])) == "e"
# assert sol.majority_search(iter(["e", "e", "e", "e", "e", "a", "b", "c", "d"])) == "e"
# assert sol.majority_search(iter(["ab", "cd", "ab"])) == "ab"
# assert sol.majority_search(iter(["", "x", ""])) == ""
# assert sol.majority_search(iter(["a", "b"] * 50000 + ["a"])) == "a"
# assert sol.majority_search(iter(["b", "a"] * 50000 + ["a"])) == "a"
# assert sol.majority_search("k" if i % 3 else "m" for i in range(300000)) == "k"
# assert sol.majority_search(iter(["y"] * 499999 + ["z"] * 500001)) == "z"
