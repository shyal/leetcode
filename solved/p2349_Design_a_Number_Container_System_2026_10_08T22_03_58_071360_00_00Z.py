# combo chain: data-sync, problem 2 of 17. Run `make combos data-sync` to see
# the chain and what is done this pass; the chain is saved in graph/chains/data-sync.json.
"""
URL: https://leetcode.com/problems/design-a-number-container-system/description/?envType=problem-list-v2&envId=vn57k9wr

2349. Design a Number Container System

Design a number container system that can do the following:

- Insert or Replace a number at the given index in the system.
- Return the smallest index for the given number in the system.

Implement the NumberContainers class:

- NumberContainers() Initializes the number container system.
- void change(int index, int number) Fills the container at index with the number. If there is already a number at that index, replace it.
- int find(int number) Returns the smallest index for the given number, or -1 if there is no index that is filled by number in the system.

Example 1:

Input
["NumberContainers","find","change","change","change","change","find","change","find"]
[[],[10],[2,10],[1,10],[3,10],[5,10],[10],[1,20],[10]]
Output
[null, -1, null, null, null, null, 1, null, 2]

Explanation
NumberContainers nc = new NumberContainers();
nc.find(10); // There is no index that is filled with number 10. Therefore, we return -1.
nc.change(2, 10); // Your container at index 2 will be filled with number 10.
nc.change(1, 10); // Your container at index 1 will be filled with number 10.
nc.change(3, 10); // Your container at index 3 will be filled with number 10.
nc.change(5, 10); // Your container at index 5 will be filled with number 10.
nc.find(10); // Number 10 is at the indices 1, 2, 3, and 5. Since the smallest index that is filled with 10 is 1, we return 1.
nc.change(1, 20); // Your container at index 1 will be filled with number 20. Note that index 1 was filled with 10 and then replaced with 20.
nc.find(10); // Number 10 is at the indices 2, 3, and 5. The smallest index that is filled with 10 is 2. Therefore, we return 2.

Constraints:

    1 <= index, number <= 10^9
    At most 10^5 calls will be made in total to change and find.

---

After much pain.

LEETCODE: Accepted (114 ms, 75.8 MB)
"""


class NumberContainers:

    def __init__(self):
        self.h = defaultdict(list)
        self.d = {}

    def change(self, index: int, number: int) -> None:
        heappush(self.h[number], index)
        self.d[index] = number

    def find(self, number: int) -> int:
        while number in self.h and self.h[number]:
            index = self.h[number][0]
            if self.d[index] == number:
                return index
            else:
                heappop(self.h[number])
        return -1


sol = NumberContainers()

print(sol.find(10))  # -1

sol.change(2, 10)
sol.change(1, 10)
sol.change(3, 10)
sol.change(5, 10)
print(sol.find(10))
assert sol.find(10) == 1
sol.change(1, 20)
assert sol.find(10) == 2


# sequence asserts for the data-sync chain: misc/data_sync_asserts.py

# the values are the reference solution's; a read the statement leaves
# open is asserted over every answer it allows

sol = NumberContainers()  # a number never stored
assert sol.find(10) == -1

sol = NumberContainers()  # the index moved to another number
sol.change(1, 10)
sol.change(1, 20)
assert sol.find(10) == -1
assert sol.find(20) == 1

sol = NumberContainers()  # the index set to the same number twice, then moved
sol.change(1, 10)
sol.change(1, 10)
sol.change(1, 20)
assert sol.find(10) == -1
assert sol.find(20) == 1

sol = NumberContainers()  # the index moved away and back
sol.change(1, 10)
sol.change(1, 20)
sol.change(1, 10)
assert sol.find(10) == 1
assert sol.find(20) == -1
sol.change(1, 20)
assert sol.find(10) == -1
assert sol.find(20) == 1

sol = NumberContainers()  # the smallest index moves, the next one answers
sol.change(1, 10)
sol.change(2, 10)
sol.change(3, 10)
sol.change(1, 20)
assert sol.find(10) == 2
sol.change(2, 30)
assert sol.find(10) == 3
sol.change(3, 10)
assert sol.find(10) == 3
sol.change(3, 40)
assert sol.find(10) == -1

