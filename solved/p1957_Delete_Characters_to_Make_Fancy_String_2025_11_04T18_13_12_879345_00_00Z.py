"""
URL: https://leetcode.com/problems/delete-characters-to-make-fancy-string/description/?envType=problem-list-v2&envId=vn57k9wr

1957. Delete Characters to Make Fancy String

A fancy string is a string where no three consecutive characters are equal.

Given a string s, delete the minimum possible number of characters from s to make it fancy.

Return the final string after the deletion. It can be shown that the answer will always be unique.

Example 1:

Input: s = "leeetcode"
Output: "leetcode"
Explanation:
Remove an 'e' from the first group of 'e's to create "leetcode".
No three consecutive characters are equal, so return "leetcode".

Example 2:

Input: s = "aaabaaaa"
Output: "aabaa"
Explanation:
Remove an 'a' from the first group of 'a's to create "aabaaaa".
Remove two 'a's from the second group of 'a's to create "aabaa".
No three consecutive characters are equal, so return "aabaa".

Example 3:

Input: s = "aab"
Output: "aab"
Explanation: No three consecutive characters are equal, so return "aab".

Constraints:

    1 <= s.length <= 10^5
    s consists only of lowercase English letters.
"""


class Solution:
    def makeFancyString(self, s: str) -> str:
        s = list(s)
        count = 1
        keep = [True]
        for i in range(1, len(s)):
            if s[i] == s[i - 1]:
                count += 1
            else:
                count = 1
            keep.append(count < 3)
        res = "".join(compress(s, keep))
        return res


sol = Solution()

# print(sol.makeFancyString("leeetcode"))  # "leetcode"

assert sol.makeFancyString("leeetcode") == "leetcode"
assert sol.makeFancyString("aaabaaaa") == "aabaa"
assert sol.makeFancyString("aab") == "aab"
assert sol.makeFancyString("a") == "a"
assert sol.makeFancyString("aa") == "aa"
assert sol.makeFancyString("aaa") == "aa"
assert sol.makeFancyString("aaaa") == "aa"
assert sol.makeFancyString("aaaaa") == "aa"
assert sol.makeFancyString("abc") == "abc"
assert sol.makeFancyString("abbbccc") == "abbcc"
assert sol.makeFancyString("aaabbbccc") == "aabbcc"
assert sol.makeFancyString("aabbcc") == "aabbcc"
assert sol.makeFancyString("ababab") == "ababab"
assert sol.makeFancyString("aaabaaa") == "aabaa"
assert sol.makeFancyString("aaaabbbb") == "aabb"
