# REFERENCE: d348 Move Zeros To End
class Solution
  def moveZerosToEnd(arr: [int]) -> [int]
    w = 0
    for x in arr
      if x != 0
        arr[w] = x
        w += 1
    for i in w..<len(arr)
      arr[i] = 0
    arr
