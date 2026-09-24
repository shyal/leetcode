# REFERENCE: d147 Split The Excess
class Solution:
    def nextRow(self, row):
        new_row = table(len(row) + 1, fill=0)
        for c, amt in enumerate(row):
            excess = (amt - 1) / 2
            if excess > 0:
                new_row[c] += excess
                new_row[c + 1] += excess
        return new_row