sol = NumberContainers()  # a smaller index arrives later
sol.change(5, 10)
assert sol.find(10) == 5
sol.change(2, 10)
assert sol.find(10) == 2
sol.change(2, 20)
assert sol.find(10) == 5

sol = NumberContainers()  # every index leaves the number, then one returns
sol.change(1, 10)
sol.change(2, 10)
sol.change(1, 20)
sol.change(2, 20)
assert sol.find(10) == -1
sol.change(2, 10)
assert sol.find(10) == 2

sol = NumberContainers()  # the largest index and number
sol.change(1000000000, 1000000000)
assert sol.find(1000000000) == 1000000000
sol.change(1, 1000000000)
assert sol.find(1000000000) == 1

sol = NumberContainers()  # one index flips between two numbers many times
sol.change(3, 1)
sol.change(3, 2)
sol.change(3, 1)
sol.change(3, 2)
sol.change(3, 1)
assert sol.find(1) == 3
assert sol.find(2) == -1
sol.change(4, 2)
sol.change(3, 2)
assert sol.find(2) == 3
assert sol.find(1) == -1

sol = NumberContainers()  # two indices swap numbers
sol.change(1, 10)
sol.change(2, 20)
sol.change(1, 20)
sol.change(2, 10)
assert sol.find(10) == 2
assert sol.find(20) == 1

sol = NumberContainers()  # random sequence 1
sol.change(1, 30)
sol.change(1, 10)
assert sol.find(10) == 1
sol.change(1, 10)
assert sol.find(20) == -1
sol.change(1, 20)
assert sol.find(20) == 1
sol.change(1, 20)
sol.change(3, 10)
assert sol.find(30) == -1
assert sol.find(20) == 1
assert sol.find(10) == 3
sol.change(5, 30)
sol.change(4, 10)
assert sol.find(30) == 5
sol.change(5, 20)
assert sol.find(10) == 3
sol.change(2, 10)
assert sol.find(20) == 1
sol.change(5, 10)
sol.change(1, 20)
sol.change(5, 30)
sol.change(1, 20)
sol.change(4, 20)
assert sol.find(10) == 2
sol.change(4, 30)
assert sol.find(20) == 1
sol.change(2, 20)
sol.change(1, 20)
assert sol.find(10) == 3

sol = NumberContainers()  # random sequence 2
sol.change(2, 10)
sol.change(3, 10)
assert sol.find(30) == -1
sol.change(5, 20)
sol.change(4, 20)
sol.change(1, 10)
assert sol.find(40) == -1
sol.change(2, 30)
assert sol.find(40) == -1
assert sol.find(30) == 2
sol.change(4, 30)
assert sol.find(10) == 1
sol.change(2, 20)
assert sol.find(40) == -1
assert sol.find(10) == 1
sol.change(4, 10)
sol.change(3, 20)
sol.change(3, 30)
sol.change(3, 20)
sol.change(5, 20)
sol.change(1, 20)
sol.change(4, 20)
sol.change(2, 10)
sol.change(1, 10)
sol.change(3, 20)
sol.change(2, 10)
assert sol.find(20) == 3
assert sol.find(40) == -1
assert sol.find(40) == -1
sol.change(3, 30)

sol = NumberContainers()  # random sequence 3
assert sol.find(40) == -1
sol.change(2, 20)
sol.change(1, 30)
sol.change(1, 10)
sol.change(1, 30)
assert sol.find(10) == -1
sol.change(3, 20)
sol.change(1, 30)
assert sol.find(40) == -1
assert sol.find(30) == 1
sol.change(3, 30)
sol.change(5, 30)
assert sol.find(20) == 2
assert sol.find(20) == 2
sol.change(1, 10)
assert sol.find(20) == 2
sol.change(2, 30)
sol.change(4, 30)
sol.change(2, 30)
sol.change(4, 20)
assert sol.find(20) == 4
sol.change(3, 30)
sol.change(4, 30)
assert sol.find(30) == 2
sol.change(5, 30)
assert sol.find(10) == 1
sol.change(5, 10)
assert sol.find(20) == -1
assert sol.find(30) == 2
assert sol.find(10) == 1

