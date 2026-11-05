# URL: https://leetcode.com/problems/iterator-for-combination/description/?envType=problem-list-v2&envId=vn57k9wr
#
# 1286. Iterator for Combination
#
# Design the CombinationIterator class:
#
# - CombinationIterator(string characters, int combinationLength) Initializes the object with a string characters of sorted distinct lowercase English letters and a number combinationLength as arguments.
# - next() Returns the next combination of length combinationLength in lexicographical order.
# - hasNext() Returns true if and only if there exists a next combination.
#
# Example 1:
#
# Input
# ["CombinationIterator", "next", "hasNext", "next", "hasNext", "next", "hasNext"]
# [["abc", 2], [], [], [], [], [], []]
# Output
# [null, "ab", true, "ac", true, "bc", false]
#
# Explanation
# CombinationIterator itr = new CombinationIterator("abc", 2);
# itr.next();    // return "ab"
# itr.hasNext(); // return True
# itr.next();    // return "ac"
# itr.hasNext(); // return True
# itr.next();    // return "bc"
# itr.hasNext(); // return False
#
# Constraints:
#
#     1 <= combinationLength <= characters.length <= 15
#     All the characters of characters are unique.
#     At most 10^4 calls will be made to next and hasNext.
#     It is guaranteed that all calls of the function next are valid.
#
# ---
# LEETCODE: Accepted (25 ms, 22.5 MB)

# mu 0.16


class CombinationIterator
  def __init__(characters: str, combinationLength: int)
    self.arr = characters
    self.n = combinationLength
    self.res = []
    self.path = []
    self.i = 0
    def helper(i)
      if len self.path == self.n
        self.res <- self.path[:]
        return
      if len self.path > self.n
        return
      for j in i..<len(self.arr)
        self.path <- self.arr[j]
        helper(j + 1)
        self.path .
    helper(0)

  def next() -> str
    ret res = ''
    if self.hasNext()
      res = ''.join self.res[self.i]
      self.i += 1

  def hasNext() -> bool
    self.i < len self.res

sol = CombinationIterator('abc', 2)
print(sol.next())  # "ab"

itr = CombinationIterator('abc', 2)
assert itr.next() == 'ab'
assert itr.hasNext() == true
assert itr.next() == 'ac'
assert itr.hasNext() == true
assert itr.next() == 'bc'
assert itr.hasNext() == false

assert CombinationIterator('a', 1).next() == 'a'
assert CombinationIterator('a', 1).hasNext() == true
assert CombinationIterator('abcde', 1).next() == 'a'
assert CombinationIterator('abcde', 5).next() == 'abcde'
assert CombinationIterator('abcde', 5).hasNext() == true
assert CombinationIterator('abcdefghijklmno', 15).next() == 'abcdefghijklmno'
assert CombinationIterator('abcdefghijklmno', 1).next() == 'a'
assert CombinationIterator('abcdefghijklmno', 1).hasNext() == true
assert CombinationIterator('abcdefghijklmno', 14).next() == 'abcdefghijklmn'
assert CombinationIterator('abcdefghijklmno', 14).hasNext() == true
assert CombinationIterator('abc', 2).hasNext() == true
assert CombinationIterator('abc', 3).next() == 'abc'
