# URL: https://leetcode.com/problems/swap-nodes-in-pairs/description/?envType=problem-list-v2&envId=vn57k9wr
#
# 24. Swap Nodes in Pairs
#
# Given a linked list, swap every two adjacent nodes and return its head. You must solve the problem without modifying the values in the list's nodes (i.e., only nodes themselves may be changed).
#
# Example 1:
#
# Input: head = [1,2,3,4]
# Output: [2,1,4,3]
# Explanation:
#
# Example 2:
#
# Input: head = []
# Output: []
#
# Example 3:
#
# Input: head = [1]
# Output: [1]
#
# Example 4:
#
# Input: head = [1,2,3]
# Output: [2,1,3]
#
# Constraints:
#
#     The number of nodes in the list is in the range [0, 100].
#     0 <= Node.val <= 100
#
# ---
# Learning

# mu 0.16

class Solution
  def swapPairs(head: ListNode?) -> ListNode?
    if not head or not head.next
      return head
    m, c = head, head.next
    m.next, c.next = self.swapPairs(c.next), m
    c

sol = Solution()

head = build_linked_list([1, 2, 3, 4])
print(head)

print(get_list_values(sol.swapPairs(head)))  # [2,1,4,3]

assert get_list_values(sol.swapPairs(build_linked_list([1, 2, 3, 4]))) == [2, 1, 4, 3]
assert get_list_values(sol.swapPairs(build_linked_list([]))) == []
assert get_list_values(sol.swapPairs(build_linked_list([1]))) == [1]
assert get_list_values(sol.swapPairs(build_linked_list([1, 2, 3]))) == [2, 1, 3]
assert get_list_values(sol.swapPairs(build_linked_list([0, 0, 0, 0]))) == [0, 0, 0, 0]
assert get_list_values(sol.swapPairs(build_linked_list([100, 99, 98, 97, 96, 95]))) == [99, 100, 97, 98, 95, 96]
assert get_list_values(sol.swapPairs(build_linked_list([1, 1, 1, 1, 1]))) == [1, 1, 1, 1, 1]
assert get_list_values(sol.swapPairs(build_linked_list([-1, -2, -3, -4]))) == [-2, -1, -4, -3]
assert get_list_values(sol.swapPairs(build_linked_list([1] * 100))) == [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
assert get_list_values(sol.swapPairs(build_linked_list(list(0..<100)))) == [1, 0, 3, 2, 5, 4, 7, 6, 9, 8, 11, 10, 13, 12, 15, 14, 17, 16, 19, 18, 21, 20, 23, 22, 25, 24, 27, 26, 29, 28, 31, 30, 33, 32, 35, 34, 37, 36, 39, 38, 41, 40, 43, 42, 45, 44, 47, 46, 49, 48, 51, 50, 53, 52, 55, 54, 57, 56, 59, 58, 61, 60, 63, 62, 65, 64, 67, 66, 69, 68, 71, 70, 73, 72, 75, 74, 77, 76, 79, 78, 81, 80, 83, 82, 85, 84, 87, 86, 89, 88, 91, 90, 93, 92, 95, 94, 97, 96, 99, 98]
assert get_list_values(sol.swapPairs(build_linked_list([2]))) == [2]
assert get_list_values(sol.swapPairs(build_linked_list([1, 2]))) == [2, 1]
assert get_list_values(sol.swapPairs(build_linked_list([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]))) == [2, 1, 4, 3, 6, 5, 8, 7, 10, 9]
assert get_list_values(sol.swapPairs(build_linked_list([10, 9, 8, 7, 6, 5, 4, 3, 2, 1]))) == [9, 10, 7, 8, 5, 6, 3, 4, 1, 2]
assert get_list_values(sol.swapPairs(build_linked_list([0]))) == [0]
assert get_list_values(sol.swapPairs(build_linked_list([100]))) == [100]
