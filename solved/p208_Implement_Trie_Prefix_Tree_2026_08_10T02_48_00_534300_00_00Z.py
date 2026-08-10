"""
URL: https://leetcode.com/problems/implement-trie-prefix-tree/description/?envType=problem-list-v2&envId=vn57k9wr

208. Implement Trie (Prefix Tree)

A trie (pronounced as "try") or prefix tree is a tree data structure used to
efficiently store and retrieve keys in a dataset of strings. There are various
applications of this data structure, such as autocomplete and spellchecker.

Implement the Trie class:

    Trie() Initializes the trie object.
    void insert(String word) Inserts the string word into the trie.
    boolean search(String word) Returns true if the string word is in the trie
        (i.e., was inserted before), and false otherwise.
    boolean startsWith(String prefix) Returns true if there is a previously
        inserted string word that has the prefix prefix, and false otherwise.


Example 1:

Input
["Trie", "insert", "search", "search", "startsWith", "insert", "search"]
[[], ["apple"], ["apple"], ["app"], ["app"], ["app"], ["app"]]
Output
[null, null, true, false, true, null, true]

Explanation
Trie trie = new Trie();
trie.insert("apple");
trie.search("apple");   // return True
trie.search("app");     // return False
trie.startsWith("app"); // return True
trie.insert("app");
trie.search("app");     // return True


Constraints:

    1 <= word.length, prefix.length <= 2000
    word and prefix consist only of lowercase English letters.
    At most 3 * 10^4 calls in total will be made to insert, search, and startsWith.
"""

class Trie:

    def __init__(self):
        self.tree = Node(val=None)

    def insert(self, word: str) -> None:
        def helper(d, tree):
            if d >= len(word):
                tree.children['terminal'] = Node('terminal')
                return
            if word[d] not in tree.children:
                tree.children[word[d]] = Node(word[d])
                helper(d+1, tree.children[word[d]])
            else:
                helper(d+1, tree.children[word[d]])
        helper(0, self.tree)

    def search(self, word: str) -> bool:
        def helper(d, tree):
            if not tree:
                return True
            if d >= len(word):
                return 'terminal' in tree.children
            return word[d] in tree.children and helper(d+1, tree.children[word[d]])
        return helper(0, self.tree)

    def startsWith(self, prefix: str) -> bool:
        def helper(d, tree):
            if not tree:
                return True
            if d >= len(prefix):
                return True
            return prefix[d] in tree.children and helper(d+1, tree.children[prefix[d]])
        return helper(0, self.tree)



def run_ops(ops: List[str], args: List[List[Any]]) -> List[Any]:
    obj = None
    out = []
    for op, arg in zip(ops, args):
        if op == "Trie":
            obj = Trie()
            out.append(None)
        else:
            out.append(getattr(obj, op)(*arg))
    return out


print(
    run_ops(
        ["Trie", "insert", "search", "search", "startsWith", "insert", "search"],
        [[], ["apple"], ["apple"], ["app"], ["app"], ["app"], ["app"]],
    )
)  # [None, None, True, False, True, None, True]

assert run_ops(
    ["Trie", "insert", "search", "search", "startsWith", "insert", "search"],
    [[], ["apple"], ["apple"], ["app"], ["app"], ["app"], ["app"]],
) == [None, None, True, False, True, None, True]

assert run_ops(["Trie"], [[]]) == [None]

assert run_ops(
    ["Trie", "search", "startsWith", "insert", "search", "startsWith", "startsWith"],
    [[], ["a"], ["a"], ["a"], ["a"], ["a"], ["ab"]],
) == [None, False, False, None, True, True, False]

assert run_ops(
    ["Trie", "insert", "insert", "search", "search", "startsWith", "startsWith"],
    [[], ["ab"], ["ab"], ["ab"], ["a"], ["a"], ["b"]],
) == [None, None, None, True, False, True, False]

trie = Trie()
trie.insert("apple")

# draw_general_tree(trie.tree)

