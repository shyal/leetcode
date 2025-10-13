"""
URL: https://leetcode.com/problems/kth-largest-element-in-a-stream/description/

703. Kth Largest Element in a Stream

Design a class to find the kth largest element in a stream. Note that it is the kth largest element in the sorted order, not the kth distinct element.

Implement KthLargest class:

    KthLargest(int k, int[] nums) Initializes the object with the integer k and the stream of integers nums.
    int add(int val) Appends the integer val to the stream and returns the element representing the kth largest element in the stream.


Example 1:

Input
["KthLargest", "add", "add", "add", "add", "add"]
[[3, [4, 5, 8, 2]], [3], [5], [10], [9], [4]]
Output
[null, 4, 5, 5, 8, 8]

Explanation
KthLargest kthLargest = new KthLargest(3, [4, 5, 8, 2]);
kthLargest.add(3);   // return 4
kthLargest.add(5);   // return 5
kthLargest.add(10);  // return 5
kthLargest.add(9);   // return 8
kthLargest.add(4);   // return 8


Constraints:

    1 <= k <= 10^4
    0 <= nums.length <= 10^4
    -10^4 <= nums[i] <= 10^4
    -10^4 <= val <= 10^4
    At most 10^4 calls will be made to add.
    It is guaranteed that there will be at least k elements in the array when you search for the kth element.

---

The solution obviously requires a heap, but i wasted time getting started on it,
for some reason, so will try submitting this brute force method for now,
and revisit this question later with a proper heap implementation.

"""


class KthLargest:

    def __init__(self, k: int, nums: List[int]):
        self.nums = nums
        self.k = k

    def add(self, val: int) -> int:
        self.nums.append(val)
        self.nums.sort()
        return self.nums[-self.k]


kth = KthLargest(3, [4, 5, 8, 2])

# print(kth.add(3))
# print(kth.add(5))
# print(kth.add(10))
# print(kth.add(9))
# print(kth.add(4))

assert kth.add(5) == 5
assert kth.add(10) == 5
assert kth.add(9) == 8
assert kth.add(4) == 8

kth2 = KthLargest(1, [])
assert kth2.add(0) == 0
assert kth2.add(100) == 100
assert kth2.add(-100) == 100
assert kth2.add(50) == 100

kth3 = KthLargest(2, [-1])
assert kth3.add(0) == -1
assert kth3.add(1) == 0
assert kth3.add(-2) == 0

kth4 = KthLargest(3, [5, 5, 5, 5])
assert kth4.add(5) == 5
assert kth4.add(6) == 5
assert kth4.add(4) == 5
assert kth4.add(7) == 5

kth5 = KthLargest(4, [1, 2, 3])
assert kth5.add(4) == 1
assert kth5.add(0) == 1
assert kth5.add(5) == 2

kth6 = KthLargest(2, [-10, -20])
assert kth6.add(-15) == -15
assert kth6.add(0) == -10
