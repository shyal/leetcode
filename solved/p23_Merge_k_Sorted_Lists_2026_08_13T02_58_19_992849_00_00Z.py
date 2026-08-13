"""
URL: https://leetcode.com/problems/merge-k-sorted-lists/description/?envType=problem-list-v2&envId=vn57k9wr

23. Merge k Sorted Lists

You are given an array of k linked-lists lists, each linked-list is sorted in
ascending order.

Merge all the linked-lists into one sorted linked-list and return it.


Example 1:

Input: lists = [[1,4,5],[1,3,4],[2,6]]
Output: [1,1,2,3,4,4,5,6]
Explanation: The linked-lists are:
[
  1->4->5,
  1->3->4,
  2->6
]
merging them into one sorted linked list:
1->1->2->3->4->4->5->6

Example 2:

Input: lists = []
Output: []

Example 3:

Input: lists = [[]]
Output: []


Constraints:

    k == lists.length
    0 <= k <= 10^4
    0 <= lists[i].length <= 500
    -10^4 <= lists[i][j] <= 10^4
    lists[i] is sorted in ascending order.
    The sum of lists[i].length will not exceed 10^4.

---

Clean solve. Easy peasy.

"""
from random import randint

class Solution:
    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        rand = lambda: randint(0, int(1e12))
        h = [(n.val, rand(), n) for n in lists if n]
        heapify(h)
        def get_next():
            if h:
                _, _, node = heappop(h)
                if node.next:
                    heappush(h, (node.next.val, rand(), node.next))
                    node.next = None
                return node
        head = ListNode()
        curr = head
        while curr:
            curr.next = get_next()
            curr = curr.next
        return head.next


def build_lists(arrs):
    return [build_linked_list(a) for a in arrs]


sol = Solution()

# print(get_list_values(sol.mergeKLists(build_lists([[1, 4, 5], [1, 3, 4], [2, 6]]))))  # [1, 1, 2, 3, 4, 4, 5, 6]

assert get_list_values(sol.mergeKLists(build_lists([[1, 4, 5], [1, 3, 4], [2, 6]]))) == [1, 1, 2, 3, 4, 4, 5, 6]
assert get_list_values(sol.mergeKLists(build_lists([]))) == []
assert get_list_values(sol.mergeKLists(build_lists([[]]))) == []
assert get_list_values(sol.mergeKLists(build_lists([[], []]))) == []
assert get_list_values(sol.mergeKLists(build_lists([[1]]))) == [1]
assert get_list_values(sol.mergeKLists(build_lists([[0]]))) == [0]
assert get_list_values(sol.mergeKLists(build_lists([[2], [1]]))) == [1, 2]
assert get_list_values(sol.mergeKLists(build_lists([[], [1], []]))) == [1]
assert get_list_values(sol.mergeKLists(build_lists([[-10000, 10000]]))) == [-10000, 10000]
assert get_list_values(sol.mergeKLists(build_lists([[-1, 0, 1], [-2, 2]]))) == [-2, -1, 0, 1, 2]
assert get_list_values(sol.mergeKLists(build_lists([[-3, -1], [-2, 0]]))) == [-3, -2, -1, 0]
assert get_list_values(sol.mergeKLists(build_lists([[5, 5, 5], [5, 5]]))) == [5, 5, 5, 5, 5]
assert get_list_values(sol.mergeKLists(build_lists([[1, 1], [1], [1, 1, 1]]))) == [1, 1, 1, 1, 1, 1]
assert get_list_values(sol.mergeKLists(build_lists([[1, 2, 3], [4, 5, 6], [7, 8, 9]]))) == [1, 2, 3, 4, 5, 6, 7, 8, 9]
assert get_list_values(sol.mergeKLists(build_lists([[7, 8, 9], [4, 5, 6], [1, 2, 3]]))) == [1, 2, 3, 4, 5, 6, 7, 8, 9]
assert get_list_values(sol.mergeKLists(build_lists([[1, 3, 5, 7], [2, 4, 6, 8]]))) == [1, 2, 3, 4, 5, 6, 7, 8]
assert get_list_values(sol.mergeKLists(build_lists([[10], [1, 2, 3, 4, 5, 6, 7, 8, 9]]))) == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
assert get_list_values(sol.mergeKLists(build_lists([[-10000], [10000], [0]]))) == [-10000, 0, 10000]