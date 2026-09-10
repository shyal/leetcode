"""
DRILL: Parts Per Pallet

Given crates, where crates[i] is the list of part ids in crate i, return
one merged list per pallet. Solution extends UnionFind from
dsa/union_find.py, built over the crates, and the tests have already
joined the crates stacked on each pallet, so self.find(i) returns the
head of the pallet crate i is stacked on. A merged list is the sorted
list of distinct part ids across the crates of its pallet. Order the
merged lists by the smallest crate index on each pallet.

Example 1:

Input: crates = [[21, 24], [22], [24, 27], [23, 22]],
       pallets = [[0, 2], [1, 3]]
Output: [[21, 24, 27], [22, 23]]
Explanation: crates 0 and 2 are stacked on one pallet and both hold part
24, which is listed once. Crates 1 and 3 are stacked on the other.

   pallet [0, 2]            pallet [1, 3]
   +----------------+      +----------------+
   | crate 0: 21 24 |      | crate 1: 22    |
   | crate 2: 24 27 |      | crate 3: 23 22 |
   +----------------+      +----------------+
      [21, 24, 27]              [22, 23]

Example 2:

Input: crates = [[26], [26], [26]], pallets = [[0, 1, 2]]
Output: [[26]]

Constraints:

    1 <= len(crates) <= 1000
    1 <= len(crates[i]) <= 10
    0 <= part id < 10^6
    the tests call self.union along each pallet before calling you

    REQUIRED: must call self.find at most once per crate. NO crate-to-crate
    pair tests; NO scan for heads other than through self.find.
"""

from dsa.union_find import UnionFind


class Solution(UnionFind):
    def mergePallets(self, crates: List[List[int]]) -> List[List[int]]:
        pass


def merged(sol, crates, pallets):
    for pallet in pallets:
        for a, b in zip(pallet, pallet[1:]):
            sol.union(a, b)
    return sol.mergePallets(crates)


sol = Solution(4)

print(merged(sol, [[21, 24], [22], [24, 27], [23, 22]], [[0, 2], [1, 3]]))  # [[21, 24, 27], [22, 23]]

# assert merged(Solution(4), [[21, 24], [22], [24, 27], [23, 22]], [[0, 2], [1, 3]]) == [[21, 24, 27], [22, 23]]
# assert merged(Solution(3), [[26], [26], [26]], [[0, 1, 2]]) == [[26]]
# assert merged(Solution(1), [[28]], [[0]]) == [[28]]
# assert merged(Solution(2), [[21, 22], [23, 24]], [[0], [1]]) == [[21, 22], [23, 24]]
# assert merged(Solution(4), [[29], [21, 22], [23, 24], [22, 23]], [[0], [1, 2, 3]]) == [[29], [21, 22, 23, 24]]
