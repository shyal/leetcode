# REFERENCE: d364 Word Count Engine
class Solution:
    def word_count_engine(self, document):
        count = Counter()
        for token in document.lower().split():
            word = "".join(c for c in token if c.isalpha())
            if word:
                count[word] += 1
        buckets = [[] for _ in range(max(count.values(), default=0) + 1)]
        for word, n in count.items():
            buckets[n].append(word)
        return [[w, str(n)] for n in range(len(buckets) - 1, 0, -1) for w in buckets[n]]
