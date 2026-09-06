"""
DRILL: Shake Hands With The Host
TRAINS: graph-adjacency-build

Given parties, where parties[i] lists the numbered guests at party i in
arrival order, return the dict adj of who shook hands with whom. The
parties happen over a week, so a guest can attend several. The first to
arrive hosts the party. Every other guest shakes hands with the host.
The dict adj is one record for the week: every guest is a key, and
adj[g] holds every guest g shook hands with, at any party, in the order
the handshakes happen, repeats included.

Example 1:

Input: parties = [[11, 12, 15], [14, 15], [16, 14], [19]]
Output: {11: [12, 15], 12: [11], 15: [11, 14], 14: [15, 16], 16: [14], 19: []}
Explanation: guest 15 goes to party 0, hosted by 11, and party 1, hosted
by 14, so 15 shakes hands once at each. Guest 19 parties alone.

Example 2:

Input: parties = [[13], [13], [13]]
Output: {13: []}

Constraints:

    1 <= len(parties) <= 1000
    1 <= len(parties[i]) <= 10
    0 <= guest number < 10^6

    REQUIRED: must run in O(L) time, where L is the total guest count over
    all parties. NO party-to-party pair tests; NO all-pairs handshakes
    inside a party.
"""


class Solution:

    def handshakes(self, parties: List[List[int]]) -> Dict[int, List[int]]:
        adj = defaultdict(list)
        for guests in parties:
            adj[guests[0]]
            for guest in guests[1:]:
                adj[guest].append(guests[0])
                adj[guests[0]].append(guest)
        return adj


sol = Solution()

print(
    dict(sol.handshakes([[11, 12, 15], [14, 15], [16, 14], [19]]))
)  # {11: [12, 15], 12: [11], 15: [11, 14], 14: [15, 16], 16: [14], 19: []}

assert sol.handshakes([[11, 12, 15], [14, 15], [16, 14], [19]]) == {
    11: [12, 15],
    12: [11],
    15: [11, 14],
    14: [15, 16],
    16: [14],
    19: [],
}
assert sol.handshakes([[13], [13], [13]]) == {13: []}
assert sol.handshakes([[17]]) == {17: []}
assert sol.handshakes([[11, 12], [13, 14]]) == {11: [12], 12: [11], 13: [14], 14: [13]}
assert sol.handshakes([[11, 12], [12, 11]]) == {11: [12, 12], 12: [11, 11]}
assert sol.handshakes([[11, 12], [11, 13]]) == {
    11: [12, 13],
    12: [11],
    13: [11],
}  # one host, two parties
assert sol.handshakes([[15, 11], [12, 11]]) == {
    15: [11],
    11: [15, 12],
    12: [11],
}  # handshake order, not sorted
assert sol.handshakes([[12, 11], [11, 13]]) == {
    12: [11],
    11: [12, 13],
    13: [11],
}  # guest at party 0, host at party 1