sol = NumberContainers()  # random sequence 4
sol.change(4, 20)
assert sol.find(10) == -1
assert sol.find(30) == -1
sol.change(4, 30)
assert sol.find(40) == -1
sol.change(3, 10)
assert sol.find(40) == -1
sol.change(3, 10)
assert sol.find(40) == -1
assert sol.find(10) == 3
assert sol.find(40) == -1
sol.change(5, 10)
assert sol.find(40) == -1
assert sol.find(30) == 4
assert sol.find(20) == -1
sol.change(3, 10)
assert sol.find(10) == 3
sol.change(4, 10)
assert sol.find(30) == -1
assert sol.find(30) == -1
sol.change(1, 10)
assert sol.find(20) == -1
assert sol.find(20) == -1
sol.change(1, 20)
assert sol.find(10) == 3
assert sol.find(20) == 1
sol.change(3, 20)
sol.change(2, 10)
sol.change(3, 20)
sol.change(4, 30)

sol = NumberContainers()  # random sequence 5
assert sol.find(30) == -1
sol.change(4, 10)
sol.change(5, 20)
sol.change(4, 10)
sol.change(1, 20)
sol.change(5, 20)
sol.change(5, 20)
sol.change(2, 30)
sol.change(3, 20)
assert sol.find(30) == 2
assert sol.find(40) == -1
sol.change(2, 20)
sol.change(5, 10)
sol.change(1, 20)
assert sol.find(30) == -1
sol.change(2, 10)
sol.change(3, 20)
sol.change(3, 10)
sol.change(5, 30)
assert sol.find(40) == -1
assert sol.find(10) == 2
sol.change(3, 30)
sol.change(1, 20)
sol.change(3, 30)
assert sol.find(40) == -1
sol.change(1, 10)
assert sol.find(40) == -1
assert sol.find(30) == 3
assert sol.find(20) == -1
sol.change(4, 20)

sol = NumberContainers()  # random sequence 6
sol.change(3, 10)
sol.change(4, 30)
assert sol.find(10) == 3
sol.change(2, 10)
assert sol.find(30) == 4
assert sol.find(40) == -1
assert sol.find(40) == -1
assert sol.find(10) == 2
assert sol.find(30) == 4
assert sol.find(10) == 2
assert sol.find(20) == -1
sol.change(5, 20)
sol.change(1, 30)
sol.change(2, 30)
sol.change(2, 10)
sol.change(2, 10)
assert sol.find(20) == 5
assert sol.find(10) == 2
sol.change(2, 30)
sol.change(3, 20)
assert sol.find(10) == -1
sol.change(4, 10)
sol.change(1, 20)
assert sol.find(40) == -1
sol.change(5, 20)
assert sol.find(20) == 1
assert sol.find(40) == -1
assert sol.find(10) == 4
assert sol.find(40) == -1
sol.change(1, 10)

sol = NumberContainers()  # random sequence 7
sol.change(1, 10)
sol.change(2, 20)
sol.change(2, 20)
assert sol.find(20) == 2
assert sol.find(10) == 1
assert sol.find(20) == 2
sol.change(2, 30)
assert sol.find(10) == 1
sol.change(5, 10)
assert sol.find(20) == -1
sol.change(4, 30)
sol.change(2, 10)
sol.change(5, 30)
sol.change(3, 30)
sol.change(3, 30)
sol.change(1, 20)
sol.change(1, 20)
assert sol.find(20) == 1
sol.change(2, 10)
sol.change(1, 10)
sol.change(5, 30)
sol.change(1, 30)
assert sol.find(20) == -1
sol.change(5, 20)
sol.change(4, 10)
sol.change(4, 30)
assert sol.find(20) == 5
assert sol.find(30) == 1
assert sol.find(40) == -1
sol.change(5, 30)

