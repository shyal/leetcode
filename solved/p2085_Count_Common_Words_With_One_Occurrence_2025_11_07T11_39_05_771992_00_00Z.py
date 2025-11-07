"""
URL: https://leetcode.com/problems/count-common-words-with-one-occurrence/description/?envType=problem-list-v2&envId=vn57k9wr

2085. Count Common Words With One Occurrence

Given two string arrays words1 and words2, return the number of strings that appear exactly once in each of the two arrays.


Example 1:

Input: words1 = ["leetcode","is","amazing","as","is"], words2 = ["amazing","leetcode","is"]
Output: 2
Explanation:
- "leetcode" appears exactly once in each of the two arrays. We count this string.
- "amazing" appears exactly once in each of the two arrays. We count this string.
- "is" appears in each of the two arrays, but there are 2 occurrences of it in words1. We do not count this string.
- "as" appears once in words1, but does not appear in words2. We do not count this string.
Thus, there are 2 strings that appear exactly once in each of the two arrays.

Example 2:

Input: words1 = ["b","bb","bbb"], words2 = ["a","aa","aaa"]
Output: 0
Explanation: There are no strings that appear in each of the two arrays.

Example 3:

Input: words1 = ["a","ab"], words2 = ["a","a","a","ab"]
Output: 1
Explanation: The only string that appears exactly once in each of the two arrays is "ab".


Constraints:

    1 <= words1.length, words2.length <= 1000
    1 <= words1[i].length, words2[j].length <= 30
    words1[i] and words2[j] consists only of lowercase English letters.
"""


class Solution:
    def countWords(self, words1: List[str], words2: List[str]) -> int:
        get_1_appearances = lambda x: set(
            word for word, count in Counter(x).items() if count == 1
        )
        words1, words2 = get_1_appearances(words1), get_1_appearances(words2)
        return len(words1.intersection(words2))


sol = Solution()

# print(
#     sol.countWords(
#         ["leetcode", "is", "amazing", "as", "is"], ["amazing", "leetcode", "is"]
#     )
# )  # 2

assert (
    sol.countWords(
        ["leetcode", "is", "amazing", "as", "is"], ["amazing", "leetcode", "is"]
    )
    == 2
)
assert sol.countWords(["b", "bb", "bbb"], ["a", "aa", "aaa"]) == 0
assert sol.countWords(["a", "ab"], ["a", "a", "a", "ab"]) == 1
assert sol.countWords(["a"], ["a"]) == 1
assert sol.countWords(["a"], ["b"]) == 0
assert sol.countWords(["a", "a"], ["a"]) == 0
assert sol.countWords(["a", "b", "c"], ["a", "b", "c"]) == 3
assert sol.countWords(["aa"], ["aa", "aa"]) == 0
assert sol.countWords(["x", "x", "x"], ["x"]) == 0
assert sol.countWords(["hello", "world", "hello"], ["world", "hello"]) == 1
assert sol.countWords(["ab", "ab"], ["ab", "cd", "ab"]) == 0
assert sol.countWords(["a" * 30], ["a" * 30]) == 1
assert sol.countWords(["a", "b"], ["b", "c"]) == 1
