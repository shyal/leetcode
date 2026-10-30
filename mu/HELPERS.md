# The helpers a mu solve may call

The LeetCode profile's library (`mu/leetmu.py`): the pydsa functions a
mu file calls by name. The transpiler pastes each one's source into the
Python it emits, so LeetCode runs it unchanged, and the ide shows these
lines on hover. Each line is one way of calling the helper and what it
gives.

```python
@as_list                              # above a def: its yields, returned as a list
cells(grid)                           # every (i, j), row by row
cells(grid, start=1)                  # only i, j >= 1
cells(grid, eq=0)                     # only cells holding 0
cells(grid, gte=k)                    # only cells holding k or more; also lt, lte, gt
nbrs(grid, i, j)                      # on-grid neighbours: up, left, right, down
nbrs(grid, p)                         # the same, with the cell as one pair
nbrs(grid, p, eq=inf)                 # only neighbours holding inf; same comparisons
table(m, n, fill=0)                   # m rows of n cells
like(grid, fill=inf)                  # a new table with the shape of grid
shape(grid)                           # (rows, cols); shape(a, b) is (len(a), len(b))
shape(grid, last_index=True)          # the index of the last cell
put(grid, at, v)                      # grid[i][j] = v for every (i, j) in at
put(grid, at, scan(+, xs))            # v may be an iterable: one item per cell, in the order of at
row(grid, i)                          # a copy of row i
col(grid, j)                          # a copy of column j, top to bottom
set_row(grid, i, v)                   # every cell of row i; v one value or an iterable
set_col(grid, j, v)                   # every cell of column j; v one value or an iterable
pairs(n)                              # every (i, j) with 0 <= i < j < n
pairs(n, back=True)                   # the same, grouped by j: cell j looks back at every i < j
levels(q)                             # pops deque q level by level, yields (d, item)
levels(q, grouped=True)               # yields (d, items), one level at a time
levels(q, grid, seen, gte=k)          # drops items seen before or whose value fails
adjacency(edges)                      # adjacency lists; also n, reverse, directed, weighted
indegrees(edges)                      # in-degree of every vertex; same flags
components(land, p -> nbrs(grid, p))  # connected components
graph(vs, edges)                      # a weighted graph; an edge (u, v) has weight 1
dijkstra(g, src)                      # shortest distance to every vertex, inf if unreachable
in_bounds(grid, i, j)                 # True if (i, j) is a cell of grid
in_bounds(grid, p)                    # the same, with the cell as one pair
edges(grid)                           # every (i, j) on the border, row by row
is_edge(grid, i, j)                   # True if (i, j) is on the first or last row or column
grid_bfs(grid, sources)               # steps from the nearest source to every cell, -1 if none
grid_bfs(grid, sources, ok=v -> v == 0)  # enters a cell only if ok(grid[cell]); also dirs
triples(n)                            # every (i, j, k) with 0 <= i < j < k < n
ceil_div(a, b)                        # (a + b - 1) // b
factorial(n)                          # n!, for n >= 0; factorial(0) is 1
primes(n)                             # the primes below n, in order; primes(10) is [2, 3, 5, 7]
primes(lo, hi)                        # the primes in lo..<hi; primes(10, 30) is [11, 13, 17, 19, 23, 29]
first_true(lo, hi, ok)                # smallest x in lo..hi with ok(x); hi + 1 if none
last_true(lo, hi, ok)                 # largest x in lo..hi with ok(x); lo - 1 if none
first_false(lo, hi, ok)               # smallest x in lo..hi without ok(x); hi + 1 if none
last_false(lo, hi, ok)                # largest x in lo..hi without ok(x); lo - 1 if none
min_chunks(nums, cap)                 # fewest runs of nums each summing to at most cap; inf if one exceeds cap
Multiset()                            # a Counter that drops a key when its count reaches 0
heap(xs)                              # a min-heap of xs
heap(xs, type=max)                    # a max-heap of xs
to_digits(num)                        # the digits of an int or str, most significant first
to_digits(num, reverse=True)          # least significant first, digit i is the 10**i place
to_int(ds)                            # the int with these digits, most significant first
to_int(ds, reverse=True)              # the inverse of to_digits(num, reverse=True)
to_digits(num, base=2)                # the bits of num, most significant first; any base works
to_int(bits, base=2)                  # the int with these bits; any base works
num_digits(num)                       # the count of digits of num; 0 has one digit; also base=
even(n)                               # n % 2 == 0
odd(n)                                # n % 2 == 1
```

Items pushed onto `q` while `levels(q)` runs are yielded at the next level.

A heap has `push(x)`, `pop()`, `peek()` and `len`. Iterating over a heap
gives its items in no particular order.
