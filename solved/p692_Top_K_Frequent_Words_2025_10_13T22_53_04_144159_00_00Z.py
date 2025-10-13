"""
URL: https://leetcode.com/problems/top-k-frequent-words/description/

692. Top K Frequent Words

Given a non-empty list of words, return the k most frequent elements.

Your answer should be sorted by frequency from highest to lowest. If two words have the same frequency, then the word with the lower alphabetical order comes first.

Example 1:

Input: words = ["i","love","leetcode","i","love","coding"], k = 2
Output: ["i","love"]
Explanation: "i" and "love" are the two most frequent words.
Note that "i" comes before "love" due to a lower alphabetical order.

Example 2:

Input: words = ["the","day","is","sunny","the","the","the","sunny","is","is"], k = 4
Output: ["the","is","sunny","day"]
Explanation: "the", "is", "sunny" and "day" are the four most frequent words, with the number of occurrence being 4, 3, 2 and 1 respectively.

Constraints:

    1 <= words.length <= 500
    1 <= words[i].length <= 10
    words[i] consists of lowercase English letters.
    k is in the range [1, The number of unique words[i]]

Follow-up: Try to solve it in O(n log k) time and O(n) extra space.
"""


class Solution:
    def topKFrequent(self, words: List[str], k: int) -> List[str]:
        counts = [(-count, word) for word, count in Counter(words).items()]
        heapify(counts)
        return [heappop(counts)[1] for _ in range(k)]


sol = Solution()

# print(sol.topKFrequent(["b", "b", "a", "a"], 2))

assert sol.topKFrequent(["i", "love", "leetcode", "i", "love", "coding"], 2) == [
    "i",
    "love",
]
assert sol.topKFrequent(
    ["the", "day", "is", "sunny", "the", "the", "the", "sunny", "is", "is"], 4
) == ["the", "is", "sunny", "day"]
assert sol.topKFrequent(["hello"], 1) == ["hello"]
assert sol.topKFrequent(["a", "a", "a"], 1) == ["a"]
assert sol.topKFrequent(["c", "b", "a"], 3) == ["a", "b", "c"]
assert sol.topKFrequent(
    ["banana", "apple", "cherry", "apple", "cherry", "banana", "apple"], 3
) == ["apple", "banana", "cherry"]
assert sol.topKFrequent(["b", "a", "c", "a", "b"], 1) == ["a"]
assert sol.topKFrequent(["aa", "a", "aa", "a"], 2) == ["a", "aa"]
assert sol.topKFrequent(["a", "b", "c", "a"], 3) == ["a", "b", "c"]
assert sol.topKFrequent(
    ["the", "day", "is", "sunny", "the", "the", "the", "sunny", "is", "is"], 1
) == ["the"]
