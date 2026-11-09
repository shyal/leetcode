# REFERENCE: d514 EPI 16.7 Building a search index for domains
class Solution
  def decompose_into_dictionary_words(domain: str, dictionary: {str}) -> [str]
    n = len(domain)
    last = [0] * (n + 1)
    last[0] = -1
    for end in 1..n
      for start in 0..<end
        if last[start] and domain[start:end] in dictionary
          last[end] = end - start
          break
    if not last[n]
      return []
    words, end = [], n
    while end
      words <- domain[end - last[end]:end]
      end -= last[end]
    words[::-1]
