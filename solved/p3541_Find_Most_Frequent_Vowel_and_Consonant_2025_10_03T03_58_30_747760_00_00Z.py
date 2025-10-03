"""
URL: https://leetcode.com/problems/find-most-frequent-vowel-and-consonant/description/?envType=problem-list-v2&envId=vn57k9wr

3541. Find Most Frequent Vowel and Consonant

You are given a string s consisting of lowercase English letters ('a' to 'z').

Your task is to:

    Find the vowel (one of 'a', 'e', 'i', 'o', or 'u') with the maximum frequency.
    Find the consonant (all other letters excluding vowels) with the maximum frequency.

Return the sum of the two frequencies.

Note: If multiple vowels or consonants have the same maximum frequency, you may choose any one of them. If there are no vowels or no consonants in the string, consider their frequency as 0.
The frequency of a letter x is the number of times it occurs in the string.

Example 1:

Input: s = "successes"

Output: 6

Explanation:

    The vowels are: 'u' (frequency 1), 'e' (frequency 2). The maximum frequency is 2.
    The consonants are: 's' (frequency 4), 'c' (frequency 2). The maximum frequency is 4.
    The output is 2 + 4 = 6.

Example 2:

Input: s = "aeiaeia"

Output: 3

Explanation:

    The vowels are: 'a' (frequency 3), 'e' ( frequency 2), 'i' (frequency 2). The maximum frequency is 3.
    There are no consonants in s. Hence, maximum consonant frequency = 0.
    The output is 3 + 0 = 3.


Constraints:

    1 <= s.length <= 100
    s consists of lowercase English letters only.
"""

from collections import Counter


class Solution:
    def maxFreqSum(self, s: str) -> int:
        vowels = set("aeiou")
        freq = defaultdict(int)
        for c in s:
            freq[c] += 1
        freq = list(freq.items())
        freq.sort(key=lambda x: -x[1])
        return next((x[1] for x in freq if x[0] in vowels), 0) + next(
            (x[1] for x in freq if x[0] not in vowels), 0
        )


sol = Solution()
assert sol.maxFreqSum("successes") == 6
assert sol.maxFreqSum("aeiaeia") == 3
assert sol.maxFreqSum("a") == 1
assert sol.maxFreqSum("b") == 1
assert sol.maxFreqSum("aaa") == 3
assert sol.maxFreqSum("bbb") == 3
assert sol.maxFreqSum("aei") == 1
assert sol.maxFreqSum("bcd") == 1
assert sol.maxFreqSum("ab") == 2
assert sol.maxFreqSum("aabbcc") == 4
assert sol.maxFreqSum("mississippi") == 8
