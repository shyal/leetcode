# URL: https://leetcode.com/problems/search-suggestions-system/description/?envType=problem-list-v2&envId=vn57k9wr
#
# 1268. Search Suggestions System
#
# You are given an array of strings products and a string searchWord.
#
# Design a system that suggests at most three product names from products after each character of searchWord is typed. Suggested products should have common prefix with searchWord. If there are more than three products with a common prefix return the three lexicographically minimum products.
#
# Return a list of lists of the suggested products after each character of searchWord is typed.
#
# Example 1:
#
# Input: products = ["mobile","mouse","moneypot","monitor","mousepad"], searchWord = "mouse"
# Output: [["mobile","moneypot","monitor"],["mobile","moneypot","monitor"],["mouse","mousepad"],["mouse","mousepad"],["mouse","mousepad"]]
# Explanation: products sorted lexicographically = ["mobile","moneypot","monitor","mouse","mousepad"].
# After typing m and mo all products match and we show user ["mobile","moneypot","monitor"].
# After typing mou, mous and mouse the system suggests ["mouse","mousepad"].
#
# Example 2:
#
# Input: products = ["havana"], searchWord = "havana"
# Output: [["havana"],["havana"],["havana"],["havana"],["havana"],["havana"]]
# Explanation: The only word "havana" will be always suggested while typing the search word.
#
# Constraints:
#
#     1 <= products.length <= 1000
#     1 <= products[i].length <= 3000
#     1 <= sum(products[i].length) <= 2 * 10^4
#     All the strings of products are unique.
#     products[i] consists of lowercase English letters.
#     1 <= searchWord.length <= 1000
#     searchWord consists of lowercase English letters.
#
# ---
# STAGE 1 of 3 - the approach. Write it in plain English under this line. Then run make solved.
# the fast way is to build a trie, but since the constraints are small we can brute force this
# use an outer loop over the letters of the search word, so the first loop is m, second is mo etc.
# in the inner loop, get the products with matching prefixes.
# then sort them, and append the first 3 to an array.
# continue this process for all prefixes in searchWord.
# STAGE 1: pass
# STAGE 2 of 3 - the pseudocode. Write one comment line for each step in the solve below. Then run make solved.
# STAGE 2: miss (slow)
# LEETCODE: Accepted (2991 ms, 22.2 MB)

# mu 0.17

class Solution
  def suggestedProducts(products: [str], searchWord: str) -> [[str]]
    ret res = []
    for >i in searchWord
      cand = []
      prefix = searchWord[:i+1]
      for p in products
        common = commonprefix([prefix, p])
        if len common == len prefix
          cand <- p
      res <- [*sorted(cand)][:3]

sol = Solution()

print(sol.suggestedProducts(['mobile', 'mouse', 'moneypot', 'monitor', 'mousepad'], 'mouse'))

# [["mobile","moneypot","monitor"],["mobile","moneypot","monitor"],["mouse","mousepad"],["mouse","mousepad"],["mouse","mousepad"]]
assert sol.suggestedProducts(['mobile', 'mouse', 'moneypot', 'monitor', 'mousepad'], 'mouse') == [['mobile', 'moneypot', 'monitor'], ['mobile', 'moneypot', 'monitor'], ['mouse', 'mousepad'], ['mouse', 'mousepad'], ['mouse', 'mousepad']]
assert sol.suggestedProducts(['havana'], 'havana') == [['havana'], ['havana'], ['havana'], ['havana'], ['havana'], ['havana']]
assert sol.suggestedProducts(['a', 'aa', 'aaa', 'aaaa'], 'aaaa') == [['a', 'aa', 'aaa'], ['aa', 'aaa', 'aaaa'], ['aaa', 'aaaa'], ['aaaa']]
assert sol.suggestedProducts(['abc', 'abd', 'abe', 'abf', 'abg', 'abh'], 'ab') == [['abc', 'abd', 'abe'], ['abc', 'abd', 'abe']]
assert sol.suggestedProducts(['zebra', 'zebras', 'zen', 'zero'], 'ze') == [['zebra', 'zebras', 'zen'], ['zebra', 'zebras', 'zen']]
assert sol.suggestedProducts(['apple', 'app', 'application', 'apply', 'apt'], 'app') == [['app', 'apple', 'application'], ['app', 'apple', 'application'], ['app', 'apple', 'application']]
assert sol.suggestedProducts(['dog', 'deer', 'deal'], 'cat') == [[], [], []]
assert sol.suggestedProducts(['aaa', 'aaa', 'aaa'], 'a') == [['aaa', 'aaa', 'aaa']]
assert sol.suggestedProducts(['x', 'y', 'z'], 'a') == [[]]
assert sol.suggestedProducts(['abc', 'abcd', 'abcde', 'abcdef'], 'abcdefg') == [['abc', 'abcd', 'abcde'], ['abc', 'abcd', 'abcde'], ['abc', 'abcd', 'abcde'], ['abcd', 'abcde', 'abcdef'], ['abcde', 'abcdef'], ['abcdef'], []]
assert sol.suggestedProducts(['mike', 'mike', 'mike', 'mike'], 'mike') == [['mike', 'mike', 'mike'], ['mike', 'mike', 'mike'], ['mike', 'mike', 'mike'], ['mike', 'mike', 'mike']]
assert sol.suggestedProducts(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'], 'm') == [['m']]
