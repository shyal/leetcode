# REFERENCE: d359 Smallest Substring of All Characters
class Solution:
    def get_shortest_unique_substring(self, arr, s):
        need = set(arr)
        count = Counter()
        left = 0
        best = ""
        for right, c in enumerate(s):
            if c in need:
                count[c] += 1
            while len(count) == len(need):
                if best == "" or right - left + 1 < len(best):
                    best = s[left:right + 1]
                d = s[left]
                if d in need:
                    count[d] -= 1
                    if count[d] == 0:
                        del count[d]
                left += 1
        return best
