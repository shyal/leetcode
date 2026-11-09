# REFERENCE: d472 EPI 12.10 Compute all string decompositions
class Solution:
    def find_all_substrings(self, s, words):
        size, count = len(words[0]), len(words)
        want = Counter(words)
        return [
            i
            for i in range(len(s) - size * count + 1)
            if Counter(s[i + j * size : i + (j + 1) * size] for j in range(count)) == want
        ]
