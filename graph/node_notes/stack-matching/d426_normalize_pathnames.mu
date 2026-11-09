# REFERENCE: d426 EPI 8.4 Normalize pathnames
class Solution
  def shortest_equivalent_path(path: str) -> str
    stack = []
    for name in path.split('/')
      if name in ('', '.')
        continue
      if name == '..' and stack and stack[-1] != '..'
        stack.pop()
      else
        stack <- name
    joined = '/'.join(stack)
    path.startswith('/') ? '/' + joined : joined
