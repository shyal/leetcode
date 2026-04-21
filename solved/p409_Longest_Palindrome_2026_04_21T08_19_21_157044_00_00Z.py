"""
URL: https://leetcode.com/problems/longest-palindrome/description/?envType=problem-list-v2&envId=vn57k9wr

409. Longest Palindrome

Given a string s which consists of lowercase or uppercase letters, return the
length of the longest palindrome that can be built with those letters.

Letters are case sensitive, for example, "Aa" is not considered a palindrome.


Example 1:

Input: s = "abccccdd"
Output: 7
Explanation: One longest palindrome that can be built is "dccaccd", whose length is 7.

Example 2:

Input: s = "a"
Output: 1
Explanation: The longest palindrome that can be built is "a", whose length is 1.


Constraints:

    1 <= s.length <= 2000
    s consists of lowercase and/or uppercase English letters only.

---

abccccdd

a: 1
b: 1
c: 4
d: 2

Looks like: simply add even counts: 2 + 4. If an odd count exists, pick the largest one: 1 -- total is 7

"""

class Solution:
    def longestPalindrome(self, s: str) -> int:
        counts = Counter(s)
        even = sum([x for x in counts.values() if x % 2 == 0] or [0])
        total = even
        odds = [*sorted([x for x in counts.values() if x % 2 != 0], reverse=True)]
        if len(odds) == 1:
            return even + odds[0]
        else:
            for i, odd in enumerate(odds):
                if i == 0:
                    total += odd
                else:
                    total += odd -1
            return total

            



sol = Solution()

# print(sol.longestPalindrome("abccccdd"))  # 7

assert sol.longestPalindrome("abccccdd") == 7
assert sol.longestPalindrome("a") == 1
assert sol.longestPalindrome("bb") == 2
assert sol.longestPalindrome("ab") == 1
assert sol.longestPalindrome("Aa") == 1
assert sol.longestPalindrome("aaaa") == 4
assert sol.longestPalindrome("aaa") == 3
assert sol.longestPalindrome("abc") == 1
assert sol.longestPalindrome("aabbcc") == 6
assert sol.longestPalindrome("aabbccd") == 7
assert sol.longestPalindrome("aaabbb") == 5
assert sol.longestPalindrome("AaBbCc") == 1
assert sol.longestPalindrome("AAaa") == 4
assert sol.longestPalindrome("z") == 1
assert sol.longestPalindrome("zZ") == 1
assert sol.longestPalindrome("abcdefg") == 1
assert sol.longestPalindrome("aaaaaaaaaa") == 10
assert sol.longestPalindrome("aaaaaaaaab") == 9
assert sol.longestPalindrome("a" * 2000) == 2000
assert sol.longestPalindrome("a" * 1999 + "b") == 1999
assert sol.longestPalindrome("a" * 1000 + "b" * 1000) == 2000
assert sol.longestPalindrome("a" * 999 + "b" * 1000) == 1999
assert sol.longestPalindrome("abcABC") == 1
assert sol.longestPalindrome("ccc") == 3