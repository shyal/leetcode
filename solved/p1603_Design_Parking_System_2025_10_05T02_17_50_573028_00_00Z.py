"""
URL: https://leetcode.com/problems/design-parking-system/description/?envType=study-plan-v2&envId=leetcode-75

1603. Design Parking System

Design a parking system for a parking lot. The parking lot has three kinds of parking spaces: big, medium, and small, with a fixed number of slots for each size.

Implement the ParkingSystem class:

    ParkingSystem(int big, int medium, int small) Initializes object of the ParkingSystem class. The number of slots for each parking space are given as part of the constructor.
    bool addCar(int carType) Checks whether there is a parking space of carType for the car that wants to get into the parking lot. carType can be of three kinds: big, medium, or small, which are represented by 1, 2, and 3 respectively. A car can only park in a parking space of its carType. If there is no space available, return false, else park the car in that size space and return true.

Example 1:

Input
["ParkingSystem", "addCar", "addCar", "addCar", "addCar"]
[[1, 1, 0], [1], [2], [3], [1]]
Output
[null, true, true, false, false]

Explanation
ParkingSystem parkingSystem = new ParkingSystem(1, 1, 0);
parkingSystem.addCar(1); // return true because there is 1 available slot for a big car
parkingSystem.addCar(2); // return true because there is 1 available slot for a medium car
parkingSystem.addCar(3); // return false because there is no available slot for a small car
parkingSystem.addCar(1); // return false because there is no available slot for a big car. It is already occupied.

Constraints:

    0 <= big, medium, small <= 1000
    carType is 1, 2, or 3
    At most 1000 calls will be made to addCar
"""


class CarSize:

    big = 1
    medium = 2
    small = 3


class ParkingSystem:
    def __init__(self, big: int, medium: int, small: int):
        self.spaces = {CarSize.big: big, CarSize.medium: medium, CarSize.small: small}

    def addCar(self, carType: int) -> bool:
        if self.spaces[carType] > 0:
            self.spaces[carType] -= 1
            return True
        else:
            return False


sol = ParkingSystem(1, 1, 0)

sol = ParkingSystem(1, 1, 0)
assert sol.addCar(1) == True
assert sol.addCar(2) == True
assert sol.addCar(3) == False
assert sol.addCar(1) == False

sol = ParkingSystem(0, 0, 0)
assert sol.addCar(1) == False
assert sol.addCar(2) == False
assert sol.addCar(3) == False
assert sol.addCar(1) == False
assert sol.addCar(2) == False
assert sol.addCar(3) == False

sol = ParkingSystem(2, 0, 0)
assert sol.addCar(1) == True
assert sol.addCar(1) == True
assert sol.addCar(1) == False
assert sol.addCar(2) == False
assert sol.addCar(3) == False

sol = ParkingSystem(0, 3, 0)
assert sol.addCar(2) == True
assert sol.addCar(2) == True
assert sol.addCar(2) == True
assert sol.addCar(2) == False
assert sol.addCar(1) == False
assert sol.addCar(3) == False

sol = ParkingSystem(0, 0, 1)
assert sol.addCar(3) == True
assert sol.addCar(3) == False
assert sol.addCar(1) == False
assert sol.addCar(2) == False

sol = ParkingSystem(1, 2, 3)
assert sol.addCar(3) == True
assert sol.addCar(2) == True
assert sol.addCar(1) == True
assert sol.addCar(3) == True
assert sol.addCar(3) == True
assert sol.addCar(2) == True
assert sol.addCar(1) == False  # Big exhausted
assert sol.addCar(2) == False  # Medium exhausted
assert sol.addCar(3) == False  # Small exhausted

sol = ParkingSystem(1000, 1000, 1000)
assert sol.addCar(1) == True
assert sol.addCar(2) == True
assert sol.addCar(3) == True
for _ in range(999):
    assert sol.addCar(1) == True
assert sol.addCar(1) == False  # Big exhausted after 1000 adds
assert sol.addCar(2) == True  # Medium still available
assert sol.addCar(3) == True  # Small still available

sol = ParkingSystem(0, 0, 2)
assert sol.addCar(3) == True
assert sol.addCar(1) == False
assert sol.addCar(2) == False
assert sol.addCar(3) == True
assert sol.addCar(3) == False

sol = ParkingSystem(1, 1, 1)
assert sol.addCar(2) == True  # Fill medium first
assert sol.addCar(2) == False
assert sol.addCar(1) == True  # Big still available
assert sol.addCar(3) == True  # Small still available
assert sol.addCar(1) == False
assert sol.addCar(3) == False

sol = ParkingSystem(1, 0, 1)
assert sol.addCar(1) == True
assert sol.addCar(3) == True
assert sol.addCar(2) == False
assert sol.addCar(1) == False
assert sol.addCar(3) == False
