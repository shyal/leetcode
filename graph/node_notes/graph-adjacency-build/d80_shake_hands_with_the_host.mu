# REFERENCE: d80 Shake Hands With The Host
class Solution
  def handshakes(parties: [[int]]) -> {int: [int]}
    ret res = {:list}
    for guests in parties
      res[guests[0]]
      for guest in guests[1:]
        res[guests[0]] <- guest
        res[guest] <- guests[0]
