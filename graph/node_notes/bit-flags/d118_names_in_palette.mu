# REFERENCE: d118 Names In Palette
def present(palette: Color, names: [str]) -> [str]
  [name for name in names if Color[name] in palette]
