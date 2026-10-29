# 3841. Palindromic Path Queries in a Tree
class Solution
  def palindromePath(n: int, edges: [[int]], s: str, queries: [str]) -> [bool]
    G = adjacency(edges, n, directed=false)
    s = list(s)
    LOG = n.bit_length()
    up = table(LOG, n)
    depth, tin, tout = table(n)...
    tree = table(n + 2)

    # Euler tour: tin on the way down, tout on the way up
    t = 0
    stack = [0]
    while stack
      v = stack .
      if v >= 0
        tin[v] = t
        t += 1
        stack <- ~v
        for w in G[v]
          if w != up[0][v]
            up[0][w] = v
            depth[w] = depth[v] + 1
            stack <- w
      else
        tout[~v] = t
    for k in 1..<LOG
      for v in 0..<n
        up[k][v] = up[k - 1][up[k - 1][v]]

    def lca(u, v)
      if depth[u] < depth[v]
        u, v = v, u
      for k in 0..<LOG
        if depth[u] - depth[v] >> k & 1
          u = up[k][u]
      for k in reversed(0..<LOG)
        if up[k][u] != up[k][v]
          u, v = up[k][u], up[k][v]
      u == v ? u : up[0][u]

    # Fenwick of xor: a letter toggled on a subtree, read as the xor root..v
    def bit(c): 1 << ord(c) - 97
    def add(i, x)
      while i < len(tree)
        tree[i] ^= x
        i += i & -i
    def toggle(u, x)
      add(tin[u] + 1, x)
      add(tout[u] + 1, x)
    def mask(v)
      ret r = 0
      i = tin[v] + 1
      while i
        r ^= tree[i]
        i -= i & -i

    for u in 0..<n
      toggle(u, bit(s[u]))
    ret ans = []
    for q in queries
      op, a, b = q.split(' ')
      int(a) = a
      if op == 'update'
        toggle(a, bit(s[a]) ^ bit(b))
        s[a] = b
      else
        m = mask(a) ^ mask(int(b)) ^ bit(s[lca(a, int(b))])
        ans <- m & m - 1 == 0
