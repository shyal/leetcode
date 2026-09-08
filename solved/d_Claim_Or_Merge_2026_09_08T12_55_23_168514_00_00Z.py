"""
DRILL: Claim Or Merge
TRAINS: union-find

Given boxes, where boxes[i] is the list of wire ids running through
junction box i, return the dict owner mapping each wire id to the first
box it runs through. Solution extends UnionFind from dsa/union_find.py,
built over the boxes with each box in a circuit of its own. After your
call, two boxes that share a wire must be in the same circuit, and so
must two boxes joined by a chain of shared wires. Call self.union on
boxes only, never on wires. The tests read the circuits back through
self.find.

Example 1:

Input: boxes = [[41, 42], [43], [42, 44], [45, 43]]
Output: owner = {41: 0, 42: 0, 43: 1, 44: 2, 45: 3}
        circuits = [[0, 2], [1, 3]]
Explanation: wire 42 runs through boxes 0 and 2, and wire 43 through
boxes 1 and 3. Box 0 is the first to reach 42, box 1 the first to reach 43.

         41           44
         |            |
      [box 0]==42==[box 2]

      [box 1]==43==[box 3]
                      |
                      45

Example 2:

Input: boxes = [[47], [47], [47]]
Output: owner = {47: 0}
        circuits = [[0, 1, 2]]

Constraints:

    1 <= len(boxes) <= 1000
    1 <= len(boxes[i]) <= 10
    0 <= wire id < 10^6

    REQUIRED: must run in O(L) union and dict operations, where L is the
    total number of wire entries. NO box-to-box pair tests; NO second pass
    over boxes.

---

Learning

"""

from dsa.union_find import UnionFind


class Solution(UnionFind):
    def claimOrMerge(self, boxes: List[List[int]]) -> Dict[int, int]:
        owner = {}
        for i, box in enumerate(boxes):
            for wire in box:
                if wire in owner:
                    self.union(i, owner[wire])
                else:
                    owner[wire] = i
        return owner


def claim(sol, boxes):
    owner = sol.claimOrMerge(boxes)
    circuits = {}
    for i in range(len(boxes)):
        circuits.setdefault(sol.find(i), []).append(i)
    return owner, sorted(circuits.values())


sol = Solution(4)

print(
    claim(sol, [[41, 42], [43], [42, 44], [45, 43]])
)  # ({41: 0, 42: 0, 43: 1, 44: 2, 45: 3}, [[0, 2], [1, 3]])

assert claim(Solution(4), [[41, 42], [43], [42, 44], [45, 43]]) == (
    {41: 0, 42: 0, 43: 1, 44: 2, 45: 3},
    [[0, 2], [1, 3]],
)
assert claim(Solution(3), [[47], [47], [47]]) == ({47: 0}, [[0, 1, 2]])
assert claim(Solution(1), [[48]]) == ({48: 0}, [[0]])
assert claim(Solution(2), [[41, 42], [43, 44]]) == (
    {41: 0, 42: 0, 43: 1, 44: 1},
    [[0], [1]],
)
assert claim(Solution(3), [[41, 42], [43, 44], [42, 43]]) == (
    {41: 0, 42: 0, 43: 1, 44: 1},
    [[0, 1, 2]],
)
