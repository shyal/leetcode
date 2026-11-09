# REFERENCE: d518 EPI 16.11 The pretty printing problem
class Solution
  def minimum_messiness(words: [str], line_length: int) -> int
    best = [0]
    for i in 1..len(words)
      free = line_length + 1
      least = inf
      for j in i - 1..0 by -1
        free -= len(words[j]) + 1
        if free < 0
          break
        least = min(least, best[j] + free * free)
      best <- least
    best[-1]
