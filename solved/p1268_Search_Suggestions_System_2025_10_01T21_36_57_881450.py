"""
1268. Search Suggestions System
Copy
Copy Markdown
Medium
Topics
premium lock icon
Companies
Hint
You are given an array of strings products and a string searchWord.

Design a system that suggests at most three product names from products after each character of searchWord is typed. Suggested products should have common prefix with searchWord. If there are more than three products with a common prefix return the three lexicographically minimums products.

Return a list of lists of the suggested products after each character of searchWord is typed.



Example 1:

Input: products = ["mobile","mouse","moneypot","monitor","mousepad"], searchWord = "mouse"
Output: [["mobile","moneypot","monitor"],["mobile","moneypot","monitor"],["mouse","mousepad"],["mouse","mousepad"],["mouse","mousepad"]]
Explanation: products sorted lexicographically = ["mobile","moneypot","monitor","mouse","mousepad"].
After typing m and mo all products match and we show user ["mobile","moneypot","monitor"].
After typing mou, mous and mouse the system suggests ["mouse","mousepad"].
Example 2:

Input: products = ["havana"], searchWord = "havana"
Output: [["havana"],["havana"],["havana"],["havana"],["havana"],["havana"]]
Explanation: The only word "havana" will be always suggested while typing the search word.


Constraints:

1 <= products.length <= 1000
1 <= products[i].length <= 3000
1 <= sum(products[i].length) <= 2 * 104
All the strings of products are unique.
products[i] consists of lowercase English letters.
1 <= searchWord.length <= 1000
searchWord consists of lowercase English letters.
"""

from typing import List


class Solution:
    def suggestedProducts(
        self, products: List[str], searchWord: str
    ) -> List[List[str]]:
        res = []
        for i in range(len(searchWord)):
            prefix = searchWord[: i + 1]
            res.append([*sorted(filter(lambda x: x.startswith(prefix), products))][:3])
        return res


sol = Solution()

res = sol.suggestedProducts(
    products=["mobile", "mouse", "moneypot", "monitor", "mousepad"], searchWord="mouse"
)

assert res == [
    ["mobile", "moneypot", "monitor"],
    ["mobile", "moneypot", "monitor"],
    ["mouse", "mousepad"],
    ["mouse", "mousepad"],
    ["mouse", "mousepad"],
]

res = sol.suggestedProducts(products=["havana"], searchWord="havana")
assert res == [["havana"], ["havana"], ["havana"], ["havana"], ["havana"], ["havana"]]

res = sol.suggestedProducts(products=["abc"], searchWord="def")
assert res == [[], [], []]

res = sol.suggestedProducts(
    products=["ape", "apple", "application", "apricot"], searchWord="app"
)
assert res == [
    ["ape", "apple", "application"],
    ["ape", "apple", "application"],
    ["apple", "application"],
]

res = sol.suggestedProducts(
    products=["code", "coder", "coding", "codex"], searchWord="code"
)
assert res == [
    ["code", "coder", "codex"],
    ["code", "coder", "codex"],
    ["code", "coder", "codex"],
    ["code", "coder", "codex"],
]

res = sol.suggestedProducts(products=["aa", "ab", "ac", "ad"], searchWord="a")
assert res == [["aa", "ab", "ac"]]

res = sol.suggestedProducts(products=["a", "b", "c"], searchWord="a")
assert res == [["a"]]

res = sol.suggestedProducts(products=["ab", "abc", "abcd", "a"], searchWord="abc")
assert res == [["a", "ab", "abc"], ["ab", "abc", "abcd"], ["abc", "abcd"]]
