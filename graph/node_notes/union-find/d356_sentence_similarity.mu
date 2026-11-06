# REFERENCE: d356 Sentence Similarity
class Solution
  def areSentencesSimilar(sentence1: [str], sentence2: [str], similarPairs: [[str]]) -> bool
    if len(sentence1) != len(sentence2)
      return false
    parent = {}
    def find(w)
      parent.setdefault(w, w)
      while parent[w] != w
        parent[w] = parent[parent[w]]
        w = parent[w]
      w
    for a, b in similarPairs
      parent[find(a)] = find(b)
    all(find(a) == find(b) for a, b in zip(sentence1, sentence2))
