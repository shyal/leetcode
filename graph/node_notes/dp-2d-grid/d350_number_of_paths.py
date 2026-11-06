# REFERENCE: d350 Number of Paths
class Solution:
    def num_of_paths_to_dest(self, n):
        paths = [[0] * n for _ in range(n)]
        paths[0][0] = 1
        for i in range(n):
            for j in range(i + 1):
                if i > 0:
                    paths[i][j] += paths[i - 1][j]
                if j > 0:
                    paths[i][j] += paths[i][j - 1]
        return paths[n - 1][n - 1]
