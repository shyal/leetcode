from typing import List, Optional, Dict, Any


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

    def __repr__(self):
        vals = []
        it = self
        seen = set()
        while it:
            if it in seen:
                break
            seen.add(it)
            vals.append(str(it.val))
            it = it.next
        return "->".join(vals)


class GraphNode:
    def __init__(self, val=0, neighbors=None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []

    def __repr__(self):
        return f"{self.val} -> ..."


class Node:
    def __init__(self, val: Any, children: Dict[Any, "Node"] = {}):
        self.val = val
        self.children = children


# class Node:
#     def __init__(
#         self, val: Optional[int] = None, children: Optional[List["Node"]] = None
#     ):
#         self.val = val
#         self.children = children if children is not None else []
