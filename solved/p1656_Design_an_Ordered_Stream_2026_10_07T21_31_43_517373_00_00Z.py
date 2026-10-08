# combo chain: backend, problem 2 of 10. Run `make combos backend` to see
# the chain and what is done this lap; the chain is saved in graph/chains/backend.json.
"""
URL: https://leetcode.com/problems/design-an-ordered-stream/description/?envType=problem-list-v2&envId=vn57k9wr

1656. Design an Ordered Stream

There is a stream of n (idKey, value) pairs arriving in an arbitrary order, where idKey is an integer between 1 and n and value is a string. No two pairs have the same id.

Design a stream that returns the values in increasing order of their IDs by returning a chunk (list) of values after each insertion. The concatenation of all the chunks should result in a list of the sorted values.

Implement the OrderedStream class:

- OrderedStream(int n) Constructs the stream to take n values.
- String[] insert(int idKey, String value) Inserts the pair (idKey, value) into the stream, then returns the largest possible chunk of currently inserted values that appear next in the order.

Example:

Input
["OrderedStream","insert","insert","insert","insert","insert"]
[[5],[3,"ccccc"],[1,"aaaaa"],[2,"bbbbb"],[5,"eeeee"],[4,"ddddd"]]
Output
[null, [], ["aaaaa"], ["bbbbb","ccccc"], [], ["ddddd","eeeee"]]

Explanation
// Note that the values ordered by ID is ["aaaaa", "bbbbb", "ccccc", "ddddd", "eeeee"].
OrderedStream os = new OrderedStream(5);
os.insert(3, "ccccc"); // Inserts (3, "ccccc"), returns [].
os.insert(1, "aaaaa"); // Inserts (1, "aaaaa"), returns ["aaaaa"].
os.insert(2, "bbbbb"); // Inserts (2, "bbbbb"), returns ["bbbbb", "ccccc"].
os.insert(5, "eeeee"); // Inserts (5, "eeeee"), returns [].
os.insert(4, "ddddd"); // Inserts (4, "ddddd"), returns ["ddddd", "eeeee"].
// Concatenating all the chunks returned:
// [] + ["aaaaa"] + ["bbbbb", "ccccc"] + [] + ["ddddd", "eeeee"] = ["aaaaa", "bbbbb", "ccccc", "ddddd", "eeeee"]
// The resulting order is the same as the order above.

Constraints:

    1 <= n <= 1000
    1 <= id <= n
    value.length == 5
    value consists only of lowercase letters.
    Each call to insert will have a unique id.
    Exactly n calls will be made to insert.

---

Learning

LEETCODE: Accepted (3 ms, 19.9 MB)
"""


class OrderedStream:

    def __init__(self, n: int):
        self.vals = table(n + 1, fill=None)
        self.ptr = 1

    def insert(self, idKey: int, value: str) -> List[str]:
        self.vals[idKey] = value
        out = []
        while self.ptr < len(self.vals) and self.vals[self.ptr] is not None:
            out.append(self.vals[self.ptr])
            self.ptr += 1
        return out


sol = OrderedStream(5)

print(sol.insert(3, "ccccc"))  # []
# print(sol.insert(1, "aaaaa"))  # ["aaaaa"]
# print(sol.insert(2, "bbbbb"))  # ["bbbbb", "ccccc"]
# print(sol.insert(5, "eeeee"))  # []
# print(sol.insert(4, "ddddd"))  # ["ddddd", "eeeee"]

# # Assertions for the official example
# os = OrderedStream(5)
# assert os.insert(3, "ccccc") == []
# assert os.insert(1, "aaaaa") == ["aaaaa"]
# assert os.insert(2, "bbbbb") == ["bbbbb", "ccccc"]
# assert os.insert(5, "eeeee") == []
# assert os.insert(4, "ddddd") == ["ddddd", "eeeee"]

# assert OrderedStream(1).insert(1, "abcde") == ["abcde"]
