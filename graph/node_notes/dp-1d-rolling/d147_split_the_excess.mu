# REFERENCE: d147 Split The Excess
def nextRow(row: [float]) -> [float]
  new_row = table(len(row) + 1, fill = 0)
  for c, amt in row
    excess = (amt - 1) / 2
    if excess > 0
      new_row[c] += excess
      new_row[c + 1] += excess
  new_row
