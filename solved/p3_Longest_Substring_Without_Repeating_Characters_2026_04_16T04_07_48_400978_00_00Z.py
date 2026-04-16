"""
URL: https://leetcode.com/problems/longest-substring-without-repeating-characters/description/

3. Longest Substring Without Repeating Characters

Medium
Given a string s, find the length of the longest substring without repeating characters.

Example 1:

Input: s = "abcabcbb"
Output: 3
Explanation: The answer is "abc", with the length of 3.

Example 2:

Input: s = "bbbbb"
Output: 1
Explanation: The answer is "b", with the length of 1.

Example 3:

Input: s = "pwwkew"
Output: 3
Explanation: The answer is "wke", with the length of 3.
Notice that the answer must be a substring, "pwke" is a subsequence and not a substring.

Constraints:

0 <= s.length <= 5 * 10^4
s consists of English letters, digits, symbols and spaces.


---

Ok so this is sort of a two pointer algo.

- l and r both start at the first letter, let's use example PWAWKEW, so they're at P
- right point progresses, and builds up a set of letters
- if the right pointer letter is in the set, we need to remove its first instance, as well as letters to its left
    - we can do so by using a dict, with letters as keys, and positions as values
"""

class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        letters = OrderedDict()
        current_length = 0
        longest = 0
        for i, r in enumerate(s):
            if r in letters:
                to_delete = [letter for letter, pos in letters.items() if pos <= letters[r]]
                for d in to_delete:
                    del letters[d]
                    current_length -= 1
            letters[r] = i
            current_length += 1
            if current_length > longest:
                longest = current_length
        return longest

sol = Solution()

assert sol.lengthOfLongestSubstring(s="abcabcbb") == 3
assert sol.lengthOfLongestSubstring(s="bbbbb") == 1
assert sol.lengthOfLongestSubstring(s="pwwkew") == 3
assert sol.lengthOfLongestSubstring(s="") == 0
assert sol.lengthOfLongestSubstring(s="a") == 1
assert sol.lengthOfLongestSubstring(s="abcdefg") == 7
assert sol.lengthOfLongestSubstring(s="aab") == 2
assert sol.lengthOfLongestSubstring(s="dvdf") == 3
assert sol.lengthOfLongestSubstring(s="abba") == 2
assert sol.lengthOfLongestSubstring(s=" ") == 1
assert sol.lengthOfLongestSubstring(s="a b c") == 3
assert sol.lengthOfLongestSubstring(s="123!@#123") == 6
assert sol.lengthOfLongestSubstring(s="tmmzuxt") == 5
assert sol.lengthOfLongestSubstring(s="aa") == 1
