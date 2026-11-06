# REFERENCE: d337 Deletion Distance
class Solution:
    def deletion_distance(self, str1, str2):
        @cache
        def f(i, j):
            if i == len(str1):
                return len(str2) - j
            if j == len(str2):
                return len(str1) - i
            if str1[i] == str2[j]:
                return f(i + 1, j + 1)
            return 1 + min(f(i + 1, j), f(i, j + 1))

        return f(0, 0)
