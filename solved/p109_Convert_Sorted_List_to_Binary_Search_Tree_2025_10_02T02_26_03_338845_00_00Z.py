"""
URL: https://leetcode.com/problems/convert-sorted-list-to-binary-search-tree/description/

109. Convert Sorted List to Binary Search Tree

Given the head of a singly linked list where elements are sorted in ascending order, convert it to a height-balanced binary search tree.


Example 1:

Input: head = [-10,-3,0,5,9]
Output: [0,-3,9,-10,null,5]
Explanation: One possible answer is [0,-3,9,-10,null,5], which represents the shown height balanced BST.

Example 2:

Input: head = []
Output: []


Constraints:

    The number of nodes in head is in the range [0, 2 * 104].
    -105 <= Node.val <= 105

---

Interesting challenge. Quite tricky as i'm not even sure i can built a balanced BST with a sorted list. Might be worth working on that first before working with the linked list.

Ok i guess to build a BST with a sorted list, one starts from the middle, adds that as a node, then uses the left and right subarrays recursively. So i could simply convert the LL to an array, but that's extra space.

If i pass the middle of the LL, then i'll have to iterate over and over to find the mid point for the sublists, so that's less time efficient. I think i'll go with O(N) space, and keep time efficient.

Hmm tricky to decide between time and space on this one. Both seem interesting, though constant space sounds like the more 'fun' approach, while O(N) space is less interesting.

Ah NVM let's keep it simple first. So O(N) space.

Ok so i guess this can be done in O(N)

Ok solved. This definitely felt easy.

"""


class Solution:
    def sortedListToBST(self, head: Optional[ListNode]) -> Optional[TreeNode]:
        vals = []
        it = head
        while it:
            vals.append(it.val)
            it = it.next

        def dfs(left, right):
            if left > right:
                return
            mid = (left + right) // 2
            val = vals[mid]
            node = TreeNode(val)
            node.left = dfs(left, mid - 1)
            node.right = dfs(mid + 1, right)
            return node

        return dfs(0, len(vals) - 1)


sol = Solution()
head = build_linked_list([-10, -3, 0, 5, 9])
draw_linked_list(head)
values = get_list_values(head)
tree = sol.sortedListToBST(head)
draw_tree(tree)
assert get_inorder(tree) == values
assert is_valid_bst(tree)
assert is_balanced(tree)

head = build_linked_list([])
draw_linked_list(head)
values = get_list_values(head)
tree = sol.sortedListToBST(head)
draw_tree(tree)
assert get_inorder(tree) == values
assert is_valid_bst(tree)
assert is_balanced(tree)

sol = Solution()
head = build_linked_list([-10, -3, 0, 5, 9])
values = get_list_values(head)
tree = sol.sortedListToBST(head)
assert get_inorder(tree) == values
assert is_valid_bst(tree)
assert is_balanced(tree)

head = build_linked_list([])
values = get_list_values(head)
tree = sol.sortedListToBST(head)
assert get_inorder(tree) == values
assert is_valid_bst(tree)
assert is_balanced(tree)

sol = Solution()
head = build_linked_list([0])
values = get_list_values(head)
tree = sol.sortedListToBST(head)
assert get_inorder(tree) == values
assert is_valid_bst(tree)
assert is_balanced(tree)

sol = Solution()
head = build_linked_list([-1, 1])
values = get_list_values(head)
tree = sol.sortedListToBST(head)
assert get_inorder(tree) == values
assert is_valid_bst(tree)
assert is_balanced(tree)

sol = Solution()
head = build_linked_list([-1, 0, 1])
values = get_list_values(head)
tree = sol.sortedListToBST(head)
assert get_inorder(tree) == values
assert is_valid_bst(tree)
assert is_balanced(tree)

sol = Solution()
head = build_linked_list([-5, -3, -1])
values = get_list_values(head)
tree = sol.sortedListToBST(head)
assert get_inorder(tree) == values
assert is_valid_bst(tree)
assert is_balanced(tree)

sol = Solution()
head = build_linked_list([1, 3, 5])
values = get_list_values(head)
tree = sol.sortedListToBST(head)
assert get_inorder(tree) == values
assert is_valid_bst(tree)
assert is_balanced(tree)

sol = Solution()
head = build_linked_list([1, 2, 3, 4])
values = get_list_values(head)
tree = sol.sortedListToBST(head)
assert get_inorder(tree) == values
assert is_valid_bst(tree)
assert is_balanced(tree)

sol = Solution()
head = build_linked_list([1, 2, 3, 4, 5])
values = get_list_values(head)
tree = sol.sortedListToBST(head)
assert get_inorder(tree) == values
assert is_valid_bst(tree)
assert is_balanced(tree)

sol = Solution()
head = build_linked_list([-100000, -50000, 0, 50000, 100000])
values = get_list_values(head)
tree = sol.sortedListToBST(head)
assert get_inorder(tree) == values
assert is_valid_bst(tree)
assert is_balanced(tree)
