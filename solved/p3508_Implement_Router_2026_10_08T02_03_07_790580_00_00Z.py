# combo chain: backend-live-coding, problem 8 of 10. Run `make combos backend-live-coding` to see
# the chain and what is done this lap; the chain is saved in graph/chains/backend-live-coding.json.
"""
URL: https://leetcode.com/problems/implement-router/description/?envType=problem-list-v2&envId=vn57k9wr

3508. Implement Router

Design a data structure that can efficiently manage data packets in a network router. Each data packet consists of the following attributes:

- source: A unique identifier for the machine that generated the packet.
- destination: A unique identifier for the target machine.
- timestamp: The time at which the packet arrived at the router.

Implement the Router class:

Router(int memoryLimit): Initializes the Router object with a fixed memory limit.
- memoryLimit is the maximum number of packets the router can store at any given time.
- If adding a new packet would exceed this limit, the oldest packet must be removed to free up space.

bool addPacket(int source, int destination, int timestamp): Adds a packet with the given attributes to the router.
- A packet is considered a duplicate if another packet with the same source, destination, and timestamp already exists in the router.
- Return true if the packet is successfully added (i.e., it is not a duplicate); otherwise return false.

int[] forwardPacket(): Forwards the next packet in FIFO (First In First Out) order.
- Remove the packet from storage.
- Return the packet as an array [source, destination, timestamp].
- If there are no packets to forward, return an empty array.

int getCount(int destination, int startTime, int endTime):
- Returns the number of packets currently stored in the router (i.e., not yet forwarded) that have the specified destination and have timestamps in the inclusive range [startTime, endTime].

Note that queries for addPacket will be made in non-decreasing order of timestamp.

Example 1:

Input:
["Router","addPacket","addPacket","addPacket","addPacket","addPacket","forwardPacket","addPacket","getCount"]
[[3],[1,4,90],[2,5,90],[1,4,90],[3,5,95],[4,5,105],[],[5,2,110],[5,100,110]]

Output:
[null, true, true, false, true, true, [2, 5, 90], true, 1]

Explanation:
Router router = new Router(3); // Initialize Router with memoryLimit of 3.
router.addPacket(1, 4, 90); // Packet is added. Return True.
router.addPacket(2, 5, 90); // Packet is added. Return True.
router.addPacket(1, 4, 90); // This is a duplicate packet. Return False.
router.addPacket(3, 5, 95); // Packet is added. Return True
router.addPacket(4, 5, 105); // Packet is added, [1, 4, 90] is removed as number of packets exceeds memoryLimit. Return True.
router.forwardPacket(); // Return [2, 5, 90] and remove it from router.
router.addPacket(5, 2, 110); // Packet is added. Return True.
router.getCount(5, 100, 110); // The only packet with destination 5 and timestamp in the inclusive range [100, 110] is [4, 5, 105]. Return 1.

Example 2:

Input:
["Router","addPacket","forwardPacket","forwardPacket"]
[[2],[7,4,90],[],[]]

Output:
[null, true, [7, 4, 90], []]

Explanation:
Router router = new Router(2); // Initialize Router with memoryLimit of 2.
router.addPacket(7, 4, 90); // Return True.
router.forwardPacket(); // Return [7, 4, 90].
router.forwardPacket(); // There are no packets left, return [].

Constraints:

- 2 <= memoryLimit <= 10^5
- 1 <= source, destination <= 2 * 10^5
- 1 <= timestamp <= 10^9
- 1 <= startTime <= endTime <= 10^9
- At most 10^5 calls will be made to addPacket, forwardPacket, and getCount methods altogether.
- Queries for addPacket will be made in non-decreasing order of timestamp.

---

BF solve using a deque. Clearly the packet information needs to be compressed with ranges.
And of course this is totally doable in 30 minutes... sure.

class Router:

    def __init__(self, memoryLimit: int):
        self.maxpackets = memoryLimit
        self.d = deque([])

    def addPacket(self, source: int, destination: int, timestamp: int) -> bool:
        if [source, destination, timestamp] not in self.d:
            while len(self.d) + 1 > self.maxpackets:
                self.d.popleft()
            self.d.append([source, destination, timestamp])
            return True
        return False

    def forwardPacket(self) -> List[int]:
        if self.d:
            return list(self.d.popleft())
        return []

    def getCount(self, destination: int, startTime: int, endTime: int) -> int:
        count = 0
        for s, d, t in self.d:
            if d == destination and t >= startTime and t <= endTime:
                count += 1
        return count

LEETCODE: Time Limit Exceeded (744/753 cases)
"""


