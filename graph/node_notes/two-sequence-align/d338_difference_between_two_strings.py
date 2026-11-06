# REFERENCE: d338 Difference Between Two Strings
class Solution:
    def diff_between_two_strings(self, source, target):
        @cache
        def edits(i, j):
            if i == len(source):
                return len(target) - j
            if j == len(target):
                return len(source) - i
            if source[i] == target[j]:
                return edits(i + 1, j + 1)
            return 1 + min(edits(i + 1, j), edits(i, j + 1))

        res = []
        i = j = 0
        while i < len(source) or j < len(target):
            if i < len(source) and j < len(target) and source[i] == target[j]:
                res.append(source[i])
                i += 1
                j += 1
            elif j == len(target) or (i < len(source) and edits(i + 1, j) <= edits(i, j + 1)):
                res.append("-" + source[i])
                i += 1
            else:
                res.append("+" + target[j])
                j += 1
        return res
