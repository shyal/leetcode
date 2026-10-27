# URL: https://leetcode.com/problems/design-circular-deque/description/?envType=problem-list-v2&envId=vn57k9wr
#
# 641. Design Circular Deque
#
# Design your implementation of the circular double-ended queue (deque).
#
# Implement the MyCircularDeque class:
#
# - MyCircularDeque(int k) Initializes the deque with a maximum size of k.
# - boolean insertFront() Adds an item at the front of Deque. Returns true if the operation is successful, or false otherwise.
# - boolean insertLast() Adds an item at the rear of Deque. Returns true if the operation is successful, or false otherwise.
# - boolean deleteFront() Deletes an item from the front of Deque. Returns true if the operation is successful, or false otherwise.
# - boolean deleteLast() Deletes an item from the rear of Deque. Returns true if the operation is successful, or false otherwise.
# - int getFront() Returns the front item from the Deque. Returns -1 if the deque is empty.
# - int getRear() Returns the last item from Deque. Returns -1 if the deque is empty.
# - boolean isEmpty() Returns true if the deque is empty, or false otherwise.
# - boolean isFull() Returns true if the deque is full, or false otherwise.
#
# Example 1:
#
# Input
# ["MyCircularDeque","insertLast","insertLast","insertFront","insertFront","getRear","isFull","deleteLast","insertFront","getFront"]
# [[3],[1],[2],[3],[4],[],[],[],[4],[]]
# Output
# [null, true, true, true, false, 2, true, true, true, 4]
#
# Explanation
# MyCircularDeque myCircularDeque = new MyCircularDeque(3);
# myCircularDeque.insertLast(1);  // return True
# myCircularDeque.insertLast(2);  // return True
# myCircularDeque.insertFront(3); // return True
# myCircularDeque.insertFront(4); // return False, the queue is full.
# myCircularDeque.getRear();      // return 2
# myCircularDeque.isFull();       // return True
# myCircularDeque.deleteLast();   // return True
# myCircularDeque.insertFront(4); // return True
# myCircularDeque.getFront();     // return 4
#
# Constraints:
#
#     1 <= k <= 1000
#     0 <= value <= 1000
#     At most 2000 calls will be made to insertFront, insertLast, deleteFront, deleteLast, getFront, getRear, isEmpty, isFull.
#
# ---
# LEETCODE: Accepted (17 ms, 19.9 MB)

# mu 0.13

class MyCircularDeque
  def __init__(k: int)
    self.k = k
    self.deque = deque([])

  def insertFront(value: int) -> bool
    if not self.isFull()
      self.deque.appendleft(value)
      return true
    false

  def insertLast(value: int) -> bool
    if not self.isFull()
      self.deque.append(value)
      return true
    false

  def deleteFront() -> bool
    if not self.isEmpty()
      self.deque.popleft()
      return true
    false

  def deleteLast() -> bool
    if not self.isEmpty()
      self.deque.pop()
      return true
    false

  def getFront() -> int
    if not self.isEmpty()
      return self.deque[0]
    -1

  def getRear() -> int
    if not self.isEmpty()
      return self.deque[-1]
    -1

  def isEmpty() -> bool
    len self.deque == 0

  def isFull() -> bool
    len self.deque == self.k

sol = MyCircularDeque(3)

print(sol.insertLast(1))  # True

print(sol.insertLast(2))  # True
print(sol.insertFront(3))  # True
print(sol.insertFront(4))  # False
print(sol.getRear())  # 2
print(sol.isFull())  # True
print(sol.deleteLast())  # True
print(sol.insertFront(4))  # True
print(sol.getFront())  # 4

assert sol.insertLast(1) is false
assert sol.insertLast(2) is false
assert sol.insertFront(3) is false
assert sol.insertFront(4) is false
assert sol.getRear() == 1
assert sol.isFull() is true
assert sol.deleteLast() is true
assert sol.insertFront(4) is true
assert sol.getFront() == 4

assert MyCircularDeque(1).insertFront(10) == true
assert MyCircularDeque(1).insertLast(20) == true
assert MyCircularDeque(1).deleteFront() == false
assert MyCircularDeque(1).deleteLast() == false
assert MyCircularDeque(2).insertLast(5) == true
assert MyCircularDeque(2).insertLast(5) == true
assert MyCircularDeque(2).insertFront(5) == true
assert MyCircularDeque(2).deleteFront() == false
assert MyCircularDeque(2).deleteLast() == false
