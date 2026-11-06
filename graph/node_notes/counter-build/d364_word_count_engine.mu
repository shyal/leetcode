# REFERENCE: d364 Word Count Engine
class Solution
  def word_count_engine(document: str) -> [[str]]
    count = {:int}
    for token in document.lower().split()
      word = "".join(c for c in token if c is alpha)
      if word
        count[word] += 1
    buckets = [[] for _ in 0..max(count.values(), default = 0)]
    for word, n in count.items()
      buckets[n] <- word
    [[w, str(n)] for <n in buckets for w in buckets[n]]
