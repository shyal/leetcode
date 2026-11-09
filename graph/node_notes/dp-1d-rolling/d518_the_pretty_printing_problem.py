# REFERENCE: d518 EPI 16.11 The pretty printing problem
class Solution:
    def minimum_messiness(self, words, line_length):
        best = [0]
        for i in range(1, len(words) + 1):
            free = line_length + 1
            least = inf
            for j in range(i - 1, -1, -1):
                free -= len(words[j]) + 1
                if free < 0:
                    break
                least = min(least, best[j] + free * free)
            best.append(least)
        return best[-1]
