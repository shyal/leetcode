"""Prototype helpers under test. Each is a candidate builtin."""
from bisect import bisect_left
from collections import deque, defaultdict


def first_true(lo, hi, ok):
    """The smallest x in [lo, hi] with ok(x), assuming ok is False then True; hi + 1 if none."""
    return lo + bisect_left(range(lo, hi + 1), True, key=ok)


def last_true(lo, hi, ok):
    """The largest x in [lo, hi] with ok(x), assuming ok is True then False; lo - 1 if none."""
    return lo + bisect_left(range(lo, hi + 1), True, key=lambda x: not ok(x)) - 1


def nodes(head):
    """Every node of the list from head, in order."""
    while head:
        nxt = head.next
        yield head
        head = nxt


def children(node):
    """The children of node that exist, left before right."""
    return [c for c in (node.left, node.right) if c]


def preorder(root):
    if root:
        yield root
        yield from preorder(root.left)
        yield from preorder(root.right)


def inorder(root):
    if root:
        yield from inorder(root.left)
        yield root
        yield from inorder(root.right)


def postorder(root):
    if root:
        yield from postorder(root.left)
        yield from postorder(root.right)
        yield root


def levels(root):
    """The nodes of each level, top level first."""
    level = [root] if root else []
    while level:
        yield level
        level = [c for node in level for c in children(node)]


def digits(n, base=10):
    """The digits of n in the given base, most significant first."""
    out = []
    while n:
        out.append(n % base)
        n //= base
    return out[::-1] or [0]


def adjacency(edges, n=None, directed=False):
    """adj[u] lists v for every edge (u, v); and u under v unless directed."""
    adj = [[] for _ in range(n)] if n is not None else defaultdict(list)
    for u, v in edges:
        adj[u].append(v)
        if not directed:
            adj[v].append(u)
    return adj


def bfs(adj, *sources):
    """(node, distance) for every node reachable from the sources, nearest first."""
    dist = {s: 0 for s in sources}
    q = deque(sources)
    while q:
        u = q.popleft()
        yield u, dist[u]
        for v in adj[u]:
            if v not in dist:
                dist[v] = dist[u] + 1
                q.append(v)


def toposort(adj):
    """Kahn's algorithm: every node of adj once, sources first; short if there is a cycle."""
    indeg = defaultdict(int)
    for u in adj:
        for v in adj[u]:
            indeg[v] += 1
    q = deque(u for u in adj if indeg[u] == 0)
    while q:
        u = q.popleft()
        yield u
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
