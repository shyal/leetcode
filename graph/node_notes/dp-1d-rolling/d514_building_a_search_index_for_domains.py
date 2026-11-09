# REFERENCE: d514 EPI 16.7 Building a search index for domains
class Solution:
    def decompose_into_dictionary_words(self, domain, dictionary):
        n = len(domain)
        last = [0] * (n + 1)
        last[0] = -1
        for end in range(1, n + 1):
            for start in range(end):
                if last[start] and domain[start:end] in dictionary:
                    last[end] = end - start
                    break
        if not last[n]:
            return []
        words, end = [], n
        while end:
            words.append(domain[end - last[end] : end])
            end -= last[end]
        return words[::-1]
