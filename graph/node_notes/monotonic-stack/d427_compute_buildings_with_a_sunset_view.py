# REFERENCE: d427 EPI 8.5 Compute buildings with a sunset view
class Solution:
    def examine_buildings_with_sunset(self, sequence):
        stack = []  # (index, height), heights strictly decreasing
        for i, height in enumerate(sequence):
            while stack and stack[-1][1] <= height:
                stack.pop()
            stack.append((i, height))
        return [i for i, _ in reversed(stack)]
