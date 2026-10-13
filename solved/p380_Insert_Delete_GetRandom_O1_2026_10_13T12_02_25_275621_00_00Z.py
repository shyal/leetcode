"""
URL: https://leetcode.com/problems/insert-delete-getrandom-o1/description/?envType=problem-list-v2&envId=vn57k9wr

380. Insert Delete GetRandom O(1)

Implement the RandomizedSet class:

- RandomizedSet() Initializes the RandomizedSet object.
- bool insert(int val) Inserts an item val into the set if not present. Returns true if the item was not present, false otherwise.
- bool remove(int val) Removes an item val from the set if present. Returns true if the item was present, false otherwise.
- int getRandom() Returns a random element from the current set of elements (it's guaranteed that at least one element exists when this method is called). Each element must have the same probability of being returned.

You must implement the functions of the class such that each function works in average O(1) time complexity.

Example 1:

Input
["RandomizedSet","insert","remove","insert","getRandom","remove","insert","getRandom"]
[[],[1],[2],[2],[],[1],[2],[]]
Output
[null, true, false, true, 2, true, false, 2]

Explanation
RandomizedSet randomizedSet = new RandomizedSet();
randomizedSet.insert(1); // Inserts 1 to the set. Returns true as 1 was inserted successfully.
randomizedSet.remove(2); // Returns false as 2 does not exist in the set.
randomizedSet.insert(2); // Inserts 2 to the set, returns true. Set now contains [1,2].
randomizedSet.getRandom(); // getRandom() should return either 1 or 2 randomly.
randomizedSet.remove(1); // Removes 1 from the set, returns true. Set now contains [2].
randomizedSet.insert(2); // 2 was already in the set, so return false.
randomizedSet.getRandom(); // Since 2 is the only number in the set, getRandom() will always return 2.

Constraints:

-2^31 <= val <= 2^31 - 1
At most 2 * 10^5 calls will be made to insert, remove, and getRandom.
There will be at least one element in the data structure when getRandom is called.
---
Hinted

LEETCODE: Accepted (97 ms, 57.1 MB)
"""

import random


# mu 0.10
# class RandomizedSet
#   def __init__()
#     self.vals = []
#     self.pos = {}
#
#   def insert(val: int) -> bool
#     ret absent = val not in self.pos
#     if absent
#       self.pos[val] = len(self.vals)
#       self.vals.append(val)
#
#   def remove(val: int) -> bool
#     ret present = val in self.pos
#     if present
#       i = self.pos[val]            # index of val
#       last = self.vals[-1]
#       self.vals[i] = last          # last element moves to index i
#       self.pos[last] = i           # its index is now i
#       self.vals.pop()              # drop the last slot
#       del self.pos[val]
#
#   def getRandom() -> int
#     random.choice(self.vals)
#
# # Your RandomizedSet object will be instantiated and called as such:
# # obj = RandomizedSet()
# # param_1 = obj.insert(val)
# # param_2 = obj.remove(val)
# # param_3 = obj.getRandom()

class RandomizedSet:
    def __init__(self):
        self.vals = []
        self.pos = {}

    def insert(self, val: int) -> bool:
        absent = val not in self.pos
        if absent:
            self.pos[val] = len(self.vals)
            self.vals.append(val)
        return absent

    def remove(self, val: int) -> bool:
        present = val in self.pos
        if present:
            i = self.pos[val]
            last = self.vals[-1]
            self.vals[i] = last
            self.pos[last] = i
            self.vals.pop()
            del self.pos[val]
        return present

    def getRandom(self) -> int:
        return random.choice(self.vals)