sol = NumberContainers()  # random sequence 8
sol.change(5, 30)
sol.change(4, 10)
sol.change(5, 30)
sol.change(3, 10)
sol.change(5, 20)
sol.change(2, 20)
sol.change(2, 10)
sol.change(3, 30)
sol.change(1, 30)
assert sol.find(20) == 5
assert sol.find(10) == 2
assert sol.find(20) == 5
assert sol.find(40) == -1
sol.change(4, 20)
assert sol.find(10) == 2
sol.change(5, 30)
assert sol.find(40) == -1
sol.change(1, 10)
assert sol.find(40) == -1
sol.change(5, 30)
assert sol.find(30) == 3
sol.change(2, 20)
sol.change(1, 10)
sol.change(1, 30)
assert sol.find(10) == -1
assert sol.find(20) == 2
assert sol.find(20) == 2
sol.change(3, 10)
sol.change(2, 30)
sol.change(3, 20)

sol = NumberContainers()  # random sequence 9
assert sol.find(40) == -1
sol.change(5, 30)
sol.change(5, 30)
assert sol.find(30) == 5
sol.change(3, 20)
assert sol.find(40) == -1
sol.change(5, 30)
sol.change(4, 20)
sol.change(2, 10)
sol.change(5, 10)
sol.change(5, 20)
sol.change(5, 10)
assert sol.find(30) == -1
sol.change(1, 20)
sol.change(3, 10)
sol.change(4, 20)
sol.change(5, 10)
sol.change(1, 10)
assert sol.find(30) == -1
sol.change(4, 10)
assert sol.find(20) == -1
assert sol.find(40) == -1
assert sol.find(10) == 1
assert sol.find(20) == -1
sol.change(2, 10)
assert sol.find(10) == 1
assert sol.find(20) == -1
sol.change(3, 20)
sol.change(2, 20)
sol.change(3, 30)

sol = NumberContainers()  # random sequence 10
assert sol.find(10) == -1
assert sol.find(10) == -1
assert sol.find(40) == -1
assert sol.find(40) == -1
assert sol.find(20) == -1
sol.change(5, 30)
sol.change(1, 10)
assert sol.find(20) == -1
sol.change(4, 30)
sol.change(3, 10)
sol.change(5, 20)
sol.change(5, 30)
sol.change(1, 20)
sol.change(2, 20)
sol.change(4, 10)
sol.change(1, 20)
sol.change(4, 30)
sol.change(3, 30)
sol.change(4, 30)
sol.change(2, 20)
sol.change(5, 20)
sol.change(3, 30)
assert sol.find(20) == 1
sol.change(4, 20)
sol.change(1, 30)
sol.change(5, 10)
assert sol.find(20) == 2
assert sol.find(20) == 2
sol.change(5, 30)
sol.change(4, 20)

sol = NumberContainers()  # random sequence 11
assert sol.find(10) == -1
sol.change(3, 20)
sol.change(4, 20)
assert sol.find(30) == -1
sol.change(3, 10)
assert sol.find(10) == 3
sol.change(5, 20)
sol.change(5, 10)
sol.change(1, 10)
assert sol.find(10) == 1
sol.change(4, 10)
assert sol.find(30) == -1
assert sol.find(30) == -1
assert sol.find(30) == -1
sol.change(2, 30)
sol.change(4, 10)
assert sol.find(30) == 2
assert sol.find(10) == 1
assert sol.find(20) == -1
sol.change(2, 20)
assert sol.find(20) == 2
sol.change(2, 20)
sol.change(2, 10)
assert sol.find(10) == 1
assert sol.find(40) == -1
assert sol.find(10) == 1
sol.change(5, 10)
sol.change(3, 20)
sol.change(1, 30)
sol.change(5, 30)

