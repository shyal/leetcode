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

# mu 0.17

class Solution
  def suggestedProducts(products: [str], searchWord: str) -> [[str]]
    pass
