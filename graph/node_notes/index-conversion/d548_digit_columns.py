# REFERENCE: d548 Digit Columns
class Solution:
    def digit_columns(self, nums):
        rows = [*map(to_digits, nums)]
        cols = [col for col in zip(*rows)]
        return cols
