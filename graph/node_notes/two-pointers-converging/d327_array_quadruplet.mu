# REFERENCE: d327 Array Quadruplet
class Solution
  def find_array_quadruplet(arr: [int], s: int) -> [int]
    arr = sort arr
    n = len arr
    for i in 0..<n - 3
      for j in i + 1..<n - 2
        low, high = j + 1, n - 1
        while low < high
          total = arr[i] + arr[j] + arr[low] + arr[high]
          if total < s
            low += 1
          elif total > s
            high -= 1
          else
            return [arr[i], arr[j], arr[low], arr[high]]
    []
