# REFERENCE: d381 EPI 5.4 Advancing through an array
class Solution:
    def can_reach_end(self, A):
        reach = 0
        for i, step in enumerate(A):
            if i > reach:
                return False
            reach = max(reach, i + step)
        return True
