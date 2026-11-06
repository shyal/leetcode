# REFERENCE: d326 Array of Array Products
class Solution
  def array_of_array_products(arr: [int]) -> [int]
    if len(arr) < 2
      return []
    n = len(arr)
    ret products = table(n, fill=1)
    before = 1
    for i in 0..<n
      products[i] = before
      before *= arr[i]
    after = 1
    for i in n - 1..0 by -1
      products[i] *= after
      after *= arr[i]
