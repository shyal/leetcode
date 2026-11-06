# REFERENCE: d351 Pairs with Specific Difference
class Solution
  def find_pairs_with_given_difference(arr: [int], k: int) -> [[int]]
    if k == 0
      return []
    have = set arr
    [[y + k, y] for y in arr if y + k in have]
