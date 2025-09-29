from PrettyPrint import PrettyPrintLinkedList
from rich import print
from Types import ListNode


def build_linked_list(vals):
    dummy = ListNode()
    it = dummy
    for v in vals:
        it.next = ListNode(v)
        it = it.next
    return dummy.next


def print_linked_list(head):
    while head:
        print(head.val, end=(" -> " if head.next else ""))
        head = head.next
    print("")


def get_list_values(head):
    ret = []
    while head:
        ret.append(head.val)
        head = head.next
    return ret


def draw_linked_list(head):
    if not head:
        print("Empty linked list")
        return
    pt = PrettyPrintLinkedList(
        lambda x: x.val,
        lambda x: x.next,
        lambda x: None,
        orientation=PrettyPrintLinkedList.Horizontal,
    )
    pt(head)
