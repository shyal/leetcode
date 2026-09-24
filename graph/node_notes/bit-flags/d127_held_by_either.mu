# REFERENCE: d127 Held By Either
def either(a: Color, b: Color, names: [str]) -> [str]
  [name for name in names if Color[name] in a | b]
