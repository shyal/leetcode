"""
EPI 15.1 The Towers of Hanoi problem

Given num_rings, the number of rings on peg 0, return a shortest list of
moves that puts every ring on peg 1, or every ring on peg 2. Ring k has
size k, and at the start the rings sit on peg 0 with the largest at the
bottom. A move [a, b] takes the top ring of peg a and puts it on peg b.
No move may put a ring on top of a smaller ring. Any shortest list of
legal moves is accepted.

Example 1:

Input: num_rings = 2
Output: [[0, 2], [0, 1], [2, 1]]
Explanation: ring 1 goes to peg 2, ring 2 goes to peg 1, and ring 1 goes
on top of ring 2.

    start                  end

      1                             1
      2                             2
    -----  -----  -----    -----  -----  -----
    peg 0  peg 1  peg 2    peg 0  peg 1  peg 2

Example 2:

Input: num_rings = 1
Output: [[0, 1]]
Explanation: [[0, 2]] is also accepted.

Example 3:

Input: num_rings = 0
Output: []

Constraints:

    0 <= num_rings <= 15
    The pegs are numbered 0, 1 and 2.

    REQUIRED: O(2^num_rings) time. NO search over the states of the
    pegs.
"""


class Solution:
    def compute_tower_hanoi(self, num_rings: int) -> list[list[int]]:
        pass


sol = Solution()


def replay(num_rings, moves):
    """The three pegs after the moves, bottom ring first; None when a move
    is illegal."""
    pegs = [list(range(num_rings, 0, -1)), [], []]
    for a, b in moves:
        if not pegs[a] or (pegs[b] and pegs[b][-1] < pegs[a][-1]):
            return None
        pegs[b].append(pegs[a].pop())
    return pegs


def done(num_rings):
    full = list(range(num_rings, 0, -1))
    return [[[], full, []], [[], [], full]]


print(sol.compute_tower_hanoi(2))  # [[0, 2], [0, 1], [2, 1]]

# assert sol.compute_tower_hanoi(0) == []
# assert sol.compute_tower_hanoi(1) in ([[0, 1]], [[0, 2]])
# assert sol.compute_tower_hanoi(2) in ([[0, 2], [0, 1], [2, 1]], [[0, 1], [0, 2], [1, 2]])
# moves = sol.compute_tower_hanoi(3)
# assert len(moves) == 7
# assert replay(3, moves) in done(3)
# moves = sol.compute_tower_hanoi(4)
# assert len(moves) == 15
# assert replay(4, moves) in done(4)
# moves = sol.compute_tower_hanoi(5)
# assert len(moves) == 31
# assert replay(5, moves) in done(5)
# moves = sol.compute_tower_hanoi(8)
# assert len(moves) == 255
# assert replay(8, moves) in done(8)
# moves = sol.compute_tower_hanoi(10)
# assert len(moves) == 1023
# assert replay(10, moves) in done(10)
# moves = sol.compute_tower_hanoi(15)
# assert len(moves) == 32767
# assert replay(15, moves) in done(15)
