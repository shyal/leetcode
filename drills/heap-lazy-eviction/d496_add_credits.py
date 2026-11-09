"""
EPI 14.11 Add credits

Implement a store of clients and their credits, where each client_id is a
string and each credit is an integer:

    insert(client_id, c): set the credit of client_id to c. A client
        that is already in the store gets the new credit.
    remove(client_id): remove client_id. Return True when it was in the
        store, and False otherwise.
    lookup(client_id): return the credit of client_id, or -1 when it is
        not in the store.
    add_all(C): add C to the credit of every client in the store now.
        A client inserted later does not get C.
    max(): return a client_id with the largest credit, or "" when the
        store is empty. When several clients have that credit, return any
        of them.

Example 1:

Input: insert("ann", 5), insert("bob", 9), add_all(3), lookup("ann"),
       max(), remove("bob"), max(), lookup("bob")
Output: None, None, None, 8, "bob", True, "ann", -1
Explanation: add_all(3) takes ann to 8 and bob to 12.

Example 2:

Input: max(), remove("ann")
Output: "", False

Example 3:

Input: insert("ann", 5), insert("bob", 2), insert("ann", 1), max()
Output: None, None, None, "bob"
Explanation: the third call sets the credit of ann to 1.

Constraints:

    At most 10^5 calls in total.
    -10^9 <= c, C <= 10^9

    REQUIRED: insert and remove in O(log n) time, lookup and add_all in
    O(1) time, and max in O(log n) amortized time, for n calls so far.
    NO loop over all the clients. NO sorting.
"""


class Solution:
    def __init__(self):
        pass

    def insert(self, client_id: str, c: int) -> None:
        pass

    def remove(self, client_id: str) -> bool:
        pass

    def lookup(self, client_id: str) -> int:
        pass

    def add_all(self, C: int) -> None:
        pass

    def max(self) -> str:
        pass


sol = Solution()

sol.insert("ann", 5)
sol.insert("bob", 9)
sol.add_all(3)
print(sol.lookup("ann"), sol.max())  # 8 bob

# assert sol.lookup("ann") == 8
# assert sol.lookup("bob") == 12
# assert sol.max() == "bob"
# assert sol.remove("bob") is True
# assert sol.max() == "ann"
# assert sol.lookup("bob") == -1
# assert sol.remove("bob") is False
# sol.insert("cy", 7)
# assert sol.lookup("cy") == 7
# assert sol.max() == "ann"
# sol.add_all(-10)
# assert sol.lookup("ann") == -2 and sol.lookup("cy") == -3
# assert sol.max() == "ann"
# sol.insert("ann", -100)
# assert sol.max() == "cy"
# sol = Solution()
# assert sol.max() == ""
# assert sol.remove("ann") is False
# assert sol.lookup("ann") == -1
# sol.insert("ann", 5)
# sol.insert("bob", 2)
# sol.insert("ann", 1)
# assert sol.max() == "bob"
# sol.insert("cy", 2)
# assert sol.max() in ("bob", "cy")
# assert sol.remove("bob") is True
# assert sol.max() == "cy"
# assert sol.remove("cy") is True and sol.remove("ann") is True
# assert sol.max() == ""
# sol.insert("dee", 4)
# assert sol.max() == "dee" and sol.lookup("dee") == 4
# sol.remove("dee")
# sol.insert("dee", 4)
# assert sol.max() == "dee"
# sol = Solution()
# sol.insert("zed", 0)
# sol.add_all(10 ** 9)
# sol.insert("amy", 10 ** 9)
# assert sol.max() in ("zed", "amy")
# sol.add_all(1)
# assert sol.lookup("zed") == 10 ** 9 + 1 and sol.lookup("amy") == 10 ** 9 + 1
# sol = Solution()
# ops = [sol.insert(f"c{i}", i) for i in range(10 ** 5 // 2)] + [sol.add_all(1) for _ in range(10 ** 5 // 2)]
# assert sol.lookup("c0") == 10 ** 5 // 2
# assert sol.max() == f"c{10 ** 5 // 2 - 1}"
