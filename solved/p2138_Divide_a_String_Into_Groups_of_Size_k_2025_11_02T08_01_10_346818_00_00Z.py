"""
URL: https://leetcode.com/problems/divide-a-string-into-groups-of-size-k/description/?envType=problem-list-v2&envId=vn57k9wr

2138. Divide a String Into Groups of Size k

A string s can be partitioned into groups of size k using the following procedure:

- The first group consists of the first k characters of the string, the second group consists of the next k characters of the string, and so on. Each element can be a part of exactly one group.
- For the last group, if the string does not have k characters remaining, a character fill is used to complete the group.

Note that the partition is done so that after removing the fill character from the last group (if it exists) and concatenating all the groups in order, the resultant string should be s.

Given the string s, the size of each group k and the character fill, return a string array denoting the composition of every group s has been divided into, using the above procedure.

Example 1:

Input: s = "abcdefghi", k = 3, fill = "x"
Output: ["abc","def","ghi"]
Explanation:
The first 3 characters "abc" form the first group.
The next 3 characters "def" form the second group.
The last 3 characters "ghi" form the third group.
Since all groups can be completely filled by characters from the string, we do not need to use fill.
Thus, the groups formed are "abc", "def", and "ghi".

Example 2:

Input: s = "abcdefghij", k = 3, fill = "x"
Output: ["abc","def","ghi","jxx"]
Explanation:
Similar to the previous example, we are forming the first three groups "abc", "def", and "ghi".
For the last group, we can only use the character 'j' from the string. To complete this group, we add 'x' twice.
Thus, the 4 groups formed are "abc", "def", "ghi", and "jxx".

Constraints:

- 1 <= s.length <= 100
- s consists of lowercase English letters only.
- 1 <= k <= 100
- fill is a lowercase English letter.
"""


class Solution:
    def divideString(self, s: str, k: int, fill: str) -> List[str]:
        def batched(s, n=1):
            r = list(range(0, len(s), n))
            return [s[a:b] for a, b in zip_longest(r, r[1:])]

        batches = batched(s, k)
        batches[-1] += fill * (k - len(batches[-1]))
        return batches


sol = Solution()

# print(sol.divideString("abcdefghi", 3, "x"))  # ["abc","def","ghi"]

assert sol.divideString("abcdefghi", 3, "x") == ["abc", "def", "ghi"]
assert sol.divideString("abcdefghij", 3, "x") == ["abc", "def", "ghi", "jxx"]
assert sol.divideString("a", 1, "x") == ["a"]
assert sol.divideString("a", 2, "x") == ["ax"]
assert sol.divideString("ab", 2, "x") == ["ab"]
assert sol.divideString("abc", 4, "y") == ["abcy"]
assert sol.divideString("abc", 1, "z") == ["a", "b", "c"]
assert sol.divideString("a", 3, "z") == ["azz"]
assert sol.divideString("abcd", 2, "x") == ["ab", "cd"]
assert sol.divideString("abcde", 3, "f") == ["abc", "def"]
assert sol.divideString("z", 5, "a") == ["zaaaa"]
assert sol.divideString("helloworld", 5, "x") == ["hello", "world"]
assert sol.divideString("short", 10, "p") == ["shortppppp"]
