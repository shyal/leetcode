"""
EPI 16.7 Building a search index for domains

Given a string domain and a set dictionary of words, return a list of
dictionary words whose concatenation is domain. A word may be used more
than once. When several lists work, any of them is accepted. Return []
when no list works.

Example 1:

Input: domain = "wordsearch",
       dictionary = {"word", "words", "sea", "search", "arch", "ear"}
Output: ["word", "search"]

Example 2:

Input: domain = "wordsearchx",
       dictionary = {"word", "words", "sea", "search", "arch", "ear"}
Output: []
Explanation: no word ends in "x".

Example 3:

Input: domain = "aaaa", dictionary = {"a", "aa"}
Output: ["aa", "aa"]
Explanation: ["a", "a", "aa"] and the other lists are also accepted.

Constraints:

    1 <= len(domain) <= 300
    1 <= len(dictionary) <= 1000
    Every word has 1 to 300 lowercase letters. domain holds only
    lowercase letters.

    REQUIRED: O(len(domain)^2) lookups in dictionary. NO search that
    tries the same suffix of domain more than once.
"""


class Solution:
    def decompose_into_dictionary_words(self, domain: str, dictionary: set[str]) -> list[str]:
        pass


sol = Solution()

print(sol.decompose_into_dictionary_words("wordsearch", {"word", "words", "sea", "search", "arch", "ear"}))  # ['word', 'search']

# D = {"word", "words", "sea", "search", "arch", "ear"}
# assert sol.decompose_into_dictionary_words("wordsearch", D) == ["word", "search"]
# assert sol.decompose_into_dictionary_words("wordsearchx", D) == []
# words = sol.decompose_into_dictionary_words("aaaa", {"a", "aa"})
# assert "".join(words) == "aaaa" and set(words) <= {"a", "aa"}
# assert sol.decompose_into_dictionary_words("a", {"a"}) == ["a"]
# assert sol.decompose_into_dictionary_words("a", {"b"}) == []
# assert sol.decompose_into_dictionary_words("searcharch", D) == ["search", "arch"]
# assert sol.decompose_into_dictionary_words("wordsear", D) == ["words", "ear"]
# assert sol.decompose_into_dictionary_words("arc", D) == []
# words = sol.decompose_into_dictionary_words("catsanddogs", {"cat", "cats", "and", "sand", "dog", "dogs"})
# assert words in (["cat", "sand", "dogs"], ["cats", "and", "dogs"])
# words = sol.decompose_into_dictionary_words("ab" * 150, {"a", "b", "ab", "ba"})
# assert "".join(words) == "ab" * 150 and set(words) <= {"a", "b", "ab", "ba"}
# assert sol.decompose_into_dictionary_words("a" * 299 + "b", {"a", "aa", "aaa", "aaaa"}) == []
# assert sol.decompose_into_dictionary_words("a" * 300, {"a" * 300}) == ["a" * 300]
# words = sol.decompose_into_dictionary_words("a" * 299 + "b", {"a", "aa", "aaa", "ab"})
# assert "".join(words) == "a" * 299 + "b" and words[-1] == "ab"
