# REFERENCE: d392 EPI 5.15 Compute a random subset
class Solution:
    def random_subset(self, n, k):
        moved = {}
        for i in range(k):
            j = randint(i, n - 1)
            moved[i], moved[j] = moved.get(j, j), moved.get(i, i)
        return [moved[i] for i in range(k)]