sol = NumberContainers()  # random sequence 12
assert sol.find(40) == -1
sol.change(2, 20)
sol.change(5, 10)
assert sol.find(30) == -1
assert sol.find(30) == -1
sol.change(2, 20)
sol.change(2, 10)
sol.change(5, 10)
sol.change(4, 30)
sol.change(2, 10)
assert sol.find(20) == -1
assert sol.find(40) == -1
assert sol.find(20) == -1
sol.change(3, 20)
assert sol.find(40) == -1
sol.change(2, 20)
assert sol.find(10) == 5
sol.change(5, 30)
assert sol.find(10) == -1
sol.change(3, 20)
assert sol.find(40) == -1
assert sol.find(10) == -1
sol.change(2, 30)
assert sol.find(20) == 3
sol.change(5, 10)
assert sol.find(20) == 3
assert sol.find(20) == 3
sol.change(4, 30)
assert sol.find(10) == 5
sol.change(5, 30)

sol = NumberContainers()  # random sequence 13
assert sol.find(30) == -1
assert sol.find(40) == -1
assert sol.find(40) == -1
sol.change(5, 20)
sol.change(1, 20)
sol.change(2, 30)
assert sol.find(40) == -1
sol.change(3, 20)
sol.change(5, 10)
sol.change(3, 30)
sol.change(2, 30)
sol.change(1, 10)
sol.change(5, 10)
sol.change(3, 20)
sol.change(3, 30)
assert sol.find(20) == -1
sol.change(3, 30)
sol.change(1, 20)
sol.change(3, 20)
sol.change(4, 10)
sol.change(1, 10)
assert sol.find(20) == 3
assert sol.find(30) == 2
sol.change(4, 10)
sol.change(2, 10)
assert sol.find(10) == 1
sol.change(4, 10)
sol.change(3, 20)
sol.change(2, 20)
sol.change(5, 30)

sol = NumberContainers()  # random sequence 14
sol.change(4, 20)
assert sol.find(30) == -1
assert sol.find(30) == -1
sol.change(1, 10)
assert sol.find(40) == -1
assert sol.find(10) == 1
sol.change(2, 20)
sol.change(2, 10)
sol.change(4, 30)
sol.change(1, 30)
sol.change(5, 10)
assert sol.find(10) == 2
sol.change(3, 20)
assert sol.find(40) == -1
sol.change(1, 30)
assert sol.find(10) == 2
assert sol.find(30) == 1
assert sol.find(20) == 3
assert sol.find(20) == 3
sol.change(2, 30)
sol.change(3, 20)
sol.change(3, 30)
assert sol.find(20) == -1
assert sol.find(30) == 1
assert sol.find(20) == -1
sol.change(1, 10)
sol.change(2, 20)
assert sol.find(40) == -1
sol.change(3, 20)
sol.change(1, 10)

sol = NumberContainers()  # random sequence 15
assert sol.find(40) == -1
sol.change(1, 30)
assert sol.find(30) == 1
assert sol.find(10) == -1
sol.change(1, 30)
sol.change(4, 20)
assert sol.find(10) == -1
sol.change(2, 10)
sol.change(3, 10)
sol.change(4, 10)
sol.change(1, 30)
assert sol.find(40) == -1
sol.change(4, 10)
assert sol.find(10) == 2
assert sol.find(10) == 2
sol.change(4, 30)
assert sol.find(20) == -1
assert sol.find(10) == 2
assert sol.find(40) == -1
sol.change(3, 10)
sol.change(4, 10)
sol.change(1, 30)
sol.change(5, 20)
assert sol.find(30) == 1
assert sol.find(40) == -1
sol.change(3, 30)
sol.change(5, 30)
sol.change(1, 30)
assert sol.find(30) == 1
sol.change(5, 30)

sol = NumberContainers()  # random sequence 16
sol.change(3, 30)
sol.change(3, 30)
sol.change(4, 10)
sol.change(1, 20)
sol.change(4, 30)
sol.change(1, 30)
sol.change(5, 20)
sol.change(3, 10)
assert sol.find(30) == 1
assert sol.find(20) == 5
assert sol.find(30) == 1
assert sol.find(40) == -1
sol.change(2, 10)
sol.change(2, 10)
assert sol.find(20) == 5
sol.change(4, 10)
sol.change(5, 20)
sol.change(4, 10)
assert sol.find(30) == 1
sol.change(3, 20)
assert sol.find(20) == 3
assert sol.find(30) == 1
sol.change(5, 20)
sol.change(4, 20)
assert sol.find(40) == -1
sol.change(1, 10)
assert sol.find(10) == 1
assert sol.find(10) == 1
sol.change(4, 10)
sol.change(4, 10)

