# REFERENCE: d406 EPI 6.9 Compute all valid IP addresses
class Solution:
    def get_valid_ip_address(self, s):
        def valid(part):
            return len(part) <= 3 and (part == "0" or part[0] != "0") and int(part) <= 255

        n, out = len(s), []
        for i in range(1, min(4, n)):
            for j in range(i + 1, min(i + 4, n)):
                for k in range(j + 1, min(j + 4, n)):
                    parts = s[:i], s[i:j], s[j:k], s[k:]
                    if all(valid(p) for p in parts):
                        out.append(".".join(parts))
        return out
