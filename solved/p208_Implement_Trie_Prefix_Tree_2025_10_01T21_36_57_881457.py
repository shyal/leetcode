"""
URL: https://leetcode.com/problems/implement-trie-prefix-tree/description/?envType=study-plan-v2&envId=leetcode-75

208. Implement Trie (Prefix Tree)

A trie (pronounced as "try") or prefix tree is a tree data structure used to efficiently store and retrieve keys in a dataset of strings. There are various applications of this data structure, such as autocomplete and spellchecker.

Implement the Trie class:

        Trie() Initializes the trie object.
        void insert(String word) Inserts the string word into the trie.
        boolean search(String word) Returns true if the string word is in the trie (i.e., was inserted before), and false otherwise.
        boolean startsWith(String prefix) Returns true if there is a previously inserted string word that has the prefix prefix, and false otherwise.


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
        At most 3 * 104 calls in total will be made to insert, search, and startsWith.
"""


class Node:
    def __init__(self, val, children=None):
        self.val = val
        self.children = children if children is not None else {}


class Solution:

    def main(self):
        class Trie:

            def __init__(self):
                self.data = set([])
                self.g = Node("head")

            def insert(self, word: str) -> None:
                it = self.g
                for c in word:
                    if c in it.children:
                        it = it.children[c]
                    else:
                        nn = Node(c)
                        it.children[c] = nn
                        it = nn
                it.children["."] = Node(".")

            def search(self, word: str) -> bool:
                it = self.g
                for c in word:
                    if c in it.children:
                        it = it.children[c]
                    else:
                        return False
                return "." in it.children

            def startsWith(self, prefix: str) -> bool:
                it = self.g
                for c in prefix:
                    if c in it.children:
                        it = it.children[c]
                    else:
                        return False
                return True

        return Trie


sol = Solution()

Trie = sol.main()

trie = Trie()
trie.insert("apple")
assert trie.search("apple") == True
assert trie.search("app") == False
assert trie.startsWith("app") == True
trie.insert("app")
assert trie.search("app") == True

trie = Trie()
trie.insert("a")
assert trie.search("a") == True
assert trie.startsWith("a") == True
assert trie.search("b") == False
assert trie.startsWith("b") == False

trie = Trie()
trie.insert("apple")
trie.insert("app")
trie.insert("apricot")
assert trie.search("apple") == True
assert trie.search("app") == True
assert trie.search("apricot") == True
assert trie.search("ap") == False
assert trie.startsWith("ap") == True
assert trie.startsWith("app") == True
assert trie.startsWith("apr") == True
assert trie.startsWith("apx") == False

trie = Trie()
trie.insert("banana")
trie.insert("banana")
assert trie.search("banana") == True
assert trie.startsWith("ban") == True
assert trie.startsWith("bana") == True
assert trie.search("ban") == False

trie = Trie()
trie.insert("cat")
trie.insert("dog")
assert trie.search("cat") == True
assert trie.search("dog") == True
assert trie.search("ca") == False
assert trie.startsWith("ca") == True
assert trie.startsWith("do") == True
assert trie.startsWith("catd") == False

trie = Trie()
trie.insert("hello")
assert trie.startsWith("helloworld") == False
assert trie.search("helloworld") == False
