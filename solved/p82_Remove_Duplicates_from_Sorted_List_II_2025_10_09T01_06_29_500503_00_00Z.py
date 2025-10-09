"""
URL: https://leetcode.com/problems/remove-duplicates-from-sorted-list-ii/description/

82. Remove Duplicates from Sorted List II

Given the head of a sorted linked list, delete all nodes that have duplicate numbers, leaving only distinct numbers from the original list. Return the linked list sorted as well.

Example 1:

Input: head = [1,2,3,3,4,4,5]
Output: [1,2,5]

Example 2:

Input: head = [1,1,1,2,3]
Output: [2,3]

Constraints:

    The number of nodes in the list is in the range [0, 300].
    -100 <= Node.val <= 100
    The list is guaranteed to be sorted in ascending order.

---
Started solving the wrong question. Didn't realise duplicates had to go
entirely. Will revisit later.

"""


class Solution:
    def deleteDuplicates(self, head: Optional[ListNode]) -> Optional[ListNode]:
        pass


sol = Solution()

# print(
#     get_list_values(sol.deleteDuplicates(build_linked_list([1, 2, 3, 3, 4, 4, 5])))
# )  # [1,2,5]

# assert get_list_values(sol.deleteDuplicates(build_linked_list([1,2,3,3,4,4,5]))) == [1,2,5]
# assert get_list_values(sol.deleteDuplicates(build_linked_list([1,1,1,2,3]))) == [2,3]
# assert get_list_values(sol.deleteDuplicates(build_linked_list([]))) == []
# assert get_list_values(sol.deleteDuplicates(build_linked_list([5]))) == [5]
# assert get_list_values(sol.deleteDuplicates(build_linked_list([1,2,3,4]))) == [1,2,3,4]
# assert get_list_values(sol.deleteDuplicates(build_linked_list([7,7,7,7]))) == []
# assert get_list_values(sol.deleteDuplicates(build_linked_list([1,1,2,3]))) == [2,3]
# assert get_list_values(sol.deleteDuplicates(build_linked_list([1,2,3,3]))) == [1,2]
# assert get_list_values(sol.deleteDuplicates(build_linked_list([1,1,2,2,3,3,4]))) == [4]
# assert get_list_values(sol.deleteDuplicates(build_linked_list([1,2,2]))) == [1]
# assert get_list_values(sol.deleteDuplicates(build_linked_list([-1,-1,0,1,1]))) == [0]
# assert get_list_values(sol.deleteDuplicates(build_linked_list([0,0,0]))) == []
# assert get_list_values(sol.deleteDuplicates(build_linked_list([-100, -100, 100]))) == [100]
# assert get_list_values(sol.deleteDuplicates(build_linked_list([1,2,3,4,4,5,6]))) == [1,2,3,5,6]
