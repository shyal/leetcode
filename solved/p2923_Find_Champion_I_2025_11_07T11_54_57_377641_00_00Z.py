"""
URL: https://leetcode.com/problems/find-champion-i/description/?envType=problem-list-v2&envId=vn57k9wr

2923. Find Champion I

**Problem Statement:**

There are `n` teams in a tournament, numbered from `0` to `n-1`. You are given a **0-indexed 2D boolean matrix** `grid` of size `n x n`, where:

- `grid[i][j] == 1` means **team `i` is stronger than team `j`**.
- `grid[i][j] == 0` means **team `j` is stronger than team `i`** (for `i != j`).
- `grid[i][i] == 0` for all `i`.

A team `a` is the **champant** if **no other team is stronger than `a`** — that is, there is no team `b` such that `grid[b][a] == 1`.

**Return the index of the champion team.**

---

### Examples

```python
Input: grid = [[0,1],[0,0]]
Output: 0
# Team 0 beats team 1 → team 0 is champion

Input: grid = [[0,0,1],[1,0,1],[0,0,0]]
Output: 1
# Team 1 beats team 0 and team 2 → team 1 is champion
```

---

### Constraints

- `2 <= n <= 100`
- `grid[i][j]` is `0` or `1`
- `grid[i][i] == 0`
- `grid[i][j] != grid[j][i]` for `i != j`
- The input guarantees **transitivity**: if A beats B and B beats C, then A beats C.
"""


class Solution:
    def findChampion(self, grid: List[List[int]]) -> int:
        scores = defaultdict(int)
        for team in range(len(grid)):
            for match in range(len(grid[team])):
                if grid[team][match]:
                    scores[team] += 1
        return next(
            iter(next(iter(sorted(scores.items(), key=lambda x: x[1], reverse=True))))
        )


sol = Solution()

# print(sol.findChampion([[0, 1], [0, 0]]))  # 0
# print(sol.findChampion([[0, 0, 1], [1, 0, 1], [0, 0, 0]]))  # 1

assert sol.findChampion([[0, 1], [0, 0]]) == 0
assert sol.findChampion([[0, 0, 1], [1, 0, 1], [0, 0, 0]]) == 1
assert sol.findChampion([[0, 0], [1, 0]]) == 1
assert sol.findChampion([[0, 1, 1], [0, 0, 1], [0, 0, 0]]) == 0
assert sol.findChampion([[0, 0, 0], [1, 0, 0], [1, 1, 0]]) == 2
assert sol.findChampion([[0, 0, 0, 0], [1, 0, 0, 0], [1, 1, 0, 0], [1, 1, 1, 0]]) == 3
assert sol.findChampion([[0, 0, 1, 0], [1, 0, 1, 1], [0, 0, 0, 0], [1, 0, 1, 0]]) == 1
