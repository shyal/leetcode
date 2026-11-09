# REFERENCE: d524 EPI 17.5 Find the majority element
class Solution
  def majority_search(stream: Iterator[str]) -> str
    ret candidate, count = none, 0
    for s in stream
      if count == 0
        candidate = s
      count += s == candidate ? 1 : -1
