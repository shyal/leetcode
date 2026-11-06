# REFERENCE: d358 Shortest Word Edit Path
class Solution
  def shortestWordEditPath(source: str, target: str, words: [str]) -> int
    unseen = set(words)
    queue = deque([(source, 0)])
    while queue
      word, steps = queue.popleft()
      if word == target
        return steps
      for i in 0..<len(word)
        for c in "abcdefghijklmnopqrstuvwxyz"
          nxt = word[:i] + c + word[i + 1:]
          if nxt in unseen
            unseen.remove(nxt)
            queue <- (nxt, steps + 1)
    -1
