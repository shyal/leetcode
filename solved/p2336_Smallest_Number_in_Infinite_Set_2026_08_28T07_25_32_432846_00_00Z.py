"""
URL: https://leetcode.com/problems/smallest-number-in-infinite-set/description/?envType=problem-list-v2&envId=vn57k9wr

2336. Smallest Number in Infinite Set

You have a set which contains all positive integers [1, 2, 3, 4, 5, ...].

Implement the SmallestInfiniteSet class:

- SmallestInfiniteSet() Initializes the SmallestInfiniteSet object to contain all positive integers.
- int popSmallest() Removes and returns the smallest integer contained in the infinite set.
- void addBack(int num) Adds a positive integer num back into the infinite set, if it is not already in the infinite set.

Example 1:

Input
["SmallestInfiniteSet","addBack","popSmallest","popSmallest","popSmallest","addBack","popSmallest","popSmallest","popSmallest"]
[[],[2],[],[],[],[1],[],[],[]]
Output
[null, null, 1, 2, 3, null, 1, 4, 5]

Explanation
SmallestInfiniteSet smallestInfiniteSet = new SmallestInfiniteSet();
smallestInfiniteSet.addBack(2);    // 2 is already in the set, so no change is made.
smallestInfiniteSet.popSmallest(); // return 1, since 1 is the smallest number, and remove it from the set.
smallestInfiniteSet.popSmallest(); // return 2, and remove it from the set.
smallestInfiniteSet.popSmallest(); // return 3, and remove it from the set.
smallestInfiniteSet.addBack(1);    // 1 is added back to the set.
smallestInfiniteSet.popSmallest(); // return 1, since 1 was added back to the set and
                                   // is the smallest number, and remove it from the set.
smallestInfiniteSet.popSmallest(); // return 4, and remove it from the set.
smallestInfiniteSet.popSmallest(); // return 5, and remove it from the set.

Constraints:

    1 <= num <= 1000
    At most 1000 calls will be made in total to popSmallest and addBack.

---

First rather naive solution. Use a deque, with bisect. But this is not efficient due to the insert
on addBack.

Next i need to think of a better ds for insertion. Worth investigating a deque next.

Oh well, since the constraints are quite friendly, the bisect version passes just fine on leetcode.

"""


class SmallestInfiniteSet:

    def __init__(self):
        self.set = deque([*range(1, 1001)])

    def popSmallest(self) -> int:
        if self.set:
            ret = self.set.popleft()
            return ret

    def addBack(self, num: int) -> None:
        ind = bisect_left(self.set, num)
        if self.set[ind] == num:
            return
        self.set.insert(ind, num)


# class SmallestInfiniteSet:

#     def __init__(self):
#         self._min = 1
#         self.added_back = []

#     def popSmallest(self) -> int:
#         if self.added_back:
#             min_added_back = self.added_back[0]
#             if min_added_back < self._min:
#                 return heappop(self.added_back)
#             else:
#                 self._min += 1
#                 return self._min - 1
#         else:
#             self._min += 1
#             return self._min - 1

#     def addBack(self, num: int) -> None:
#         if num < self._min:
#             heappush(self.added_back, num)
#         else:
#             pass


# sol = SmallestInfiniteSet()

# print(sol.popSmallest())  # 1

sol = SmallestInfiniteSet()
sol.addBack(2)
assert sol.popSmallest() == 1
assert sol.popSmallest() == 2
assert sol.popSmallest() == 3
sol.addBack(1)
assert sol.popSmallest() == 1
assert sol.popSmallest() == 4
assert sol.popSmallest() == 5


# addBack below the current front: it must come out before the rest
sol = SmallestInfiniteSet()
assert sol.popSmallest() == 1
assert sol.popSmallest() == 2
assert sol.popSmallest() == 3
sol.addBack(2)
assert sol.popSmallest() == 2
assert sol.popSmallest() == 4

# several addBacks land back in sorted order, whatever order they arrive in
sol = SmallestInfiniteSet()
for _ in range(5):
    sol.popSmallest()  # removes 1..5
sol.addBack(4)
sol.addBack(2)
assert sol.popSmallest() == 2
assert sol.popSmallest() == 4
assert sol.popSmallest() == 6

# a duplicate addBack is a no-op
sol = SmallestInfiniteSet()
assert sol.popSmallest() == 1
sol.addBack(1)
sol.addBack(1)
assert sol.popSmallest() == 1
assert sol.popSmallest() == 2

# addBack of a number still in the set is a no-op, even far from the front
sol = SmallestInfiniteSet()
sol.addBack(999)
assert sol.popSmallest() == 1

# constraint edge: num goes up to 1000
sol = SmallestInfiniteSet()
sol.addBack(1000)  # present, so no change
assert sol.popSmallest() == 1

# pop/addBack ping-pong on the same value
sol = SmallestInfiniteSet()
for _ in range(3):
    assert sol.popSmallest() == 1
    sol.addBack(1)
assert sol.popSmallest() == 1

# max load: the full 1000-call budget spent on pops walks 1..1000
sol = SmallestInfiniteSet()
for want in range(1, 1001):
    assert sol.popSmallest() == want
