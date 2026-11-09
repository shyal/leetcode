# REFERENCE: d478 EPI 13.5 Smallest nonconstructible value
class Solution:
    def smallest_nonconstructible_value(self, A):
        reach = 0
        for x in sorted(A):
            if x > reach + 1:
                break
            reach += x
        return reach + 1
