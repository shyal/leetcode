"""
URL: https://leetcode.com/problems/design-ride-sharing-system/description/?envType=problem-list-v2&envId=vn57k9wr

3829. Design Ride Sharing System

A ride sharing system manages ride requests from riders and availability from drivers. Riders request rides, and drivers become available over time. The system should match riders and drivers in the order they arrive.

Implement the RideSharingSystem class:

- RideSharingSystem() Initializes the system.
- void addRider(int riderId) Adds a new rider with the given riderId.
- void addDriver(int driverId) Adds a new driver with the given driverId.
- int[] matchDriverWithRider() Matches the earliest available driver with the earliest waiting rider and removes both of them from the system. Returns an integer array of size 2 where result = [driverId, riderId] if a match is made. If no match is available, returns [-1, -1].
- void cancelRider(int riderId) Cancels the ride request of the rider with the given riderId if the rider exists and has not yet been matched.

Example 1:

Input:
["RideSharingSystem","addRider","addDriver","addRider","matchDriverWithRider","addDriver","cancelRider","matchDriverWithRider","matchDriverWithRider"]
[[],[3],[2],[1],[],[5],[3],[],[]]

Output:
[null, null, null, null, [2, 3], null, null, [5, 1], [-1, -1]]

Explanation:
RideSharingSystem rideSharingSystem = new RideSharingSystem(); // Initializes the system
rideSharingSystem.addRider(3); // rider 3 joins the queue
rideSharingSystem.addDriver(2); // driver 2 joins the queue
rideSharingSystem.addRider(1); // rider 1 joins the queue
rideSharingSystem.matchDriverWithRider(); // returns [2, 3]
rideSharingSystem.addDriver(5); // driver 5 becomes available
rideSharingSystem.cancelRider(3); // rider 3 is already matched, cancel has no effect
rideSharingSystem.matchDriverWithRider(); // returns [5, 1]
rideSharingSystem.matchDriverWithRider(); // returns [-1, -1]

Example 2:

Input:
["RideSharingSystem","addRider","addDriver","addDriver","matchDriverWithRider","addRider","cancelRider","matchDriverWithRider"]
[[],[8],[8],[6],[],[2],[2],[]]

Output:
[null, null, null, null, [8, 8], null, null, [-1, -1]]

Explanation:
RideSharingSystem rideSharingSystem = new RideSharingSystem(); // Initializes the system
rideSharingSystem.addRider(8); // rider 8 joins the queue
rideSharingSystem.addDriver(8); // driver 8 joins the queue
rideSharingSystem.addDriver(6); // driver 6 joins the queue
rideSharingSystem.matchDriverWithRider(); // returns [8, 8]
rideSharingSystem.addRider(2); // rider 2 joins the queue
rideSharingSystem.cancelRider(2); // rider 2 cancels
rideSharingSystem.matchDriverWithRider(); // returns [-1, -1]

Constraints:

    1 <= riderId, driverId <= 1000
    Each riderId is unique among riders and is added at most once.
    Each driverId is unique among drivers and is added at most once.
    At most 1000 calls will be made in total to addRider, addDriver, matchDriverWithRider, and cancelRider.
---
I'm not seeing what's difficult here... so clearly i'm missing the point. sounds like two double ended queues
both riders and drivers get added to the right, and taken from the left.

Let's look at this test case:

print(sol.addRider(3))  # None

print(sol.addDriver(2))  # None
print(sol.addRider(1))  # None
print(sol.matchDriverWithRider())  # [2, 3]
print(sol.addDriver(5))  # None
print(sol.cancelRider(3))  # None
print(sol.matchDriverWithRider())  # [5, 1]
print(sol.matchDriverWithRider())  # [-1, -1]

LEETCODE: Accepted (58 ms, 20.3 MB)
"""


