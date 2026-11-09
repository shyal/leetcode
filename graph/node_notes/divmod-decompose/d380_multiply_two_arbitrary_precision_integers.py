# REFERENCE: d380 EPI 5.3 Multiply two arbitrary-precision integers
class Solution:
    def multiply(self, num1, num2):
        sign = -1 if (num1[0] < 0) != (num2[0] < 0) else 1
        a = [abs(num1[0])] + num1[1:]
        b = [abs(num2[0])] + num2[1:]
        res = [0] * (len(a) + len(b))
        for i in reversed(range(len(a))):
            for j in reversed(range(len(b))):
                res[i + j + 1] += a[i] * b[j]
                res[i + j] += res[i + j + 1] // 10
                res[i + j + 1] %= 10
        k = 0
        while k < len(res) - 1 and res[k] == 0:
            k += 1
        res = res[k:]
        res[0] *= sign
        return res
