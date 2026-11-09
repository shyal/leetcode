# REFERENCE: d425 EPI 8.3 Is a string well-formed?
class Solution:
    def is_well_formed(self, s):
        opener = {")": "(", "]": "[", "}": "{"}
        stack = []
        for c in s:
            if c not in opener:
                stack.append(c)
            elif not stack or stack.pop() != opener[c]:
                return False
        return not stack
