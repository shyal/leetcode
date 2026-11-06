# REFERENCE: d363 Validate IP Address
class Solution
  def validateIP(ip: str) -> bool
    parts = ip.split('.')
    if len(parts) != 4
      return false
    for p in parts
      if not p.isdigit() or not p.isascii()
        return false
      if len(p) > 1 and p[0] == '0'
        return false
      if int(p) > 255
        return false
    true
