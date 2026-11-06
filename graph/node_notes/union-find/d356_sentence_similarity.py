# REFERENCE: d356 Sentence Similarity
class Solution:
    def areSentencesSimilar(self, sentence1, sentence2, similarPairs):
        if len(sentence1) != len(sentence2):
            return False
        parent = {}

        def find(w):
            parent.setdefault(w, w)
            while parent[w] != w:
                parent[w] = parent[parent[w]]
                w = parent[w]
            return w

        for a, b in similarPairs:
            parent[find(a)] = find(b)
        return all(find(a) == find(b) for a, b in zip(sentence1, sentence2))
