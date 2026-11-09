# REFERENCE: d473 EPI 12.11 Test the Collatz conjecture
class Solution:
    def test_collatz_conjecture(self, n):
        for start in range(3, n + 1, 2):
            path, x = set(), start
            while x >= start:
                if x in path:
                    return False
                path.add(x)
                x = x // 2 if x % 2 == 0 else 3 * x + 1
        return True
