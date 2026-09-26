"""
DRILL: Call Tree

Given events, a list of function calls in time order, each a tuple
(id, op, t) with op "start" or "end", return the root of the call tree.
The root is a Node whose val is {}. A start at t adds
Node({"id": id, "start": t}) as the next child of the innermost call
still running. The matching end at t sets that node's val["dur"] to
t - start + 1, since a call runs from the beginning of second start to
the end of second t.

Example 1:

Input: events = [(0, "start", 0), (1, "start", 2), (1, "end", 5), (0, "end", 6)]
Output: [{}, [[{"id": 0, "start": 0, "dur": 7}, [[{"id": 1, "start": 2, "dur": 4}, []]]]]]
Explanation: Call 1 starts while call 0 runs, so it is call 0's child. Shown in the nested form of get_general_tree: [val, [children]].

Example 2:

Input: events = [(0, "start", 0), (0, "end", 0), (1, "start", 1), (1, "end", 1)]
Output: [{}, [[{"id": 0, "start": 0, "dur": 1}, []], [{"id": 1, "start": 1, "dur": 1}, []]]]
Explanation: Call 0 has ended when call 1 starts, so both are children of the root.

Constraints:

    2 <= len(events) <= 500
    0 <= id <= 100
    0 <= t <= 10^9
    Every start has a matching end, and the innermost running call ends first.
    No two starts share a t, and no two ends share a t.

    REQUIRED: one pass, O(len(events)). NO second pass over events. A
    start's parent is the innermost call still running, not the last
    call started; after an end, the next start belongs one level up.
"""


class Solution:

    def callTree(self, events: List[Tuple[int, str, int]]) -> Node:
        pass


sol = Solution()

draw_general_tree(
    sol.callTree([(0, "start", 0), (1, "start", 2), (1, "end", 5), (0, "end", 6)])
)
print(
    get_general_tree(
        sol.callTree([(0, "start", 0), (1, "start", 2), (1, "end", 5), (0, "end", 6)])
    )
)  # [{}, [[{'id': 0, 'start': 0, 'dur': 7}, [[{'id': 1, 'start': 2, 'dur': 4}, []]]]]]

# assert get_general_tree(
#     sol.callTree([(0, "start", 0), (1, "start", 2), (1, "end", 5), (0, "end", 6)])
# ) == [{}, [[{"id": 0, "start": 0, "dur": 7}, [[{"id": 1, "start": 2, "dur": 4}, []]]]]]
# assert get_general_tree(
#     sol.callTree([(0, "start", 0), (0, "end", 0), (1, "start", 1), (1, "end", 1)])
# ) == [{}, [[{"id": 0, "start": 0, "dur": 1}, []], [{"id": 1, "start": 1, "dur": 1}, []]]]
# assert get_general_tree(
#     sol.callTree(
#         [(0, "start", 0), (0, "start", 1), (1, "start", 2), (1, "end", 3), (0, "end", 4), (0, "end", 5)]
#     )
# ) == [
#     {},
#     [[{"id": 0, "start": 0, "dur": 6}, [[{"id": 0, "start": 1, "dur": 4}, [[{"id": 1, "start": 2, "dur": 2}, []]]]]]],
# ]
# assert get_general_tree(sol.callTree([(0, "start", 0), (0, "end", 0)])) == [
#     {},
#     [[{"id": 0, "start": 0, "dur": 1}, []]],
# ]
# assert get_general_tree(sol.callTree([(3, "start", 5), (3, "end", 1000000000)])) == [
#     {},
#     [[{"id": 3, "start": 5, "dur": 999999996}, []]],
# ]
# assert get_general_tree(
#     sol.callTree(
#         [(0, "start", 0), (1, "start", 1), (1, "end", 1), (2, "start", 2), (2, "end", 2), (0, "end", 3)]
#     )
# ) == [
#     {},
#     [
#         [
#             {"id": 0, "start": 0, "dur": 4},
#             [[{"id": 1, "start": 1, "dur": 1}, []], [{"id": 2, "start": 2, "dur": 1}, []]],
#         ]
#     ],
# ]
