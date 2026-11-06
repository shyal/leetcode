# REFERENCE: d334 Decode Variations
class Solution:
    def decodeVariations(self, S):
        one_ahead, two_ahead = 1, 1
        for i in range(len(S) - 1, -1, -1):
            ways = 0
            if S[i] != "0":
                ways = one_ahead
                if i + 1 < len(S) and int(S[i : i + 2]) <= 26:
                    ways += two_ahead
            one_ahead, two_ahead = ways, one_ahead
        return one_ahead
