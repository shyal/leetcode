"""
URL: https://leetcode.com/problems/kth-distinct-string-in-an-array/description/

2053. Kth Distinct String in an Array

A distinct string is a string that is present only once in arr.

Given an array of strings arr, and an integer k, return the kth distinct string present in arr. If there are fewer than k distinct strings, return an empty string "".

Note that the strings are considered in the order in which they appear in the array.


Example 1:

Input: arr = ["d","b","c","b","c","a"], k = 2
Output: "a"
Explanation: The only distinct strings in arr are "d" and "a".
"b" appears twice, so it is not distinct.
"c" appears twice, so it is not distinct.
The distinct strings are "d" and "a".
The second distinct string is "a".

Example 2:

Input: arr = ["aaa","aa","a"], k = 1
Output: "aaa"
Explanation: All strings in arr are distinct, so the 1st string "aaa" is returned.

Example 3:

Input: arr = ["a","b","a"], k = 3
Output: ""
Explanation: The only distinct string is "b". Since there are fewer than 3 distinct strings, we return an empty string "".


Constraints:

    1 <= k <= arr.length <= 1000
    1 <= arr[i].length <= 5
    arr[i] consists of lowercase English letters.
"""


class Solution:
    def kthDistinct(self, arr: List[str], k: int) -> str:
        vals = [s for s, count in dict(Counter(arr)).items() if count == 1]
        return vals[k - 1] if k - 1 < len(vals) else ""


sol = Solution()

# print(sol.kthDistinct(["d", "b", "c", "b", "c", "a"], 2))  # "a"

assert sol.kthDistinct(["d", "b", "c", "b", "c", "a"], 2) == "a"
assert sol.kthDistinct(["aaa", "aa", "a"], 1) == "aaa"
assert sol.kthDistinct(["a", "b", "a"], 3) == ""
assert sol.kthDistinct(["x"], 1) == "x"
assert sol.kthDistinct(["x"], 2) == ""
assert sol.kthDistinct(["a", "b", "c"], 3) == "c"
assert sol.kthDistinct(["a", "a", "a"], 1) == ""
assert sol.kthDistinct(["a", "b", "a", "c", "b"], 1) == "c"
assert sol.kthDistinct(["a", "b", "a", "c", "b"], 2) == ""
assert sol.kthDistinct(["aaa", "aa", "aaa"], 1) == "aa"
assert sol.kthDistinct(["abcde", "abcde"], 1) == ""
assert sol.kthDistinct(["a", "bb", "ccc", "a", "bb", "ddd"], 1) == "ccc"
assert sol.kthDistinct(["a", "bb", "ccc", "a", "bb", "ddd"], 2) == "ddd"
assert sol.kthDistinct(["a", "bb", "ccc", "a", "bb", "ddd"], 3) == ""
