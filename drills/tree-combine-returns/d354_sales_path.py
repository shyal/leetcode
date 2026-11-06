"""
Given the root rootNode of a tree in which every node holds a cost in
node.val and a list of children in node.children, return the smallest
cost of a path from the root to a leaf. The cost of a path is the sum
of the costs of its nodes, the root and the leaf included.

Example 1:

Input: rootNode = the root of

              0
         ┌────┼────┐
         5    3    6
         │   ┌┴┐  ┌┴┐
         4   2 0  1 5
             │ │
             1 10

Output: 6
Explanation: the path 0, 3, 2, 1. The path 0, 3, 0 is cheaper at the
second level, but its leaf 10 makes it 13.

Example 2:

Input: rootNode = a single node with val 7
Output: 7

Example 3:

Input: rootNode = the root of

          0
        ┌─┴─┐
        5   3
        │
        4

Output: 3
Explanation: the leaf 3 is one step down. The path 0, 5, 4 costs 9.

Constraints:

    1 <= number of nodes <= 10^3
    0 <= node.val <= 10^5

    REQUIRED: O(number of nodes) time. NO list of every root-to-leaf
    path.
"""


class Solution:
    def get_cheapest_cost(self, rootNode: Node) -> int:
        pass


sol = Solution()

t = Node(0, [Node(5, [Node(4)]), Node(3, [Node(2, [Node(1)]), Node(0, [Node(10)])]), Node(6, [Node(1), Node(5)])])
draw_general_tree(t)
print(sol.get_cheapest_cost(t))  # 6

# assert sol.get_cheapest_cost(t) == 6
# assert sol.get_cheapest_cost(Node(7)) == 7
# assert sol.get_cheapest_cost(Node(0, [Node(5, [Node(4)]), Node(3)])) == 3
# assert sol.get_cheapest_cost(Node(0)) == 0
# assert sol.get_cheapest_cost(Node(0, [Node(5, [Node(4)]), Node(3, [Node(2, [Node(1)]), Node(0)]), Node(6, [Node(1), Node(5)])])) == 3
# assert sol.get_cheapest_cost(Node(0, [Node(5, [Node(4)]), Node(3, [Node(2, [Node(1, [Node(1)])]), Node(0, [Node(10)])]), Node(6, [Node(1), Node(5)])])) == 7
# assert sol.get_cheapest_cost(Node(0, [Node(5, [Node(4)]), Node(3, [Node(2, [Node(1, [Node(1, [Node(4)])])]), Node(0, [Node(10)])]), Node(6, [Node(3), Node(5)])])) == 9
# assert sol.get_cheapest_cost(Node(1, [Node(1, [Node(1, [Node(1)])]), Node(100)])) == 4
# assert sol.get_cheapest_cost(Node(10 ** 5, [Node(10 ** 5), Node(10 ** 5)])) == 2 * 10 ** 5
# chain = reduce(lambda node, _: Node(1, [node]), range(499), Node(1))
# assert sol.get_cheapest_cost(chain) == 500
