# REFERENCE: d517 EPI 16.10 Count the number of moves to climb stairs
class Solution:
    def number_of_ways_to_top(self, top, maximum_step):
        ways = [1]
        for h in range(1, top + 1):
            ways.append(sum(ways[max(0, h - maximum_step) : h]))
        return ways[top]