class Router:

    def __init__(self, memoryLimit: int):
        self.maxpackets = memoryLimit
        self.d = deque([])

    def addPacket(self, source: int, destination: int, timestamp: int) -> bool:
        if [source, destination, timestamp] not in self.d:
            while len(self.d) + 1 > self.maxpackets:
                self.d.popleft()
            self.d.append([source, destination, timestamp])
            return True
        return False

    def forwardPacket(self) -> List[int]:
        if self.d:
            return list(self.d.popleft())
        return []

    def getCount(self, destination: int, startTime: int, endTime: int) -> int:
        count = 0
        for s, d, t in self.d:
            if d == destination and t >= startTime and t <= endTime:
                count += 1
        return count


sol = Router(3)

print(sol.addPacket(1, 4, 90))  # True
print(sol.addPacket(2, 5, 90))  # True
print(sol.addPacket(1, 4, 90))  # False
print(sol.addPacket(3, 5, 95))  # True
print(sol.addPacket(4, 5, 105))  # True, oldest packet removed
print(sol.forwardPacket())  # [2, 5, 90]
print(sol.addPacket(5, 2, 110))  # True
print(sol.getCount(5, 100, 110))  # 1

# Example 1 asserts
router1 = Router(3)
assert router1.addPacket(1, 4, 90) == True
assert router1.addPacket(2, 5, 90) == True
assert router1.addPacket(1, 4, 90) == False
assert router1.addPacket(3, 5, 95) == True
assert router1.addPacket(4, 5, 105) == True
assert router1.forwardPacket() == [2, 5, 90]
assert router1.addPacket(5, 2, 110) == True
assert router1.getCount(5, 100, 110) == 1

# Example 2 asserts
router2 = Router(2)
assert router2.addPacket(7, 4, 90) == True
assert router2.forwardPacket() == [7, 4, 90]
assert router2.forwardPacket() == []

assert Router(2).addPacket(1, 1, 1) == True
assert Router(2).addPacket(1, 1, 1) == True
assert Router(1).addPacket(1, 1, 1) == True
assert Router(1).addPacket(2, 2, 2) == True
assert Router(1).forwardPacket() == []
assert Router(1).forwardPacket() == []
assert Router(10**5).addPacket(1, 1, 10**9) == True
assert Router(10**5).addPacket(1, 1, 10**9 - 1) == True
assert Router(10**5).addPacket(1, 1, 10**9 - 2) == True
assert Router(10**5).getCount(1, 10**9 - 2, 10**9) == 0
assert Router(10**5).forwardPacket() == []

# leetcode case: a stored packet is counted by its destination and timestamp
router3 = Router(4)
assert router3.addPacket(4, 5, 1) == True
assert router3.getCount(5, 1, 1) == 1
assert router3.getCount(4, 1, 1) == 0
assert router3.getCount(5, 2, 2) == 0

# eviction removes the oldest packet, forwarding removes the next
router4 = Router(2)
assert router4.addPacket(1, 9, 10) == True
assert router4.addPacket(2, 9, 20) == True
assert router4.addPacket(3, 9, 30) == True
assert router4.getCount(9, 10, 30) == 2
assert router4.forwardPacket() == [2, 9, 20]
assert router4.getCount(9, 10, 30) == 1
assert router4.addPacket(1, 9, 10) == True
