# REFERENCE: d126 Held By Both
def both(a: Color, b: Color, names: [str]) -> [str]
  [name for name in names if Color[name] in a & b]