# mu 0.10
# class RideSharingSystem
#   def __init__()
#     self.riders = deque([])
#     self.drivers = deque([])
#     self.cancelledRiders = set([])
#     self.addedRiders = set([])
#
#   def addRider(riderId: int) -> none
#     self.addedRiders.add(riderId)
#     self.riders <- riderId
#     None
#
#   def addDriver(driverId: int) -> none
#     self.drivers <- driverId
#     None
#
#   def matchDriverWithRider() -> [int]
#     if self.riders and self.drivers
#       while self.riders and self.riders[0] in self.cancelledRiders
#         self.riders.popleft()
#       if self.riders
#         driver = self.drivers.popleft()
#         rider = self.riders.popleft()
#         self.addedRiders.discard(rider)
#         return [driver, rider]
#     [-1, -1]
#
#   def cancelRider(riderId: int) -> none
#     if riderId in self.addedRiders
#       self.cancelledRiders.add(riderId)
#
#
# # submitted design-ride-sharing-system as 2170753502; waiting for leetcode...
# # LEETCODE: Wrong Answer (800/844 cases)
# # input ["RideSharingSystem","addDriver","cancelRider","addRider","matchDriverWithRider"] [[],[2],[1],[1],[]]
# # expected [null,null,null,null,[2,1]]
# # got [null,null,null,null,[-1,-1]]

class RideSharingSystem:
    def __init__(self):
        self.riders = deque([])
        self.drivers = deque([])
        self.cancelledRiders = set([])
        self.addedRiders = set([])

    def addRider(self, riderId: int) -> None:
        self.addedRiders.add(riderId)
        self.riders.append(riderId)
        None

    def addDriver(self, driverId: int) -> None:
        self.drivers.append(driverId)
        None

    def matchDriverWithRider(self) -> list[int]:
        if self.riders and self.drivers:
            while self.riders and self.riders[0] in self.cancelledRiders:
                self.riders.popleft()
            if self.riders:
                driver = self.drivers.popleft()
                rider = self.riders.popleft()
                self.addedRiders.discard(rider)
                return [driver, rider]
        return [-1, -1]

    def cancelRider(self, riderId: int) -> None:
        if riderId in self.addedRiders:
            self.cancelledRiders.add(riderId)


