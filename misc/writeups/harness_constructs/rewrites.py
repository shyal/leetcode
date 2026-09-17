import sys; sys.path.insert(0, __import__('os').path.dirname(__file__))
from proto import *

# 1760. Minimum Limit of Balls in a Bag: 11 lines -> 3
class S1760:
    def minimumSize(self, nums, maxOperations):
        ops = lambda cap: sum(ceil_div(n, cap) - 1 for n in nums)
        return first_true(1, max(nums), lambda cap: ops(cap) <= maxOperations)
s = S1760()
assert s.minimumSize([9], 2) == 3
assert s.minimumSize([2,4,8,2], 4) == 2
assert s.minimumSize([7,17], 2) == 7

# 1539. Kth Missing Positive Number: 9 lines -> 2
class S1539:
    def findKthPositive(self, arr, k):
        return first_true(0, len(arr) - 1, lambda i: arr[i] - i - 1 >= k) + k
s = S1539()
assert s.findKthPositive([2,3,4,7,11], 5) == 9
assert s.findKthPositive([1,2,3,4], 2) == 6

# 102. Binary Tree Level Order Traversal: 11 lines -> 1
class S102:
    def levelOrder(self, root):
        return [[n.val for n in level] for level in levels(root)]
s = S102()
assert s.levelOrder(build_tree([3,9,20,None,None,15,7])) == [[3],[9,20],[15,7]]
assert s.levelOrder(None) == []

# 1281. Subtract the Product and Sum of Digits: 8 lines -> 2
class S1281:
    def subtractProductAndSum(self, n):
        return prod(digits(n)) - sum(digits(n))
s = S1281()
assert s.subtractProductAndSum(234) == 15
assert s.subtractProductAndSum(4421) == 21

# 1290. Convert Binary Number in a Linked List: 6 lines -> 1
class S1290:
    def getDecimalValue(self, head):
        return int("".join(str(n.val) for n in nodes(head)), 2)
s = S1290()
assert s.getDecimalValue(build_linked_list([1,0,1])) == 5
assert s.getDecimalValue(build_linked_list([0])) == 0

# 210. Course Schedule II: 30 lines -> 3
class S210:
    def findOrder(self, numCourses, prerequisites):
        adj = adjacency(((b, a) for a, b in prerequisites), numCourses, directed=True)
        order = list(toposort(dict(enumerate(adj))))
        return order if len(order) == numCourses else []
s = S210()
assert s.findOrder(2, [[1,0]]) == [0,1]
assert s.findOrder(4, [[1,0],[2,0],[3,1],[3,2]]) in ([0,1,2,3],[0,2,1,3])
assert s.findOrder(2, [[0,1],[1,0]]) == []

# 994. Rotting Oranges via bfs over an adjacency view is not the fit; grid_bfs already exists.
# 743. Network Delay Time: check bfs shape on a graph
class S1971:  # 1971. Find if Path Exists in Graph
    def validPath(self, n, edges, source, destination):
        return any(u == destination for u, _ in bfs(adjacency(edges, n), source))
s = S1971()
assert s.validPath(3, [[0,1],[1,2],[2,0]], 0, 2) == True
assert s.validPath(6, [[0,1],[0,2],[3,5],[5,4],[4,3]], 0, 5) == False

# 104. Maximum Depth: postorder is not needed, levels is
class S104:
    def maxDepth(self, root):
        return sum(1 for _ in levels(root))
assert S104().maxDepth(build_tree([3,9,20,None,None,15,7])) == 3

# 94. Inorder
class S94:
    def inorderTraversal(self, root):
        return [n.val for n in inorder(root)]
assert S94().inorderTraversal(build_tree([1,None,2,3])) == [1,3,2]
print("all rewrites pass")