sol = NumberContainers()  # random sequence 17
sol.change(4, 10)
sol.change(5, 20)
sol.change(5, 10)
sol.change(5, 10)
sol.change(5, 20)
sol.change(2, 10)
sol.change(2, 30)
sol.change(4, 30)
assert sol.find(20) == 5
assert sol.find(20) == 5
assert sol.find(10) == -1
sol.change(4, 20)
sol.change(1, 20)
assert sol.find(40) == -1
sol.change(3, 20)
sol.change(2, 20)
sol.change(3, 10)
sol.change(2, 10)
sol.change(5, 30)
sol.change(3, 30)
sol.change(2, 30)
sol.change(2, 20)
sol.change(4, 10)
sol.change(3, 10)
sol.change(3, 10)
sol.change(3, 10)
sol.change(2, 10)
sol.change(5, 20)
sol.change(3, 10)
assert sol.find(10) == 2

sol = NumberContainers()  # random sequence 18
assert sol.find(40) == -1
sol.change(2, 20)
assert sol.find(30) == -1
sol.change(5, 30)
assert sol.find(10) == -1
sol.change(3, 30)
sol.change(3, 10)
sol.change(1, 30)
sol.change(1, 30)
sol.change(1, 10)
sol.change(4, 30)
sol.change(5, 20)
assert sol.find(30) == 4
sol.change(3, 30)
sol.change(2, 10)
sol.change(5, 20)
sol.change(4, 10)
sol.change(1, 10)
sol.change(3, 20)
sol.change(4, 20)
sol.change(5, 10)
sol.change(5, 30)
sol.change(4, 10)
assert sol.find(30) == 5
sol.change(5, 30)
sol.change(1, 30)
assert sol.find(30) == 1
assert sol.find(10) == 2
assert sol.find(40) == -1
assert sol.find(40) == -1

sol = NumberContainers()  # random sequence 19
assert sol.find(10) == -1
assert sol.find(10) == -1
assert sol.find(30) == -1
sol.change(3, 30)
assert sol.find(40) == -1
sol.change(4, 10)
sol.change(5, 20)
assert sol.find(40) == -1
sol.change(3, 30)
sol.change(2, 30)
assert sol.find(10) == 4
sol.change(3, 10)
assert sol.find(20) == 5
sol.change(2, 30)
sol.change(1, 30)
assert sol.find(10) == 3
assert sol.find(40) == -1
sol.change(1, 30)
sol.change(3, 30)
assert sol.find(10) == 4
sol.change(1, 10)
sol.change(2, 10)
assert sol.find(30) == 3
sol.change(1, 10)
sol.change(5, 30)
sol.change(3, 30)
sol.change(5, 20)
sol.change(5, 30)
sol.change(5, 10)
sol.change(5, 10)

sol = NumberContainers()  # random sequence 20
sol.change(2, 20)
sol.change(1, 10)
assert sol.find(40) == -1
assert sol.find(30) == -1
assert sol.find(10) == 1
sol.change(2, 10)
assert sol.find(40) == -1
sol.change(5, 30)
sol.change(3, 10)
sol.change(1, 30)
sol.change(5, 30)
assert sol.find(30) == 1
sol.change(3, 30)
sol.change(5, 20)
assert sol.find(40) == -1
assert sol.find(30) == 1
sol.change(5, 10)
assert sol.find(20) == -1
sol.change(5, 10)
sol.change(4, 20)
sol.change(1, 10)
assert sol.find(40) == -1
assert sol.find(10) == 1
sol.change(5, 10)
sol.change(5, 10)
assert sol.find(20) == 4
sol.change(1, 10)
sol.change(2, 30)
sol.change(3, 10)
sol.change(3, 30)