sol = RideSharingSystem()
sol.addDriver(2)
sol.cancelRider(1)
sol.addRider(1)
_l, _r = sol.matchDriverWithRider(), [2, 1]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol = RideSharingSystem()
sol.cancelRider(2)
sol.addRider(5)
sol.addRider(8)
sol.addRider(10)
sol.cancelRider(5)
sol.addRider(1)
sol.cancelRider(1)
_l, _r = sol.matchDriverWithRider(), [-1, -1]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.addDriver(12)
sol.cancelRider(1)
sol.cancelRider(9)
_l, _r = sol.matchDriverWithRider(), [12, 8]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.matchDriverWithRider(), [-1, -1]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.matchDriverWithRider(), [-1, -1]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.cancelRider(12)
sol.addDriver(5)
sol.cancelRider(10)
sol.addRider(12)
sol.addDriver(6)
sol.addRider(11)
sol.cancelRider(3)
sol.cancelRider(9)
sol.addDriver(10)
sol.addDriver(4)
_l, _r = sol.matchDriverWithRider(), [5, 12]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.addRider(3)
_l, _r = sol.matchDriverWithRider(), [6, 11]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.addRider(9)
_l, _r = sol.matchDriverWithRider(), [10, 3]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.addRider(6)
sol = RideSharingSystem()
print(sol.addRider(3))
print(sol.addDriver(2))
print(sol.addRider(1))
print(sol.matchDriverWithRider())
print(sol.addDriver(5))
print(sol.cancelRider(3))
print(sol.matchDriverWithRider())
print(sol.matchDriverWithRider())
sol1 = RideSharingSystem()
sol1.addRider(3)
sol1.addDriver(2)
sol1.addRider(1)
_l, _r = sol1.matchDriverWithRider(), [2, 3]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol1.addDriver(5)
sol1.cancelRider(3)
_l, _r = sol1.matchDriverWithRider(), [5, 1]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol1.matchDriverWithRider(), [-1, -1]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol2 = RideSharingSystem()
sol2.addRider(8)
sol2.addDriver(8)
sol2.addDriver(6)
_l, _r = sol2.matchDriverWithRider(), [8, 8]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol2.addRider(2)
sol2.cancelRider(2)
_l, _r = sol2.matchDriverWithRider(), [-1, -1]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = RideSharingSystem().matchDriverWithRider(), [-1, -1]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol = RideSharingSystem()
sol.addRider(1)
_l, _r = sol.matchDriverWithRider(), [-1, -1]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.addDriver(2)
_l, _r = sol.matchDriverWithRider(), [2, 1]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.matchDriverWithRider(), [-1, -1]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol = RideSharingSystem()
sol.addDriver(2)
_l, _r = sol.matchDriverWithRider(), [-1, -1]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.addRider(1)
_l, _r = sol.matchDriverWithRider(), [2, 1]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol = RideSharingSystem()
sol.addRider(3)
sol.addRider(1)
sol.addDriver(2)
sol.cancelRider(3)
_l, _r = sol.matchDriverWithRider(), [2, 1]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol = RideSharingSystem()
sol.cancelRider(7)
sol.addRider(1)
sol.addDriver(2)
_l, _r = sol.matchDriverWithRider(), [2, 1]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol = RideSharingSystem()
sol.addRider(1)
sol.addDriver(2)
_l, _r = sol.matchDriverWithRider(), [2, 1]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.cancelRider(1)
sol.addDriver(3)
sol.addRider(4)
_l, _r = sol.matchDriverWithRider(), [3, 4]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol = RideSharingSystem()
sol.addRider(1)
sol.addRider(2)
sol.cancelRider(1)
sol.cancelRider(1)
sol.addDriver(5)
_l, _r = sol.matchDriverWithRider(), [5, 2]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol = RideSharingSystem()
sol.addDriver(1)
sol.addDriver(2)
sol.addDriver(3)
sol.addRider(9)
sol.addRider(8)
_l, _r = sol.matchDriverWithRider(), [1, 9]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.matchDriverWithRider(), [2, 8]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.matchDriverWithRider(), [-1, -1]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.addRider(7)
_l, _r = sol.matchDriverWithRider(), [3, 7]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol = RideSharingSystem()
sol.addRider(1)
sol.addRider(2)
sol.addRider(3)
sol.cancelRider(2)
sol.addDriver(10)
sol.addDriver(11)
_l, _r = sol.matchDriverWithRider(), [10, 1]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.matchDriverWithRider(), [11, 3]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.matchDriverWithRider(), [-1, -1]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol = RideSharingSystem()
sol.addRider(1)
sol.addRider(2)
sol.cancelRider(2)
sol.addDriver(4)
_l, _r = sol.matchDriverWithRider(), [4, 1]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.matchDriverWithRider(), [-1, -1]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol = RideSharingSystem()
sol.addRider(1000)
sol.addDriver(1000)
_l, _r = sol.matchDriverWithRider(), [1000, 1000]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol = RideSharingSystem()
sol.addRider(1)
sol.addRider(2)
sol.addDriver(3)
sol.cancelRider(1)
sol.cancelRider(2)
_l, _r = sol.matchDriverWithRider(), [-1, -1]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.addRider(4)
_l, _r = sol.matchDriverWithRider(), [3, 4]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol = RideSharingSystem()
sol.addRider(6)
sol.addRider(3)
sol.cancelRider(7)
_l, _r = sol.matchDriverWithRider(), [-1, -1]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.cancelRider(5)
_l, _r = sol.matchDriverWithRider(), [-1, -1]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.cancelRider(4)
_l, _r = sol.matchDriverWithRider(), [-1, -1]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.cancelRider(5)
sol.cancelRider(10)
sol.addRider(9)
sol.addRider(1)
_l, _r = sol.matchDriverWithRider(), [-1, -1]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.addRider(10)
sol.addRider(8)
_l, _r = sol.matchDriverWithRider(), [-1, -1]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.cancelRider(3)
sol.addRider(4)
_l, _r = sol.matchDriverWithRider(), [-1, -1]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.matchDriverWithRider(), [-1, -1]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.cancelRider(4)
sol.addRider(7)
sol.addRider(12)
sol.addDriver(8)
_l, _r = sol.matchDriverWithRider(), [8, 6]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.addRider(5)
sol.addDriver(3)
sol.addRider(11)
sol.addRider(2)
sol.addDriver(6)
sol = RideSharingSystem()
sol.cancelRider(2)
sol.addRider(5)
sol.addRider(8)
sol.addRider(10)
sol.cancelRider(5)
sol.addRider(1)
sol.cancelRider(1)
_l, _r = sol.matchDriverWithRider(), [-1, -1]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.addDriver(12)
sol.cancelRider(1)
sol.cancelRider(9)
_l, _r = sol.matchDriverWithRider(), [12, 8]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.matchDriverWithRider(), [-1, -1]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.matchDriverWithRider(), [-1, -1]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.cancelRider(12)
sol.addDriver(5)
sol.cancelRider(10)
sol.addRider(12)
sol.addDriver(6)
sol.addRider(11)
sol.cancelRider(3)
sol.cancelRider(9)
sol.addDriver(10)
sol.addDriver(4)
_l, _r = sol.matchDriverWithRider(), [5, 12]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.addRider(3)
_l, _r = sol.matchDriverWithRider(), [6, 11]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.addRider(9)
_l, _r = sol.matchDriverWithRider(), [10, 3]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.addRider(6)
sol = RideSharingSystem()
_l, _r = sol.matchDriverWithRider(), [-1, -1]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.cancelRider(7)
sol.addDriver(6)
sol.cancelRider(6)
sol.addDriver(7)
sol.addRider(3)
sol.addDriver(2)
sol.addDriver(12)
sol.cancelRider(1)
sol.cancelRider(5)
sol.cancelRider(7)
_l, _r = sol.matchDriverWithRider(), [6, 3]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.addDriver(5)
sol.addRider(12)
_l, _r = sol.matchDriverWithRider(), [7, 12]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.matchDriverWithRider(), [-1, -1]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.cancelRider(6)
sol.addDriver(8)
sol.addDriver(4)
sol.addRider(7)
_l, _r = sol.matchDriverWithRider(), [2, 7]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.addDriver(1)
sol.addRider(2)
sol.addDriver(9)
_l, _r = sol.matchDriverWithRider(), [12, 2]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.matchDriverWithRider(), [-1, -1]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.addRider(9)
sol.cancelRider(11)
sol.cancelRider(1)
_l, _r = sol.matchDriverWithRider(), [5, 9]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol = RideSharingSystem()
sol.addDriver(8)
sol.addRider(5)
sol.cancelRider(12)
sol.addDriver(9)
_l, _r = sol.matchDriverWithRider(), [8, 5]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.addDriver(6)
sol.cancelRider(4)
sol.addRider(3)
sol.cancelRider(6)
sol.addRider(10)
sol.cancelRider(1)
sol.addDriver(10)
sol.addRider(4)
sol.addDriver(12)
_l, _r = sol.matchDriverWithRider(), [9, 3]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.addDriver(1)
_l, _r = sol.matchDriverWithRider(), [6, 10]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.addDriver(11)
sol.cancelRider(2)
sol.cancelRider(12)
sol.cancelRider(12)
sol.cancelRider(3)
_l, _r = sol.matchDriverWithRider(), [10, 4]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.addRider(8)
_l, _r = sol.matchDriverWithRider(), [12, 8]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.addRider(7)
sol.addDriver(4)
sol.addDriver(2)
_l, _r = sol.matchDriverWithRider(), [1, 7]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.addDriver(3)
sol = RideSharingSystem()
sol.addDriver(4)
sol.cancelRider(11)
_l, _r = sol.matchDriverWithRider(), [-1, -1]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.addDriver(7)
sol.addRider(8)
_l, _r = sol.matchDriverWithRider(), [4, 8]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.cancelRider(12)
_l, _r = sol.matchDriverWithRider(), [-1, -1]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.addRider(9)
_l, _r = sol.matchDriverWithRider(), [7, 9]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.matchDriverWithRider(), [-1, -1]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.addDriver(9)
_l, _r = sol.matchDriverWithRider(), [-1, -1]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.addDriver(2)
_l, _r = sol.matchDriverWithRider(), [-1, -1]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.addDriver(5)
sol.cancelRider(10)
_l, _r = sol.matchDriverWithRider(), [-1, -1]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.matchDriverWithRider(), [-1, -1]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.addDriver(3)
sol.addDriver(10)
sol.addRider(10)
sol.addRider(3)
sol.cancelRider(3)
sol.addRider(1)
sol.addRider(5)
_l, _r = sol.matchDriverWithRider(), [9, 10]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.matchDriverWithRider(), [2, 1]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.addRider(2)
sol.addRider(11)
sol = RideSharingSystem()
sol.addRider(2)
_l, _r = sol.matchDriverWithRider(), [-1, -1]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.matchDriverWithRider(), [-1, -1]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.addDriver(6)
sol.addDriver(8)
_l, _r = sol.matchDriverWithRider(), [6, 2]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.matchDriverWithRider(), [-1, -1]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.matchDriverWithRider(), [-1, -1]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.addDriver(5)
sol.addRider(9)
sol.addRider(10)
_l, _r = sol.matchDriverWithRider(), [8, 9]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.matchDriverWithRider(), [5, 10]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.matchDriverWithRider(), [-1, -1]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.cancelRider(7)
sol.addDriver(7)
sol.cancelRider(6)
_l, _r = sol.matchDriverWithRider(), [-1, -1]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.addRider(12)
_l, _r = sol.matchDriverWithRider(), [7, 12]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.matchDriverWithRider(), [-1, -1]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.matchDriverWithRider(), [-1, -1]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.addRider(4)
_l, _r = sol.matchDriverWithRider(), [-1, -1]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.addRider(7)
_l, _r = sol.matchDriverWithRider(), [-1, -1]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.addRider(5)
sol.addRider(6)
_l, _r = sol.matchDriverWithRider(), [-1, -1]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.addRider(11)
sol = RideSharingSystem()
sol.addRider(3)
sol.addRider(9)
sol.cancelRider(7)
sol.addRider(5)
_l, _r = sol.matchDriverWithRider(), [-1, -1]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.addRider(2)
sol.addRider(7)
_l, _r = sol.matchDriverWithRider(), [-1, -1]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.cancelRider(12)
_l, _r = sol.matchDriverWithRider(), [-1, -1]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.addDriver(4)
_l, _r = sol.matchDriverWithRider(), [4, 3]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.matchDriverWithRider(), [-1, -1]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.addRider(6)
sol.addDriver(10)
sol.addRider(8)
sol.cancelRider(6)
sol.addDriver(2)
sol.addDriver(7)
sol.addRider(1)
sol.cancelRider(9)
sol.cancelRider(10)
sol.cancelRider(5)
sol.cancelRider(3)
sol.addDriver(5)
sol.cancelRider(12)
sol.addDriver(9)
sol.cancelRider(3)
sol.cancelRider(5)
sol.cancelRider(11)
sol = RideSharingSystem()
_l, _r = sol.matchDriverWithRider(), [-1, -1]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.matchDriverWithRider(), [-1, -1]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.addDriver(8)
sol.addDriver(7)
sol.addRider(9)
sol.addDriver(4)
_l, _r = sol.matchDriverWithRider(), [8, 9]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.addRider(12)
_l, _r = sol.matchDriverWithRider(), [7, 12]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.matchDriverWithRider(), [-1, -1]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.addDriver(12)
sol.addDriver(6)
sol.addDriver(3)
sol.cancelRider(5)
sol.cancelRider(8)
sol.addRider(7)
_l, _r = sol.matchDriverWithRider(), [4, 7]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.addRider(6)
_l, _r = sol.matchDriverWithRider(), [12, 6]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.addRider(3)
sol.addDriver(9)
sol.cancelRider(6)
sol.addRider(11)
sol.cancelRider(2)
sol.addDriver(11)
sol.addDriver(10)
_l, _r = sol.matchDriverWithRider(), [6, 3]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.addDriver(1)
sol.cancelRider(12)
sol.addRider(10)
sol = RideSharingSystem()
sol.cancelRider(8)
sol.addRider(8)
sol.addDriver(7)
_l, _r = sol.matchDriverWithRider(), [7, 8]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.addRider(1)
sol.cancelRider(5)
sol.addDriver(4)
_l, _r = sol.matchDriverWithRider(), [4, 1]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.addRider(6)
_l, _r = sol.matchDriverWithRider(), [-1, -1]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.matchDriverWithRider(), [-1, -1]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.cancelRider(11)
sol.cancelRider(6)
sol.addDriver(5)
_l, _r = sol.matchDriverWithRider(), [-1, -1]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.addRider(7)
sol.addDriver(2)
sol.addDriver(10)
sol.cancelRider(5)
_l, _r = sol.matchDriverWithRider(), [5, 7]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.cancelRider(8)
sol.addRider(12)
_l, _r = sol.matchDriverWithRider(), [2, 12]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.cancelRider(7)
_l, _r = sol.matchDriverWithRider(), [-1, -1]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.matchDriverWithRider(), [-1, -1]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.cancelRider(10)
sol.addRider(9)
sol.addDriver(11)
_l, _r = sol.matchDriverWithRider(), [10, 9]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol = RideSharingSystem()
sol.addRider(3)
sol.addDriver(4)
sol.addRider(8)
sol.addRider(10)
sol.addRider(7)
sol.addRider(11)
_l, _r = sol.matchDriverWithRider(), [4, 3]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.matchDriverWithRider(), [-1, -1]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.cancelRider(10)
sol.addRider(4)
_l, _r = sol.matchDriverWithRider(), [-1, -1]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.cancelRider(4)
sol.addRider(5)
sol.addRider(12)
sol.addDriver(5)
_l, _r = sol.matchDriverWithRider(), [5, 8]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.matchDriverWithRider(), [-1, -1]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.addDriver(8)
sol.addRider(6)
sol.addDriver(3)
sol.cancelRider(1)
sol.addRider(2)
sol.addDriver(7)
sol.addRider(9)
sol.cancelRider(6)
sol.addRider(1)
sol.cancelRider(5)
sol.addDriver(10)
sol.addDriver(1)
sol.addDriver(11)
sol = RideSharingSystem()
sol.addRider(12)
_l, _r = sol.matchDriverWithRider(), [-1, -1]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.addDriver(12)
sol.addRider(2)
sol.addRider(8)
_l, _r = sol.matchDriverWithRider(), [12, 12]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.addRider(9)
sol.cancelRider(1)
sol.addDriver(9)
sol.addRider(11)
sol.addRider(1)
_l, _r = sol.matchDriverWithRider(), [9, 2]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.addDriver(11)
_l, _r = sol.matchDriverWithRider(), [11, 8]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.matchDriverWithRider(), [-1, -1]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.addDriver(7)
sol.addRider(3)
sol.addRider(10)
sol.cancelRider(3)
_l, _r = sol.matchDriverWithRider(), [7, 9]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.addRider(5)
sol.addRider(7)
_l, _r = sol.matchDriverWithRider(), [-1, -1]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.addDriver(3)
sol.addDriver(8)
sol.addRider(4)
sol.addRider(6)
sol.addDriver(2)
sol.addDriver(10)
sol.addDriver(1)
sol = RideSharingSystem()
sol.addRider(2)
_l, _r = sol.matchDriverWithRider(), [-1, -1]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.matchDriverWithRider(), [-1, -1]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.addDriver(10)
sol.addRider(6)
sol.cancelRider(4)
_l, _r = sol.matchDriverWithRider(), [10, 2]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.addRider(12)
sol.cancelRider(10)
sol.cancelRider(2)
sol.addRider(7)
sol.addDriver(1)
sol.addRider(8)
sol.addDriver(4)
_l, _r = sol.matchDriverWithRider(), [1, 6]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.addRider(11)
sol.cancelRider(10)
sol.addDriver(8)
_l, _r = sol.matchDriverWithRider(), [4, 12]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.matchDriverWithRider(), [8, 7]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.addDriver(12)
_l, _r = sol.matchDriverWithRider(), [12, 8]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.cancelRider(10)
sol.cancelRider(1)
_l, _r = sol.matchDriverWithRider(), [-1, -1]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.matchDriverWithRider(), [-1, -1]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.matchDriverWithRider(), [-1, -1]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.cancelRider(2)
sol.addRider(9)
sol.addRider(4)
sol = RideSharingSystem()
sol.addDriver(9)
sol.addDriver(5)
sol.addRider(12)
_l, _r = sol.matchDriverWithRider(), [9, 12]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.addRider(2)
sol.addRider(10)
_l, _r = sol.matchDriverWithRider(), [5, 2]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.addDriver(8)
sol.cancelRider(8)
_l, _r = sol.matchDriverWithRider(), [8, 10]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.addDriver(6)
sol.addRider(6)
sol.addRider(9)
sol.cancelRider(5)
sol.cancelRider(1)
sol.addDriver(11)
sol.addRider(4)
sol.addDriver(4)
_l, _r = sol.matchDriverWithRider(), [6, 6]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.addDriver(3)
sol.cancelRider(8)
sol.addRider(8)
sol.addDriver(12)
_l, _r = sol.matchDriverWithRider(), [11, 9]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.matchDriverWithRider(), [4, 4]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.matchDriverWithRider(), [3, 8]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.addRider(11)
sol.addRider(1)
_l, _r = sol.matchDriverWithRider(), [12, 11]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.addDriver(1)
sol = RideSharingSystem()
_l, _r = sol.matchDriverWithRider(), [-1, -1]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.addDriver(12)
sol.cancelRider(8)
sol.addRider(4)
sol.addDriver(5)
sol.addRider(10)
sol.cancelRider(4)
_l, _r = sol.matchDriverWithRider(), [12, 10]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.matchDriverWithRider(), [-1, -1]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.cancelRider(6)
sol.addRider(8)
sol.cancelRider(6)
sol.addRider(3)
sol.addRider(5)
sol.cancelRider(3)
sol.addDriver(4)
sol.addRider(2)
sol.addDriver(7)
_l, _r = sol.matchDriverWithRider(), [5, 8]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.cancelRider(10)
sol.addRider(9)
_l, _r = sol.matchDriverWithRider(), [4, 5]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.matchDriverWithRider(), [7, 2]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.cancelRider(1)
sol.addRider(6)
_l, _r = sol.matchDriverWithRider(), [-1, -1]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.addDriver(8)
_l, _r = sol.matchDriverWithRider(), [8, 9]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.addDriver(1)
_l, _r = sol.matchDriverWithRider(), [1, 6]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol = RideSharingSystem()
sol.addRider(7)
sol.cancelRider(8)
_l, _r = sol.matchDriverWithRider(), [-1, -1]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.matchDriverWithRider(), [-1, -1]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.cancelRider(10)
sol.cancelRider(2)
sol.addDriver(9)
sol.addRider(3)
sol.cancelRider(2)
sol.addDriver(7)
_l, _r = sol.matchDriverWithRider(), [9, 7]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.addDriver(4)
sol.addRider(9)
_l, _r = sol.matchDriverWithRider(), [7, 3]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.cancelRider(10)
sol.addDriver(5)
_l, _r = sol.matchDriverWithRider(), [4, 9]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.cancelRider(4)
sol.addRider(1)
_l, _r = sol.matchDriverWithRider(), [5, 1]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.matchDriverWithRider(), [-1, -1]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.matchDriverWithRider(), [-1, -1]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.addRider(2)
sol.cancelRider(1)
_l, _r = sol.matchDriverWithRider(), [-1, -1]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.addDriver(1)
sol.cancelRider(10)
sol.addRider(5)
sol.addDriver(3)
sol.addDriver(6)
sol = RideSharingSystem()
sol.addRider(3)
_l, _r = sol.matchDriverWithRider(), [-1, -1]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.addDriver(9)
sol.cancelRider(12)
_l, _r = sol.matchDriverWithRider(), [9, 3]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.cancelRider(6)
_l, _r = sol.matchDriverWithRider(), [-1, -1]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.addRider(7)
sol.addRider(10)
sol.addRider(9)
_l, _r = sol.matchDriverWithRider(), [-1, -1]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.addRider(1)
sol.addRider(4)
sol.cancelRider(6)
sol.cancelRider(4)
_l, _r = sol.matchDriverWithRider(), [-1, -1]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.addDriver(2)
sol.addRider(6)
_l, _r = sol.matchDriverWithRider(), [2, 7]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.matchDriverWithRider(), [-1, -1]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.addRider(8)
_l, _r = sol.matchDriverWithRider(), [-1, -1]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.addDriver(12)
sol.cancelRider(8)
sol.cancelRider(5)
sol.cancelRider(3)
sol.addRider(5)
sol.addRider(11)
sol.addDriver(5)
_l, _r = sol.matchDriverWithRider(), [12, 10]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol = RideSharingSystem()
sol.addDriver(1)
_l, _r = sol.matchDriverWithRider(), [-1, -1]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.matchDriverWithRider(), [-1, -1]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.addDriver(2)
sol.addRider(7)
sol.addDriver(7)
sol.cancelRider(12)
sol.addDriver(6)
sol.cancelRider(2)
sol.addRider(12)
sol.addRider(1)
_l, _r = sol.matchDriverWithRider(), [1, 7]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.addRider(10)
sol.addRider(4)
sol.addRider(6)
sol.addDriver(3)
sol.cancelRider(2)
_l, _r = sol.matchDriverWithRider(), [2, 12]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.addDriver(11)
sol.addDriver(9)
sol.cancelRider(7)
sol.addRider(2)
_l, _r = sol.matchDriverWithRider(), [7, 1]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.addRider(8)
_l, _r = sol.matchDriverWithRider(), [6, 10]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.addRider(9)
sol.addRider(3)
sol.addRider(5)
sol.addRider(11)
sol.addDriver(8)
sol = RideSharingSystem()
sol.cancelRider(1)
sol.cancelRider(10)
sol.cancelRider(9)
sol.addRider(11)
sol.addRider(5)
sol.addRider(10)
sol.addRider(12)
_l, _r = sol.matchDriverWithRider(), [-1, -1]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.matchDriverWithRider(), [-1, -1]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.addDriver(4)
sol.addRider(6)
sol.addRider(3)
sol.cancelRider(4)
_l, _r = sol.matchDriverWithRider(), [4, 11]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.addDriver(5)
_l, _r = sol.matchDriverWithRider(), [5, 5]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.addDriver(2)
_l, _r = sol.matchDriverWithRider(), [2, 10]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.cancelRider(11)
sol.addDriver(1)
_l, _r = sol.matchDriverWithRider(), [1, 12]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.addRider(4)
sol.addDriver(3)
sol.cancelRider(7)
_l, _r = sol.matchDriverWithRider(), [3, 6]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.addRider(2)
sol.addRider(8)
sol.addDriver(10)
sol.addRider(9)
sol.addDriver(12)
sol = RideSharingSystem()
_l, _r = sol.matchDriverWithRider(), [-1, -1]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.cancelRider(12)
sol.addDriver(9)
sol.addDriver(3)
sol.addRider(4)
sol.addDriver(7)
_l, _r = sol.matchDriverWithRider(), [9, 4]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.matchDriverWithRider(), [-1, -1]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.addDriver(10)
sol.addDriver(1)
sol.cancelRider(6)
sol.addRider(12)
sol.cancelRider(7)
sol.addDriver(8)
sol.cancelRider(11)
sol.addRider(5)
sol.addRider(11)
_l, _r = sol.matchDriverWithRider(), [3, 12]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.addDriver(5)
sol.addRider(8)
_l, _r = sol.matchDriverWithRider(), [7, 5]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.cancelRider(7)
_l, _r = sol.matchDriverWithRider(), [10, 11]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.matchDriverWithRider(), [1, 8]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.matchDriverWithRider(), [-1, -1]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.cancelRider(3)
_l, _r = sol.matchDriverWithRider(), [-1, -1]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.addRider(10)
_l, _r = sol.matchDriverWithRider(), [8, 10]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.addDriver(12)
sol = RideSharingSystem()
sol.addRider(5)
sol.cancelRider(8)
sol.cancelRider(5)
_l, _r = sol.matchDriverWithRider(), [-1, -1]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.addDriver(1)
sol.cancelRider(6)
sol.addRider(11)
sol.addRider(7)
sol.addDriver(12)
sol.cancelRider(4)
sol.addDriver(6)
_l, _r = sol.matchDriverWithRider(), [1, 11]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.cancelRider(8)
sol.addRider(6)
_l, _r = sol.matchDriverWithRider(), [12, 7]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.addRider(10)
sol.addRider(12)
sol.addDriver(9)
_l, _r = sol.matchDriverWithRider(), [6, 6]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.matchDriverWithRider(), [9, 10]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.cancelRider(12)
sol.cancelRider(4)
_l, _r = sol.matchDriverWithRider(), [-1, -1]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.matchDriverWithRider(), [-1, -1]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
sol.addRider(8)
sol.cancelRider(3)
sol.cancelRider(5)
sol.addDriver(3)
sol.addRider(1)
sol.addDriver(5)
