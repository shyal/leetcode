# REFERENCE: d80 Shake Hands With The Host
def handshakes(parties: [[int]]) -> {int: [int]}
  adj = adjacency([(p[0], g) for p in parties for g in p[1:]], directed = false)
  for p in parties
    for g in p
      adj[g]
  adj
