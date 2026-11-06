"""
Given an integer n, return the number of paths on an n by n grid from
the square (0, 0) to the square (n - 1, n - 1). A step goes from (i, j)
to (i + 1, j) or to (i, j + 1). Every square (i, j) on the path has
i >= j.

Example 1:

Input: n = 4
Output: 5
Explanation: with E for a step in i and N for a step in j, the paths are
EEENNN, EENENN, ENEENN, ENENEN and EENNEN. The 20 paths without the
i >= j rule include NEEENN, which visits (0, 1).

Example 2:

Input: n = 1
Output: 1
Explanation: the start is the destination.

Example 3:

Input: n = 3
Output: 2
Explanation: EENN and ENEN.

Constraints:

    1 <= n <= 100

    REQUIRED: O(n^2) time. NO closed formula, NO recursion.
"""


class Solution:
    def num_of_paths_to_dest(self, n: int) -> int:
        pass


sol = Solution()

print(sol.num_of_paths_to_dest(4))  # 5

# assert sol.num_of_paths_to_dest(4) == 5
# assert sol.num_of_paths_to_dest(1) == 1
# assert sol.num_of_paths_to_dest(3) == 2
# assert sol.num_of_paths_to_dest(2) == 1
# assert sol.num_of_paths_to_dest(5) == 14
# assert sol.num_of_paths_to_dest(6) == 42
# assert sol.num_of_paths_to_dest(17) == 35357670
# assert sol.num_of_paths_to_dest(20) == 1767263190
# assert sol.num_of_paths_to_dest(100) == 227508830794229349661819540395688853956041682601541047340
