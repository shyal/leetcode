"""
In this file we'll cover the various visualization helpers / utils available.
"""

print("Draw a linked list:")
list1 = build_linked_list([1, 2, 3])
draw_linked_list(list1)
print("-" * 50)

print("Draw a tree:")
tree = build_tree([1, 2, 3, 4, 5, None, 8, None, None, 6, 7, 9])
draw_tree(tree)
print("-" * 50)

print("Draw general tree")
tree = Node(0, children=[Node(1), Node(2), Node(3)])
draw_general_tree(tree)
print("-" * 50)

print("Draw heap")
heap = [1, 2, 3, 4, 5]
heapify(heap)
draw_heap(heap)
print("-" * 50)

print("Draw graph")
edges = [[0, 1], [0, 2], [0, 3], [1, 2], [1, 3], [2, 3], [8, 9], [10, 12]]
G = build_graph_from_edge_list(edges)
draw_graphviz(edges)
print("-" * 50)

print("Draw graph, duck typing")
edges = [[0, 1], [0, 2], [0, 3], [1, 2], [1, 3], [2, 3], [8, 9], [10, 12]]
draw_graphviz(edges)
print("-" * 50)
