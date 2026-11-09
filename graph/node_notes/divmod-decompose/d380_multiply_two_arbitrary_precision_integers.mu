# REFERENCE: d380 EPI 5.3 Multiply two arbitrary-precision integers
class Solution
  def multiply(num1: [int], num2: [int]) -> [int]
    sign = -1 if (num1[0] < 0) != (num2[0] < 0) else 1
    a = [abs(num1[0])] + num1[1:]
    b = [abs(num2[0])] + num2[1:]
    res = [0] * (len(a) + len(b))
    for i in len(a) - 1..0 by -1
      for j in len(b) - 1..0 by -1
        res[i + j + 1] += a[i] * b[j]
        res[i + j] += res[i + j + 1] // 10
        res[i + j + 1] %= 10
    k = 0
    while k < len(res) - 1 and res[k] == 0
      k += 1
    res = res[k:]
    res[0] *= sign
    res
