"""
URL: https://leetcode.com/problems/serialize-and-deserialize-binary-tree/description/?envType=problem-list-v2&envId=vn57k9wr

297. Serialize and Deserialize Binary Tree

Serialization is the process of converting a data structure or object into a sequence of bits so that it can be stored in a file or memory buffer, or transmitted across a network connection link to be reconstructed later in the same or another computer environment.

Design an algorithm to serialize and deserialize a binary tree. There is no restriction on how your serialization/deserialization algorithm should work. You just need to ensure that a binary tree can be serialized to a string and this string can be deserialized to the original tree structure.

Clarification: The input/output format is the same as how LeetCode serializes a binary tree. You do not necessarily need to follow this format, so please be creative and come up with different approaches yourself.

Example 1:

Input: root = [1,2,3,null,null,4,5]
Output: [1,2,3,null,null,4,5]

Example 2:

Input: root = []
Output: []

Constraints:

    The number of nodes in the tree is in the range [0, 10^4].
    -1000 <= Node.val <= 1000

---

An old solution of mine. Re-learning.

Serialization: we just append onto a list, pre-order, as long as n
exists. If it doesn't we hit the base case by appending null.

Deserialization: We do this in reverse. We split the string (,),
ignore the first and last empty items, and build an iter.
In the helper, we call next on the iter to avoid index juggling,
base case immediately: if val is null, we return.

Else we build the node, and recursively construct its left and right
by calling the helper and assigning its results.

"""


class Solution:

    def serialize(self, root):
        def helper(n):
            if n:
                out.append(str(n.val))
                helper(n.left)
                helper(n.right)
            else:
                out.append("null")

        out = []
        helper(root)
        return f'[{",".join(out)}]'

    def deserialize(self, data):
        def helper():
            val = next(A, None)
            if val == "null":
                return None
            node = TreeNode(val)
            node.left = helper()
            node.right = helper()
            return node

        A = iter(data[1:-1].split(","))
        return helper()


sol = Solution()

# Example 1
root1 = build_tree([1, 2, 3, None, None, 4, 5])
draw_tree(root1)
serialized1 = sol.serialize(root1)
print(serialized1)  # "1,2,3,null,null,4,5"
deserialized1 = sol.deserialize(serialized1)
# assert get_level_order(deserialized1) == [1, 2, 3, None, None, 4, 5]

# # Example 2
# root2 = build_tree([])
# serialized2 = sol.serialize(root2)
# print(serialized2)  # ""
# deserialized2 = sol.deserialize(serialized2)
# assert get_level_order(deserialized2) == []

# assert get_level_order(sol.deserialize(sol.serialize(build_tree([0])))) == [0]
# assert get_level_order(sol.deserialize(sol.serialize(build_tree([-1, -1, -1])))) == [
#     -1,
#     -1,
#     -1,
# ]
# assert get_level_order(sol.deserialize(sol.serialize(build_tree([1] * 10)))) == [
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
# ]
# assert get_level_order(
#     sol.deserialize(sol.serialize(build_tree([i for i in range(15)])))
# ) == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
# assert get_level_order(
#     sol.deserialize(sol.serialize(build_tree([1000, None, -1000])))
# ) == [1000, None, -1000]
# assert get_level_order(
#     sol.deserialize(
#         sol.serialize(build_tree([i if i % 2 == 0 else None for i in range(20)]))
#     )
# ) == [
#     0,
#     None,
#     2,
#     None,
#     4,
#     None,
#     6,
#     None,
#     8,
#     None,
#     10,
#     None,
#     12,
#     None,
#     14,
#     None,
#     16,
#     None,
#     18,
# ]
# assert get_level_order(
#     sol.deserialize(sol.serialize(build_tree([0, None, 0, None, None, 0])))
# ) == [0, None, 0]
# assert get_level_order(
#     sol.deserialize(sol.serialize(build_tree([1, 2, None, 3, None, 4, None, 5])))
# ) == [1, 2, None, 3, None, 4, None, 5]


# FAILED: walked away after 40m 0s; no working solution.
# Judge the moves actually attempted as struggled, not clean.
