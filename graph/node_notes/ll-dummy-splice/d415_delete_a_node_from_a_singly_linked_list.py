# REFERENCE: d415 EPI 7.6 Delete a node from a singly linked list
class Solution:
    def deletion_from_list(self, node_to_delete):
        node_to_delete.val = node_to_delete.next.val
        node_to_delete.next = node_to_delete.next.next