assert trie.search("apple") is True
assert trie.search("app") is False
assert trie.startsWith("app") is True
trie.insert("app")
assert trie.search("app") is True
assert trie.startsWith("b") is False
assert trie.search("") is False
assert trie.startsWith("") is True
assert trie.startsWith("apple") is True
assert trie.startsWith("apples") is False
assert trie.search("apples") is False
assert trie.search("appl") is False
assert trie.startsWith("appl") is True
assert trie.search("a") is False
assert trie.startsWith("a") is True
assert trie.search("pple") is False
assert trie.startsWith("pp") is False

empty = Trie()
assert empty.search("") is False
assert empty.startsWith("") is True
assert empty.search("a") is False
assert empty.startsWith("a") is False
empty.insert("")
assert empty.search("") is True
assert empty.startsWith("") is True
assert empty.search("a") is False
assert empty.startsWith("a") is False

dup = Trie()
dup.insert("abc")
dup.insert("abc")
dup.insert("abc")
assert dup.search("abc") is True
assert dup.startsWith("abc") is True
assert dup.search("ab") is False
assert dup.startsWith("ab") is True
assert dup.search("abcd") is False
assert dup.startsWith("abcd") is False

branch = Trie()
for w in ["cat", "car", "card", "care", "dog", "do"]:
    branch.insert(w)
assert branch.search("cat") is True
assert branch.search("car") is True
assert branch.search("card") is True
assert branch.search("care") is True
assert branch.search("dog") is True
assert branch.search("do") is True
assert branch.search("ca") is False
assert branch.search("cars") is False
assert branch.search("d") is False
assert branch.search("doge") is False
assert branch.startsWith("ca") is True
assert branch.startsWith("car") is True
assert branch.startsWith("cars") is False
assert branch.startsWith("d") is True
assert branch.startsWith("do") is True
assert branch.startsWith("dog") is True
assert branch.startsWith("dogs") is False
assert branch.startsWith("e") is False
assert branch.startsWith("") is True
assert branch.search("") is False

nested = Trie()
nested.insert("abcde")
assert nested.search("abcde") is True
for i in range(5):
    pass
    assert nested.search("abcde"[:i]) is False
    assert nested.startsWith("abcde"[:i]) is True
nested.insert("abc")
assert nested.search("abc") is True
assert nested.search("ab") is False
assert nested.search("abcd") is False
assert nested.search("abcde") is True

single = Trie()
single.insert("z")
assert single.search("z") is True
assert single.startsWith("z") is True
assert single.search("y") is False
assert single.startsWith("y") is False
assert single.search("zz") is False
assert single.startsWith("zz") is False

# long_word = "a" * 2000
# longt = Trie()
# longt.insert(long_word)
# assert longt.search(long_word) is True
# assert longt.startsWith(long_word) is True
# assert longt.search("a" * 1999) is False
# assert longt.startsWith("a" * 1999) is True
# assert longt.search("a" * 2001) is False
# assert longt.startsWith("a" * 2001) is False
# longt.insert("a" * 1999)
# assert longt.search("a" * 1999) is True
# assert longt.search(long_word) is True

alphabet = Trie()
letters = "abcdefghijklmnopqrstuvwxyz"
for ch in letters:
    alphabet.insert(ch)
for ch in letters:
    pass
    assert alphabet.search(ch) is True
    assert alphabet.startsWith(ch) is True
    assert alphabet.search(ch + ch) is False
    assert alphabet.startsWith(ch + ch) is False
assert alphabet.search("") is False
assert alphabet.startsWith("") is True

shared = Trie()
shared.insert("ab")
assert shared.startsWith("a") is True
assert shared.search("a") is False
shared.insert("a")
assert shared.search("a") is True
assert shared.search("ab") is True
assert shared.search("abc") is False

isolated_a = Trie()
isolated_b = Trie()
isolated_a.insert("hello")
assert isolated_b.search("hello") is False
assert isolated_b.startsWith("hello") is False
assert isolated_a.search("hello") is True

# print("All tests passed")