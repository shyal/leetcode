# REFERENCE: d531 EPI 18.4 Deadlock detection
class Solution
  def is_deadlocked(graph: [[int]]) -> bool
    state = table(len(graph))
    def cycle_from(v) -> bool
      state[v] = 1
      for w in graph[v]
        if state[w] == 1 or (state[w] == 0 and cycle_from(w))
          return true
      state[v] = 2
      false
    any(state[v] == 0 and cycle_from(v) for v in 0..<len(graph))
