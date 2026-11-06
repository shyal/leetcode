# REFERENCE: d352 Pancake Sort
class Solution
  def pancake_sort(arr: [int]) -> [int]
    def flip(k)
      arr[:k + 1] = arr[k::-1]
    for end in len(arr) - 1..1 by -1
      top = max(0..end, by = arr)
      flip(top)
      flip(end)
    arr
