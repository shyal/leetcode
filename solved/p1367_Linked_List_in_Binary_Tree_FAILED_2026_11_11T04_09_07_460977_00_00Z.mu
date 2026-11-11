# URL: https://leetcode.com/problems/linked-list-in-binary-tree/description/?envType=problem-list-v2&envId=vn57k9wr
#
# 1367. Linked List in Binary Tree
#
# Given a binary tree root and a linked list with head as the first node.
#
# Return True if all the elements in the linked list starting from the head correspond to some downward path connected in the binary tree otherwise return False.
#
# In this context downward path means a path that starts at some node and goes downwards.
#
# Example 1:
#
# Input: head = [4,2,8], root = [1,4,4,null,2,2,null,1,null,6,8,null,null,null,null,1,3]
# Output: true
# Explanation: Nodes in blue form a subpath in the binary Tree.
#
# Example 2:
#
# Input: head = [1,4,2,6], root = [1,4,4,null,2,2,null,1,null,6,8,null,null,null,null,1,3]
# Output: true
#
# Example 3:
#
# Input: head = [1,4,2,6,8], root = [1,4,4,null,2,2,null,1,null,6,8,null,null,null,null,1,3]
# Output: false
# Explanation: There is no path in the binary tree that contains all the elements of the linked list from head.
#
# Constraints:
#
#     The number of nodes in the tree will be in the range [1, 2500].
#     The number of nodes in the list will be in the range [1, 100].
#     1 <= Node.val <= 100 for each node in the linked list and binary tree.
#
# ---
# LEETCODE: Time Limit Exceeded (43/68 cases)

# mu 0.17

class Solution
  def isSubPath(head: ListNode?, root: TreeNode?) -> bool
    self.found, curr, tail = false, head, none
    while curr
      if curr.next is none
        tail = curr
      curr = curr.next
    {
      (tn, ln) ->
        if not tn or not ln
          return
        match_curr = tn.val == ln.val
        match_head = tn.val == head.val
        if match_curr and ln == tail
          self.found = true
          return
        if match_head
          mu(tn.left, head.next)
          mu(tn.right, head.next)
        if match_curr
          mu(tn.left, ln.next)
          mu(tn.right, ln.next)
        else
          mu(tn.left, head)
          mu(tn.right, head)
    }(root, head)
    self.found

sol = Solution()

tree = build_tree([1, none, 1, 10, 1, 9])
print(tree)
assert sol.isSubPath(build_linked_list([1, 10]), tree) == true



assert sol.isSubPath(build_linked_list([4, 2, 8]), build_tree([1, 4, 4, none, 2, 2, none, 1, none, 6, 8, none, none, none, none, 1, 3])) == true
assert sol.isSubPath(build_linked_list([1, 4, 2, 6]), build_tree([1, 4, 4, none, 2, 2, none, 1, none, 6, 8, none, none, none, none, 1, 3])) == true
assert sol.isSubPath(build_linked_list([1, 4, 2, 6, 8]), build_tree([1, 4, 4, none, 2, 2, none, 1, none, 6, 8, none, none, none, none, 1, 3])) == false
assert sol.isSubPath(build_linked_list([1]), build_tree([1])) == true
assert sol.isSubPath(build_linked_list([1]), build_tree([2])) == false
assert sol.isSubPath(build_linked_list([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]), build_tree([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])) == false
assert sol.isSubPath(build_linked_list([10, 9, 8, 7, 6, 5, 4, 3, 2, 1]), build_tree([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])) == false
assert sol.isSubPath(build_linked_list([1, 1, 1]), build_tree([1, 1, 1, 1, 1, none, 1])) == true
assert sol.isSubPath(build_linked_list([-1, -2, -3]), build_tree([-1, -2, -3, none, none, -3])) == false
assert sol.isSubPath(build_linked_list([100] * 100), build_tree([100] * 2500)) == false
assert sol.isSubPath(build_linked_list([1, 2, 3]), build_tree([1, none, 2, none, 3])) == true
assert sol.isSubPath(build_linked_list([2, 2, 2]), build_tree([2, 2, none, 2, none, 2])) == true
assert sol.isSubPath(build_linked_list([1]), build_tree([1, none, none, 1, none, none, 1])) == true
assert sol.isSubPath(build_linked_list([1, 2, 3, 4, 5]), build_tree([1, 2, 3, 4, 5])) == false
assert sol.isSubPath(build_linked_list([1, 2, 3, 4, 5]), build_tree([5, 4, 3, 2, 1])) == false
assert sol.isSubPath(build_linked_list([4, 2]), build_tree([4, 4, 4, 1, none, none, none, 2])) == false
assert sol.isSubPath(build_linked_list([1, 10]), build_tree([1, none, 1, 10, 1, 9])) == true


# FAILED: walked away after 38m 45s; no working solution.
# Judge the move the defect is in as struggled, not clean. A move the code never reached gets no verdict.
