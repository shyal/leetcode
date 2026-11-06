# REFERENCE: d363 Validate IP Address
class Solution:
    def validateIP(self, ip):
        parts = ip.split('.')
        if len(parts) != 4:
            return False
        for p in parts:
            if not p.isdigit() or not p.isascii():
                return False
            if len(p) > 1 and p[0] == '0':
                return False
            if int(p) > 255:
                return False
        return True
