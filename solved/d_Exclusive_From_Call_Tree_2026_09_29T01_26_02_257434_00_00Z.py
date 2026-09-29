"""
DRILL: Exclusive From Call Tree

Given an integer n and root, a call tree as built by Call Tree, return
res, where res[i] is the exclusive time of function i. The root's val is
{}. Every other node is one call, with val["id"] the function, and
val["dur"] the whole time of the call, the calls inside it included.
A call's exclusive time is its dur minus the dur of each call directly
inside it. A function's exclusive time is the sum over its calls.

Example 1:

Input: n = 2, root = build_general_tree([{}, [[{"id": 0, "dur": 7}, [[{"id": 1, "dur": 4}, []]]]]])
Output: [3, 4]
Explanation: Call Tree built root from events = [(0, "start", 0), (1, "start", 2), (1, "end", 5), (0, "end", 6)].

    t   0 1 2 3 4 5 6
    0   [===========]
    1       [=====]

        root {}
          |
      id 0, dur 7
          |
      id 1, dur 4

The call of 0 lasts 7 and holds a call of 1 lasting 4: 7 - 4 = 3.

Example 2:

Input: n = 2, root = build_general_tree([{}, [[{"id": 0, "dur": 6}, [[{"id": 0, "dur": 4}, [[{"id": 1, "dur": 2}, []]]]]]]])
Output: [4, 2]
Explanation: Call Tree built root from events = [(0, "start", 0), (0, "start", 1), (1, "start", 2), (1, "end", 3), (0, "end", 4), (0, "end", 5)].

    t   0 1 2 3 4 5
    0   [=========]
    0     [=====]
    1       [=]

        root {}
          |
      id 0, dur 6
          |
      id 0, dur 4
          |
      id 1, dur 2

The outer call of 0 keeps 6 - 4 = 2, the inner call of 0 keeps 4 - 2 = 2, and function 0 gets both.

Example 3:

Input: n = 3, root = build_general_tree([{}, [[{"id": 0, "dur": 6}, [[{"id": 1, "dur": 2}, []], [{"id": 2, "dur": 2}, []]]], [{"id": 1, "dur": 2}, []]]])
Output: [2, 4, 2]
Explanation: Call Tree built root from events = [(0, "start", 0), (1, "start", 1), (1, "end", 2), (2, "start", 3), (2, "end", 4), (0, "end", 5), (1, "start", 6), (1, "end", 7)].

    t   0 1 2 3 4 5 6 7
    0   [=========]
    1     [=]
    2         [=]
    1               [=]

                   root {}
                      |
               +------+------+
               |             |
          id 0, dur 6   id 1, dur 2
               |
         +-----+-----+
         |           |
    id 1, dur 2 id 2, dur 2

Call 0 holds two calls, so it keeps 6 - 2 - 2 = 2. Function 1 gets both of its calls: 2 + 2 = 4.

Constraints:

    1 <= n <= 100
    1 <= number of calls <= 500
    0 <= id < n
    1 <= dur <= 10^9
    A call's dur is at least the sum of the dur of the calls directly inside it.

    REQUIRED: one visit per node, O(number of calls). NO second traversal.
    A call three levels deep must be subtracted from its parent only,
    never from its grandparent; an answer right two levels deep and wrong
    three levels deep is the failure this kills.
---
Learning

This solution is the most intuitive.
"""


# mu 0.6
# def exclusive(n: int, root: Node) -> [int]
#   def visit(node)
#     for child in node.children.values()
#       visit(child)
#     if node is not root
#       res[node.val['id']] += node.val['dur'] - sum for node.children.values(): _.val["dur"]
#   ret res = table(n)
#   visit(root)

def table(*dims, fill=0):
    if len(dims) == 1:
        return [fill] * dims[0]
    if len(dims) == 2:
        return [[fill] * dims[1] for _ in range(dims[0])]
    return [table(*dims[1:], fill=fill) for _ in range(dims[0])]


class Solution:
    def exclusive(self, n: int, root: Node) -> list[int]:
        def visit(node):
            for child in node.children.values():
                visit(child)
            if node is not root:
                res[node.val['id']] += node.val['dur'] - sum(_.val["dur"] for _ in node.children.values())
        res = table(n)
        visit(root)
        return res


sol = Solution()
root = build_general_tree([{}, [[{'id': 0, 'dur': 7}, [[{'id': 1, 'dur': 4}, []]]]]])
draw_general_tree(root)
print(sol.exclusive(2, root))
assert sol.exclusive(2, build_general_tree([{}, [[{'id': 0, 'dur': 7}, [[{'id': 1, 'dur': 4}, []]]]]])) == [3, 4]
assert sol.exclusive(2, build_general_tree([{}, [[{'id': 0, 'dur': 6}, [[{'id': 0, 'dur': 4}, [[{'id': 1, 'dur': 2}, []]]]]]]])) == [4, 2]
assert sol.exclusive(3, build_general_tree([{}, [[{'id': 0, 'dur': 6}, [[{'id': 1, 'dur': 2}, []], [{'id': 2, 'dur': 2}, []]]], [{'id': 1, 'dur': 2}, []]]])) == [2, 4, 2]
assert sol.exclusive(1, build_general_tree([{}, [[{'id': 0, 'dur': 1}, []]]])) == [1]
assert sol.exclusive(2, build_general_tree([{}, [[{'id': 0, 'dur': 1}, []], [{'id': 1, 'dur': 1}, []]]])) == [1, 1]
assert sol.exclusive(1, build_general_tree([{}, [[{'id': 0, 'dur': 8}, [[{'id': 0, 'dur': 4}, []], [{'id': 0, 'dur': 1}, []]]]]])) == [8]
assert sol.exclusive(3, build_general_tree([{}, [[{'id': 0, 'dur': 4}, [[{'id': 1, 'dur': 1}, []], [{'id': 2, 'dur': 1}, []]]]]])) == [2, 1, 1]
assert sol.exclusive(1, build_general_tree([{}, [[{'id': 0, 'dur': 6}, [[{'id': 0, 'dur': 4}, [[{'id': 0, 'dur': 2}, []]]]]]]])) == [6]
assert sol.exclusive(2, build_general_tree([{}, [[{'id': 1, 'dur': 1000000000}, [[{'id': 0, 'dur': 1}, []]]]]])) == [1, 999999999]
