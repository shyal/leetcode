"""
735. Asteroid Collision
Medium
We are given an array asteroids of integers representing asteroids in a row. The indices of the asteriod in the array represent their relative position in space.

For each asteroid, the absolute value represents its size, and the sign represents its direction (positive meaning right, negative meaning left). Each asteroid moves at the same speed.

Find out the state of the asteroids after all collisions. If two asteroids meet, the smaller one will explode. If both are the same size, both will explode. Two asteroids moving in the same direction will never meet.

Example 1:

Input: asteroids = [5,10,-5]
Output: [5,10]
Explanation: The 10 and -5 collide resulting in 10. The 5 and 10 never collide.
Example 2:

Input: asteroids = [8,-8]
Output: []
Explanation: The 8 and -8 collide exploding each other.
Example 3:

Input: asteroids = [10,2,-5]
Output: [10]
Explanation: The 2 and -5 collide resulting in -5. The 10 and -5 collide resulting in 10.
 

Constraints:

2 <= asteroids.length <= 104
-1000 <= asteroids[i] <= 1000
asteroids[i] != 0
"""


class Solution:
    def asteroidCollision(self, asteroids: List[int]) -> List[int]:
        while True:
            stack = []
            smash = False
            for ast in asteroids:
                if not stack:
                    stack.append(ast)
                    continue
                else:
                    prev = stack[-1]
                    prev_dir = prev >= 0
                    ast_dir = ast >= 0
                    on_collision_course = prev_dir == 1 and ast_dir == 0
                    prev_smash = on_collision_course and abs(prev) <= abs(ast)
                    ast_smash = on_collision_course and abs(prev) >= abs(ast)
                    if prev_smash and stack:
                        stack.pop()
                        smash = True
                    if not ast_smash:
                        stack.append(ast)
            if not smash:
                break
            asteroids = stack[:]
        return stack


sol = Solution()
assert sol.asteroidCollision(asteroids=[5, 10, -5]) == [5, 10]
assert sol.asteroidCollision(asteroids=[8, -8]) == []
assert sol.asteroidCollision([10, 2, -5]) == [10]
assert sol.asteroidCollision([-2, -1, 1, -2]) == [-2, -1, -2]
assert sol.asteroidCollision([1, -1]) == []
assert sol.asteroidCollision([-1, 1]) == [-1, 1]
assert sol.asteroidCollision([5, 5, -5]) == [5]
assert sol.asteroidCollision([1, 2, 3]) == [1, 2, 3]
assert sol.asteroidCollision([-1, -2, -3]) == [-1, -2, -3]
assert sol.asteroidCollision([4, -2, -3]) == [4]
assert sol.asteroidCollision([3, -2, -3]) == []
assert sol.asteroidCollision([1, -2, 3]) == [-2, 3]
assert sol.asteroidCollision([-5, 10]) == [-5, 10]
