# combo chain: backend, problem 6 of 10. Run `make combos backend` to see
# the chain and what is done this lap; the chain is saved in graph/chains/backend.json.
"""
URL: https://leetcode.com/problems/lru-cache/description/?envType=problem-list-v2&envId=vn57k9wr

146. LRU Cache

Design a data structure that follows the constraints of a Least Recently Used (LRU) cache.

Implement the LRUCache class:

- LRUCache(int capacity) Initialize the LRU cache with positive size capacity.
- int get(int key) Return the value of the key if the key exists, otherwise return -1.
- void put(int key, int value) Update the value of the key if the key exists. Otherwise, add the key-value pair to the cache. If the number of keys exceeds the capacity from this operation, evict the least recently used key.

The functions get and put must each run in O(1) average time complexity.

Example 1:

Input
["LRUCache","put","put","get","put","get","put","get","get","get"]
[[2],[1,1],[2,2],[1],[3,3],[2],[4,4],[1],[3],[4]]
Output
[null,null,null,1,null,-1,null,-1,3,4]

Explanation
LRUCache lRUCache = new LRUCache(2);
lRUCache.put(1, 1); // cache is {1=1}
lRUCache.put(2, 2); // cache is {1=1, 2=2}
lRUCache.get(1);    // return 1
lRUCache.put(3, 3); // LRU key was 2, evicts key 2, cache is {1=1, 3=3}
lRUCache.get(2);    // returns -1 (not found)
lRUCache.put(4, 4); // LRU key was 1, evicts key 1, cache is {4=4, 3=3}
lRUCache.get(1);    // return -1 (not found)
lRUCache.get(3);    // return 3
lRUCache.get(4);    // return 4

Constraints:

    1 <= capacity <= 3000
    0 <= key <= 10^4
    0 <= value <= 10^5
    At most 2 * 10^5 calls will be made to get and put.

---

LEETCODE: Accepted (24 ms, 29.2 MB)
"""


class LRUCache:

    def __init__(self, capacity: int):
        self.d = OrderedDict()
        self.c = capacity

    def get(self, key: int) -> int:
        if key in self.d:
            self.d.move_to_end(key)
            return self.d[key]
        return -1

    def put(self, key: int, value: int) -> None:
        if key in self.d:
            self.d.move_to_end(key)
        self.d[key] = value
        evict_n = len(self.d) - self.c
        for _ in range(evict_n):
            self.d.popitem(last=False)


sol = LRUCache(2)

print(sol.put(1, 1))  # None
print(sol.put(2, 2))  # None
print(sol.get(1))  # 1
print(sol.put(3, 3))  # None
print(sol.get(2))  # -1
print(sol.put(4, 4))  # None
print(sol.get(1))  # -1
print(sol.get(3))  # 3
print(sol.get(4))  # 4

# The above prints correspond to the example outputs, with None for put operations.

# Assertions for the example
cache = LRUCache(2)
cache.put(1, 1)
cache.put(2, 2)
assert cache.get(1) == 1
cache.put(3, 3)
assert cache.get(2) == -1
cache.put(4, 4)
assert cache.get(1) == -1
assert cache.get(3) == 3
assert cache.get(4) == 4

# the leetcode case that failed: put on a key already present overwrites the
# value and counts as a use, so it is not the one evicted next
cache = LRUCache(2)
cache.put(2, 1)
cache.put(1, 1)
cache.put(2, 3)
cache.put(4, 1)
assert cache.get(1) == -1
assert cache.get(2) == 3

# get counts as a use: the key read survives the next eviction
cache = LRUCache(2)
cache.put(1, 1)
cache.put(2, 2)
assert cache.get(1) == 1
cache.put(3, 3)
assert cache.get(1) == 1
assert cache.get(2) == -1

# overwriting does not grow the cache past capacity
cache = LRUCache(2)
cache.put(1, 1)
cache.put(1, 2)
cache.put(2, 2)
assert cache.get(1) == 2
assert cache.get(2) == 2

# capacity 1: every new key evicts the only key
cache = LRUCache(1)
cache.put(1, 1)
cache.put(2, 2)
assert cache.get(1) == -1
assert cache.get(2) == 2

# a missing key
assert LRUCache(2).get(5) == -1
