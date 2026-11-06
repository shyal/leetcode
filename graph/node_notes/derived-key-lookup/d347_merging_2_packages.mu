# REFERENCE: d347 Merging 2 Packages
class Solution
  def get_indices_of_item_weights(arr: [int], limit: int) -> [int]
    seen = {}
    for >i, w in arr
      if limit - w in seen
        return [i, seen[limit - w]]
      seen[w] = i
    []
