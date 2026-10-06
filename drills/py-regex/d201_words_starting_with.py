"""
DRILL: Words Starting With
TRAINS: py-regex

Given a sentence `s` of lowercase words and a lowercase letter `c`,
return the words of s that start with c, in order.

Example 1:

Input: s = "which foot or hand fell fastest", c = "f"
Output: ["foot", "fell", "fastest"]

Example 2:

Input: s = "which foot or hand fell fastest", c = "z"
Output: []

Example 3:

Input: s = "a cat and a dog", c = "a"
Output: ["a", "and", "a"]

Constraints:

    1 <= len(s) <= 10^4
    s has lowercase letters and single spaces only; c is one lowercase letter.

    REQUIRED: one re.findall with a raw-string pattern that anchors on a
    word boundary \b and takes the rest of the word with [a-z]*. NO
    split, NO startswith, NO loop over words.
"""

import re


class Solution:

    def words_starting_with(self, s: str, c: str) -> List[str]:
        pass


sol = Solution()

print(sol.words_starting_with("which foot or hand fell fastest", "f"))  # ['foot', 'fell', 'fastest']

# assert sol.words_starting_with("which foot or hand fell fastest", "f") == ["foot", "fell", "fastest"]
# assert sol.words_starting_with("which foot or hand fell fastest", "z") == []
# assert sol.words_starting_with("a cat and a dog", "a") == ["a", "and", "a"]
# assert sol.words_starting_with("off of if", "o") == ["off", "of"]
