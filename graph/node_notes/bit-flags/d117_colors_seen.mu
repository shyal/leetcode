# REFERENCE: d117 Colors Seen
from enum import Flag
Color = Flag("Color", ["red", "green", "blue"])

def seen(names: [str]) -> Flag
  out = Color(0)
  for name in names
    out |= Color[name]
  out
