"""
DRILL: Plates Sharing A Bolt

Given plates, where plates[i] is the list of bolt ids passing through
plate i, two plates are connected when at least one bolt passes through
both. Return the adjacency list adj, where adj[i] is the list of indexes
of the plates connected to plate i, in increasing order. A plate is never
connected to itself.

Example 1:

Input: plates = [[51, 53], [52], [53, 54], [54, 52]]
Output: [[2], [3], [0, 3], [1, 2]]
Explanation: bolt 53 passes through plates 0 and 2, bolt 54 through
plates 2 and 3, and bolt 52 through plates 1 and 3. A bolt heads its own
column, and a # is where it passes through the plate.

           51   52   53   54
plate 0     #=========#
plate 1          #
plate 2               #====#
plate 3          #=========#

Example 2:

Input: plates = [[57], [57], [57]]
Output: [[1, 2], [0, 2], [0, 1]]

Constraints:

    1 <= len(plates) <= 500
    1 <= len(plates[i]) <= 10^5
    sum(len(plates[i])) <= 10^5
    0 <= bolt id < 10^6

    REQUIRED: must run in O(n * L) time, where n is the number of plates
    and L is the total number of bolt entries. NO bolt-to-bolt edges; NO
    element-by-element pair tests.
"""


class Solution:

    def plateGraph(self, plates: List[List[int]]) -> List[List[int]]:
        pass


sol = Solution()

print(sol.plateGraph([[51, 53], [52], [53, 54], [54, 52]]))  # [[2], [3], [0, 3], [1, 2]]

# assert sol.plateGraph([[51, 53], [52], [53, 54], [54, 52]]) == [[2], [3], [0, 3], [1, 2]]
# assert sol.plateGraph([[57], [57], [57]]) == [[1, 2], [0, 2], [0, 1]]
# assert sol.plateGraph([[58]]) == [[]]
# assert sol.plateGraph([[51, 52], [53, 54]]) == [[], []]