sol = RandomizedSet()
print(sol.insert(1))
print(sol.remove(2))
print(sol.insert(2))
print(sol.getRandom())
print(sol.remove(1))
print(sol.insert(2))
print(sol.getRandom())
obj = RandomizedSet()
_l, _r = obj.insert(1), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = obj.remove(2), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = obj.insert(2), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
rand_val = obj.getRandom()
_l, _r = rand_val, (1, 2)
assert _l in _r, f"left : {_l!r}\nright: {_r!r}\nop   : in"
_l, _r = obj.remove(1), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = obj.insert(2), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
rand_val2 = obj.getRandom()
_l, _r = rand_val2, 2
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol = RandomizedSet()
_l, _r = sol.insert(1), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(1), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(1), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(1), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
sol = RandomizedSet()
_l, _r = sol.insert(1), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(2), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(1), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.getRandom(), 2
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.insert(1), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(2), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.getRandom(), 1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol = RandomizedSet()
_l, _r = sol.insert(1), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(2), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(3), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(3), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(2), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.getRandom(), 1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol = RandomizedSet()
_l, _r = sol.insert(1), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(2), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(3), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(1), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(3), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.getRandom(), 2
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.remove(2), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(2), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.getRandom(), 2
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol = RandomizedSet()
_l, _r = sol.insert(1), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(2), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(3), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(2), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(2), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(1), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(2), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.getRandom(), 3
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol = RandomizedSet()
_l, _r = sol.insert(-2147483648), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(2147483647), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(-2147483648), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.getRandom(), 2147483647
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.remove(2147483647), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(0), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.getRandom(), 0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol = RandomizedSet()
_l, _r = sol.insert(5), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(5), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(5), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.getRandom(), 5
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.remove(5), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(5), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(6), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.getRandom(), 6
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol = RandomizedSet()
_l, _r = sol.insert(1), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(2), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.getRandom(), {1, 2}
assert _l in _r, f"left : {_l!r}\nright: {_r!r}\nop   : in"
_l, _r = sol.remove(1), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.getRandom(), 2
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol = RandomizedSet()
_l, _r = sol.insert(1), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(2), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(3), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(4), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(1), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(2), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(3), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.getRandom(), 4
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.insert(1), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(4), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.getRandom(), 1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol = RandomizedSet()
_l, _r = sol.insert(2), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.getRandom(), 2
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.getRandom(), 2
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.insert(1), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(-2), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(2), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(0), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(3), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(-1), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(1), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(-1), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(2), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(3), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.getRandom(), {-2, 1, 3}
assert _l in _r, f"left : {_l!r}\nright: {_r!r}\nop   : in"
_l, _r = sol.getRandom(), {-2, 1, 3}
assert _l in _r, f"left : {_l!r}\nright: {_r!r}\nop   : in"
_l, _r = sol.remove(0), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(-1), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(-1), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(2), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.getRandom(), {-2, -1, 1, 2, 3}
assert _l in _r, f"left : {_l!r}\nright: {_r!r}\nop   : in"
_l, _r = sol.insert(-2), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(-2), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(3), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.getRandom(), {-2, -1, 1, 2}
assert _l in _r, f"left : {_l!r}\nright: {_r!r}\nop   : in"
_l, _r = sol.getRandom(), {-2, -1, 1, 2}
assert _l in _r, f"left : {_l!r}\nright: {_r!r}\nop   : in"
_l, _r = sol.getRandom(), {-2, -1, 1, 2}
assert _l in _r, f"left : {_l!r}\nright: {_r!r}\nop   : in"
_l, _r = sol.insert(1), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.getRandom(), {-2, -1, 1, 2}
assert _l in _r, f"left : {_l!r}\nright: {_r!r}\nop   : in"
_l, _r = sol.insert(1), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
sol = RandomizedSet()
_l, _r = sol.insert(-1), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(3), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(2), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(1), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.getRandom(), {-1, 1, 2}
assert _l in _r, f"left : {_l!r}\nright: {_r!r}\nop   : in"
_l, _r = sol.remove(0), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(-1), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.getRandom(), {1, 2}
assert _l in _r, f"left : {_l!r}\nright: {_r!r}\nop   : in"
_l, _r = sol.remove(-1), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(3), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(1), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.getRandom(), {1, 2, 3}
assert _l in _r, f"left : {_l!r}\nright: {_r!r}\nop   : in"
_l, _r = sol.remove(2), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(0), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(-2), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(-1), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(2), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.getRandom(), {-1, 0, 1, 2, 3}
assert _l in _r, f"left : {_l!r}\nright: {_r!r}\nop   : in"
_l, _r = sol.insert(0), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(-2), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(-2), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.getRandom(), {-2, -1, 0, 1, 2, 3}
assert _l in _r, f"left : {_l!r}\nright: {_r!r}\nop   : in"
_l, _r = sol.insert(3), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(-1), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(0), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.getRandom(), {-2, 0, 1, 2, 3}
assert _l in _r, f"left : {_l!r}\nright: {_r!r}\nop   : in"
_l, _r = sol.insert(3), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.getRandom(), {-2, 0, 1, 2, 3}
assert _l in _r, f"left : {_l!r}\nright: {_r!r}\nop   : in"
_l, _r = sol.getRandom(), {-2, 0, 1, 2, 3}
assert _l in _r, f"left : {_l!r}\nright: {_r!r}\nop   : in"
_l, _r = sol.remove(-1), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
sol = RandomizedSet()
_l, _r = sol.insert(-2), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(2), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.getRandom(), -2
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.insert(1), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(0), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.getRandom(), {-2, 0, 1}
assert _l in _r, f"left : {_l!r}\nright: {_r!r}\nop   : in"
_l, _r = sol.insert(-1), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(3), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.getRandom(), {-2, -1, 0, 1}
assert _l in _r, f"left : {_l!r}\nright: {_r!r}\nop   : in"
_l, _r = sol.insert(-1), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(2), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.getRandom(), {-2, -1, 0, 1}
assert _l in _r, f"left : {_l!r}\nright: {_r!r}\nop   : in"
_l, _r = sol.insert(1), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(-2), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(0), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(0), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(2), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(0), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(0), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.getRandom(), {-1, 1, 2}
assert _l in _r, f"left : {_l!r}\nright: {_r!r}\nop   : in"
_l, _r = sol.remove(2), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.getRandom(), {-1, 1}
assert _l in _r, f"left : {_l!r}\nright: {_r!r}\nop   : in"
_l, _r = sol.remove(-1), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.getRandom(), 1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.remove(-1), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(1), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(2), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(2), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(2), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
sol = RandomizedSet()
_l, _r = sol.insert(-1), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(-1), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.getRandom(), -1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.insert(0), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(-1), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(1), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(-1), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(3), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.getRandom(), {-1, 0}
assert _l in _r, f"left : {_l!r}\nright: {_r!r}\nop   : in"
_l, _r = sol.insert(0), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(-2), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(3), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(1), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(1), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(-1), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(2), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(3), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.getRandom(), {-2, -1, 0, 2}
assert _l in _r, f"left : {_l!r}\nright: {_r!r}\nop   : in"
_l, _r = sol.remove(0), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(2), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(0), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.getRandom(), {-2, -1}
assert _l in _r, f"left : {_l!r}\nright: {_r!r}\nop   : in"
_l, _r = sol.insert(0), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(2), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(0), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.getRandom(), {-2, -1, 0, 2}
assert _l in _r, f"left : {_l!r}\nright: {_r!r}\nop   : in"
_l, _r = sol.getRandom(), {-2, -1, 0, 2}
assert _l in _r, f"left : {_l!r}\nright: {_r!r}\nop   : in"
_l, _r = sol.getRandom(), {-2, -1, 0, 2}
assert _l in _r, f"left : {_l!r}\nright: {_r!r}\nop   : in"
_l, _r = sol.getRandom(), {-2, -1, 0, 2}
assert _l in _r, f"left : {_l!r}\nright: {_r!r}\nop   : in"
sol = RandomizedSet()
_l, _r = sol.insert(3), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(0), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.getRandom(), 3
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.getRandom(), 3
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.remove(0), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(-1), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(0), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(-2), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(-1), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(-1), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(3), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(-2), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(0), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(-1), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(2), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(2), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(2), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(2), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(2), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(-2), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(2), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(-1), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(2), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.getRandom(), 2
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol = RandomizedSet()
_l, _r = sol.insert(2), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(-2), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(3), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(0), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(3), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(2), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.getRandom(), {-2, 2, 3}
assert _l in _r, f"left : {_l!r}\nright: {_r!r}\nop   : in"
_l, _r = sol.getRandom(), {-2, 2, 3}
assert _l in _r, f"left : {_l!r}\nright: {_r!r}\nop   : in"
_l, _r = sol.remove(1), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.getRandom(), {-2, 2, 3}
assert _l in _r, f"left : {_l!r}\nright: {_r!r}\nop   : in"
_l, _r = sol.remove(2), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(0), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.getRandom(), {-2, 0, 3}
assert _l in _r, f"left : {_l!r}\nright: {_r!r}\nop   : in"
_l, _r = sol.remove(-1), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(-2), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.getRandom(), {-2, 0, 3}
assert _l in _r, f"left : {_l!r}\nright: {_r!r}\nop   : in"
_l, _r = sol.remove(0), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(0), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(-2), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(3), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(0), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(-2), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.getRandom(), 3
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.remove(3), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(-1), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(-1), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(-1), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(-1), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.getRandom(), -1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.insert(-2), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
sol = RandomizedSet()
_l, _r = sol.insert(0), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(0), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.getRandom(), 0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.insert(2), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(1), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(-2), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(-2), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(0), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(-2), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(3), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(2), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(1), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(1), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(-1), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(1), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(1), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(0), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.getRandom(), {-2, -1, 0, 1, 3}
assert _l in _r, f"left : {_l!r}\nright: {_r!r}\nop   : in"
_l, _r = sol.insert(0), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.getRandom(), {-2, -1, 0, 1, 3}
assert _l in _r, f"left : {_l!r}\nright: {_r!r}\nop   : in"
_l, _r = sol.insert(3), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.getRandom(), {-2, -1, 0, 1, 3}
assert _l in _r, f"left : {_l!r}\nright: {_r!r}\nop   : in"
_l, _r = sol.insert(1), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(3), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(-2), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.getRandom(), {-2, -1, 0, 1, 3}
assert _l in _r, f"left : {_l!r}\nright: {_r!r}\nop   : in"
_l, _r = sol.getRandom(), {-2, -1, 0, 1, 3}
assert _l in _r, f"left : {_l!r}\nright: {_r!r}\nop   : in"
_l, _r = sol.getRandom(), {-2, -1, 0, 1, 3}
assert _l in _r, f"left : {_l!r}\nright: {_r!r}\nop   : in"
_l, _r = sol.remove(3), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.getRandom(), {-2, -1, 0, 1}
assert _l in _r, f"left : {_l!r}\nright: {_r!r}\nop   : in"
sol = RandomizedSet()
_l, _r = sol.insert(-2), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(1), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(1), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(0), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(1), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(2), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(3), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(2), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(3), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(-2), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(-2), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.getRandom(), {-2, 0, 1, 2, 3}
assert _l in _r, f"left : {_l!r}\nright: {_r!r}\nop   : in"
_l, _r = sol.remove(2), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(-1), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(0), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(2), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(2), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(-2), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(1), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(-1), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(-2), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.getRandom(), {-1, 0, 3}
assert _l in _r, f"left : {_l!r}\nright: {_r!r}\nop   : in"
_l, _r = sol.remove(2), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.getRandom(), {-1, 0, 3}
assert _l in _r, f"left : {_l!r}\nright: {_r!r}\nop   : in"
_l, _r = sol.getRandom(), {-1, 0, 3}
assert _l in _r, f"left : {_l!r}\nright: {_r!r}\nop   : in"
_l, _r = sol.insert(1), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(1), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(0), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(1), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(-2), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
sol = RandomizedSet()
_l, _r = sol.remove(3), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(1), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(-2), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(-2), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(-2), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(-2), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(0), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(3), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(3), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(0), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.getRandom(), {0, 3}
assert _l in _r, f"left : {_l!r}\nright: {_r!r}\nop   : in"
_l, _r = sol.getRandom(), {0, 3}
assert _l in _r, f"left : {_l!r}\nright: {_r!r}\nop   : in"
_l, _r = sol.insert(-1), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(-2), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(3), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(2), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(1), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(3), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(-1), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.getRandom(), {-2, -1, 0, 3}
assert _l in _r, f"left : {_l!r}\nright: {_r!r}\nop   : in"
_l, _r = sol.remove(1), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.getRandom(), {-2, -1, 0, 3}
assert _l in _r, f"left : {_l!r}\nright: {_r!r}\nop   : in"
_l, _r = sol.getRandom(), {-2, -1, 0, 3}
assert _l in _r, f"left : {_l!r}\nright: {_r!r}\nop   : in"
_l, _r = sol.insert(-2), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(2), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(1), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(0), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(0), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(3), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(-1), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
sol = RandomizedSet()
_l, _r = sol.insert(0), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.getRandom(), 0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.remove(1), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.getRandom(), 0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.insert(2), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(0), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(-2), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(3), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(-1), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(-2), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(0), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(-2), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.getRandom(), {-1, 0, 2, 3}
assert _l in _r, f"left : {_l!r}\nright: {_r!r}\nop   : in"
_l, _r = sol.remove(-1), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(2), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(-1), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.getRandom(), {-1, 0, 3}
assert _l in _r, f"left : {_l!r}\nright: {_r!r}\nop   : in"
_l, _r = sol.insert(0), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(2), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(3), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(0), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(-1), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.getRandom(), 2
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.remove(0), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(2), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(0), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(2), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(0), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
sol = RandomizedSet()
_l, _r = sol.remove(-2), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(-1), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(-2), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.getRandom(), -2
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.insert(2), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.getRandom(), {-2, 2}
assert _l in _r, f"left : {_l!r}\nright: {_r!r}\nop   : in"
_l, _r = sol.insert(3), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(-1), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.getRandom(), {-2, -1, 2, 3}
assert _l in _r, f"left : {_l!r}\nright: {_r!r}\nop   : in"
_l, _r = sol.getRandom(), {-2, -1, 2, 3}
assert _l in _r, f"left : {_l!r}\nright: {_r!r}\nop   : in"
_l, _r = sol.insert(-1), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(-1), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.getRandom(), {-2, 2, 3}
assert _l in _r, f"left : {_l!r}\nright: {_r!r}\nop   : in"
_l, _r = sol.insert(1), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(1), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(-1), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(3), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(3), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(-2), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(3), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.getRandom(), {-2, -1, 2, 3}
assert _l in _r, f"left : {_l!r}\nright: {_r!r}\nop   : in"
_l, _r = sol.getRandom(), {-2, -1, 2, 3}
assert _l in _r, f"left : {_l!r}\nright: {_r!r}\nop   : in"
_l, _r = sol.remove(0), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(1), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.getRandom(), {-2, -1, 2, 3}
assert _l in _r, f"left : {_l!r}\nright: {_r!r}\nop   : in"
_l, _r = sol.getRandom(), {-2, -1, 2, 3}
assert _l in _r, f"left : {_l!r}\nright: {_r!r}\nop   : in"
_l, _r = sol.insert(0), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(-1), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(3), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
sol = RandomizedSet()
_l, _r = sol.remove(-1), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(-2), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(0), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(2), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(1), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.getRandom(), {-2, 1, 2}
assert _l in _r, f"left : {_l!r}\nright: {_r!r}\nop   : in"
_l, _r = sol.insert(2), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(1), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(3), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(3), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(1), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(-2), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(-2), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(2), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(-1), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.getRandom(), {-1, 1, 3}
assert _l in _r, f"left : {_l!r}\nright: {_r!r}\nop   : in"
_l, _r = sol.remove(2), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(-2), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.getRandom(), {-1, 1, 3}
assert _l in _r, f"left : {_l!r}\nright: {_r!r}\nop   : in"
_l, _r = sol.getRandom(), {-1, 1, 3}
assert _l in _r, f"left : {_l!r}\nright: {_r!r}\nop   : in"
_l, _r = sol.insert(-1), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(2), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(2), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(3), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.getRandom(), {-1, 1, 2, 3}
assert _l in _r, f"left : {_l!r}\nright: {_r!r}\nop   : in"
_l, _r = sol.insert(3), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(1), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(-1), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(3), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
sol = RandomizedSet()
_l, _r = sol.remove(-1), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(-1), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(2), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.getRandom(), {-1, 2}
assert _l in _r, f"left : {_l!r}\nright: {_r!r}\nop   : in"
_l, _r = sol.remove(3), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.getRandom(), {-1, 2}
assert _l in _r, f"left : {_l!r}\nright: {_r!r}\nop   : in"
_l, _r = sol.remove(-1), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.getRandom(), 2
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.insert(-2), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(1), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(2), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(2), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(1), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(-2), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.getRandom(), {-2, 2}
assert _l in _r, f"left : {_l!r}\nright: {_r!r}\nop   : in"
_l, _r = sol.insert(-2), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(0), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(-2), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.getRandom(), {-2, 0, 2}
assert _l in _r, f"left : {_l!r}\nright: {_r!r}\nop   : in"
_l, _r = sol.getRandom(), {-2, 0, 2}
assert _l in _r, f"left : {_l!r}\nright: {_r!r}\nop   : in"
_l, _r = sol.remove(0), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(-1), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.getRandom(), {-2, -1, 2}
assert _l in _r, f"left : {_l!r}\nright: {_r!r}\nop   : in"
_l, _r = sol.insert(0), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.getRandom(), {-2, -1, 0, 2}
assert _l in _r, f"left : {_l!r}\nright: {_r!r}\nop   : in"
_l, _r = sol.insert(2), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(-2), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(2), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(-1), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(-2), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
sol = RandomizedSet()
_l, _r = sol.remove(-2), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(-2), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(3), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.getRandom(), 3
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.getRandom(), 3
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.getRandom(), 3
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.remove(0), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.getRandom(), 3
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.remove(1), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(-1), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(-2), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(1), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(3), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.getRandom(), {-2, 1}
assert _l in _r, f"left : {_l!r}\nright: {_r!r}\nop   : in"
_l, _r = sol.insert(3), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(0), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(2), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.getRandom(), {-2, 0, 1, 2, 3}
assert _l in _r, f"left : {_l!r}\nright: {_r!r}\nop   : in"
_l, _r = sol.remove(-2), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.getRandom(), {0, 1, 2, 3}
assert _l in _r, f"left : {_l!r}\nright: {_r!r}\nop   : in"
_l, _r = sol.insert(0), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.getRandom(), {0, 1, 2, 3}
assert _l in _r, f"left : {_l!r}\nright: {_r!r}\nop   : in"
_l, _r = sol.remove(-2), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.getRandom(), {0, 1, 2, 3}
assert _l in _r, f"left : {_l!r}\nright: {_r!r}\nop   : in"
_l, _r = sol.insert(2), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(-1), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(-1), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.getRandom(), {-1, 0, 1, 2, 3}
assert _l in _r, f"left : {_l!r}\nright: {_r!r}\nop   : in"
sol = RandomizedSet()
_l, _r = sol.insert(3), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(1), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(-1), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(0), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.getRandom(), {-1, 0, 3}
assert _l in _r, f"left : {_l!r}\nright: {_r!r}\nop   : in"
_l, _r = sol.insert(1), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(3), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(1), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.getRandom(), {-1, 0, 1, 3}
assert _l in _r, f"left : {_l!r}\nright: {_r!r}\nop   : in"
_l, _r = sol.getRandom(), {-1, 0, 1, 3}
assert _l in _r, f"left : {_l!r}\nright: {_r!r}\nop   : in"
_l, _r = sol.remove(-2), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(3), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(0), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(3), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.getRandom(), {-1, 0, 1}
assert _l in _r, f"left : {_l!r}\nright: {_r!r}\nop   : in"
_l, _r = sol.remove(-1), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(1), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.getRandom(), {0, 1}
assert _l in _r, f"left : {_l!r}\nright: {_r!r}\nop   : in"
_l, _r = sol.getRandom(), {0, 1}
assert _l in _r, f"left : {_l!r}\nright: {_r!r}\nop   : in"
_l, _r = sol.getRandom(), {0, 1}
assert _l in _r, f"left : {_l!r}\nright: {_r!r}\nop   : in"
_l, _r = sol.insert(-1), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(-1), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(1), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(-1), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(1), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(1), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(2), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(3), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(-1), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(1), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
sol = RandomizedSet()
_l, _r = sol.insert(1), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(-2), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(2), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(-2), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(2), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(1), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(-1), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(-2), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(2), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(-1), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(1), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(-2), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(2), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.getRandom(), {-1, 1}
assert _l in _r, f"left : {_l!r}\nright: {_r!r}\nop   : in"
_l, _r = sol.remove(1), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(-1), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(3), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(0), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(2), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.getRandom(), {0, 3}
assert _l in _r, f"left : {_l!r}\nright: {_r!r}\nop   : in"
_l, _r = sol.insert(2), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(2), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(3), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(-1), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(-1), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(0), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.getRandom(), {-1, 0, 2, 3}
assert _l in _r, f"left : {_l!r}\nright: {_r!r}\nop   : in"
_l, _r = sol.insert(-2), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(2), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
sol = RandomizedSet()
_l, _r = sol.remove(3), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(1), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(3), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(1), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(-2), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(1), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.getRandom(), {-2, 1}
assert _l in _r, f"left : {_l!r}\nright: {_r!r}\nop   : in"
_l, _r = sol.insert(2), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(3), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(3), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(1), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(3), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.getRandom(), {-2, 2, 3}
assert _l in _r, f"left : {_l!r}\nright: {_r!r}\nop   : in"
_l, _r = sol.remove(1), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(2), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.getRandom(), {-2, 2, 3}
assert _l in _r, f"left : {_l!r}\nright: {_r!r}\nop   : in"
_l, _r = sol.insert(-2), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(-2), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.getRandom(), {-2, 2, 3}
assert _l in _r, f"left : {_l!r}\nright: {_r!r}\nop   : in"
_l, _r = sol.insert(3), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(3), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(2), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.getRandom(), {-2, 3}
assert _l in _r, f"left : {_l!r}\nright: {_r!r}\nop   : in"
_l, _r = sol.getRandom(), {-2, 3}
assert _l in _r, f"left : {_l!r}\nright: {_r!r}\nop   : in"
_l, _r = sol.remove(-1), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(2), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(1), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(3), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(-2), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(-2), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
sol = RandomizedSet()
_l, _r = sol.remove(2), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(2), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.getRandom(), 2
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.remove(1), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.getRandom(), 2
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.insert(-1), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(1), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(-1), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.getRandom(), {-1, 2}
assert _l in _r, f"left : {_l!r}\nright: {_r!r}\nop   : in"
_l, _r = sol.remove(-2), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(-2), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(2), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.getRandom(), -1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.getRandom(), -1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.getRandom(), -1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.getRandom(), -1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.insert(0), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(2), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(1), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(0), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(2), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.getRandom(), {-1, 0}
assert _l in _r, f"left : {_l!r}\nright: {_r!r}\nop   : in"
_l, _r = sol.insert(3), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(1), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(-2), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.getRandom(), {-1, 0, 1, 3}
assert _l in _r, f"left : {_l!r}\nright: {_r!r}\nop   : in"
_l, _r = sol.remove(2), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(0), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(-1), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
sol = RandomizedSet()
_l, _r = sol.remove(-2), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(0), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(3), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(-2), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(0), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(1), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(2), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(2), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.getRandom(), {0, 1, 3}
assert _l in _r, f"left : {_l!r}\nright: {_r!r}\nop   : in"
_l, _r = sol.remove(2), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(1), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(-1), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(0), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.getRandom(), {-1, 0, 3}
assert _l in _r, f"left : {_l!r}\nright: {_r!r}\nop   : in"
_l, _r = sol.insert(-2), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(3), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(2), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(2), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(2), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(3), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.getRandom(), {-2, -1, 0, 2}
assert _l in _r, f"left : {_l!r}\nright: {_r!r}\nop   : in"
_l, _r = sol.insert(3), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(-1), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(3), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(-1), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(-2), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(1), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(3), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(0), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(0), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
sol = RandomizedSet()
_l, _r = sol.insert(-1), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(3), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.getRandom(), -1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.insert(1), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(0), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.getRandom(), {-1, 1}
assert _l in _r, f"left : {_l!r}\nright: {_r!r}\nop   : in"
_l, _r = sol.getRandom(), {-1, 1}
assert _l in _r, f"left : {_l!r}\nright: {_r!r}\nop   : in"
_l, _r = sol.remove(1), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(1), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(3), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.getRandom(), {-1, 1}
assert _l in _r, f"left : {_l!r}\nright: {_r!r}\nop   : in"
_l, _r = sol.remove(1), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.getRandom(), -1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.getRandom(), -1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.getRandom(), -1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.getRandom(), -1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.remove(0), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(0), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(2), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(1), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.getRandom(), {-1, 1, 2}
assert _l in _r, f"left : {_l!r}\nright: {_r!r}\nop   : in"
_l, _r = sol.insert(0), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(2), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.getRandom(), {-1, 0, 1, 2}
assert _l in _r, f"left : {_l!r}\nright: {_r!r}\nop   : in"
_l, _r = sol.insert(2), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.remove(-1), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.insert(2), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.getRandom(), {0, 1, 2}
assert _l in _r, f"left : {_l!r}\nright: {_r!r}\nop   : in"
_l, _r = sol.insert(1), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.getRandom(), {0, 1, 2}
assert _l in _r, f"left : {_l!r}\nright: {_r!r}\nop   : in"
