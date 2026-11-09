# REFERENCE: d527 EPI 17.8 Compute the largest rectangle under the skyline
class Solution:
    def calculate_largest_rectangle(self, heights):
        stack, best = [], 0
        for i, h in enumerate(heights + [0]):
            while stack and heights[stack[-1]] >= h:
                top = heights[stack.pop()]
                width = i - stack[-1] - 1 if stack else i
                best = max(best, top * width)
            stack.append(i)
        return best
