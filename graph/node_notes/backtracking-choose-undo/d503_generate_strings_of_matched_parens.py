# REFERENCE: d503 EPI 15.7 Generate strings of matched parens
class Solution:
    def generate_balanced_parentheses(self, num_pairs):
        out, s = [], []

        def extend(opened, closed):
            if closed == num_pairs:
                out.append("".join(s))
                return
            if opened < num_pairs:
                s.append("(")
                extend(opened + 1, closed)
                s.pop()
            if closed < opened:
                s.append(")")
                extend(opened, closed + 1)
                s.pop()

        extend(0, 0)
        return out
