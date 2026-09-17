"""
URL: https://leetcode.com/problems/maximum-average-pass-ratio/description/?envType=problem-list-v2&envId=vn57k9wr

1792. Maximum Average Pass Ratio

There is a school that has classes of students and each class will be having a final exam. You are given a 2D integer array classes, where classes[i] = [pass_i, total_i]. You know beforehand that in the i-th class, there are total_i total students, but only pass_i number of students will pass the exam.

You are also given an integer extraStudents. There are another extraStudents brilliant students that are guaranteed to pass the exam of any class they are assigned to. You want to assign each of the extraStudents students to a class in a way that maximizes the average pass ratio across all the classes.

The pass ratio of a class is equal to the number of students of the class that will pass the exam divided by the total number of students of the class. The average pass ratio is the sum of pass ratios of all the classes divided by the number of the classes.

Return the maximum possible average pass ratio after assigning the extraStudents students. Answers within 10^-5 of the actual answer will be accepted.

Example 1:

Input: classes = [[1,2],[3,5],[2,2]], extraStudents = 2
Output: 0.78333
Explanation: You can assign the two extra students to the first class. The average pass ratio will be equal to (3/4 + 3/5 + 2/2) / 3 = 0.78333.

Example 2:

Input: classes = [[2,4],[3,9],[4,5],[2,10]], extraStudents = 4
Output: 0.53485

Constraints:

    1 <= classes.length <= 10^5
    classes[i].length == 2
    1 <= pass_i <= total_i <= 10^5
    1 <= extraStudents <= 10^5

---

Sounds like this cold be greedy. Simply compute the pass ratio for all classes,
then add the extraStudents to the classes with the weakest pass ratio?

[[1,2],[3,5],[2,2]]

0.5, 0.6, 1

so we add the two students:

[[3,4],[3,5],[2,2]]

0.75, 0.6, 1

(3/4 + 3/5 + 2/2) / 3

But why does it even matter?

What if it were:

(2/3 + 4/6 + 3/4) / 3

Hmm

The delta between 1/2 and 3/4 is 0.25

Dunno........

Ok the leetcode hints kind of give it away.

Put the ratios in a max heap, then keep adding students to it.

Learning.

LEETCODE: Accepted (2480 ms, 59.3 MB)
"""


class Solution:
    def maxAverageRatio(self, classes: List[List[int]], extraStudents: int) -> float:
        def gain(p, t):
            return (p + 1) / (t + 1) - (p / t)

        heap = [(gain(p, t), p, t) for p, t in classes]
        maxheapify(heap)

        for _ in range(extraStudents):
            _, p, t = maxheappop(heap)
            p, t = p + 1, t + 1
            maxheappush(heap, (gain(p, t), p, t))

        return sum(p / t for _, p, t in maxheapitems(heap)) / len(classes)


sol = Solution()

print(sol.maxAverageRatio([[1, 2], [3, 5], [2, 2]], 2))  # 0.78333

assert abs(sol.maxAverageRatio([[1, 2], [3, 5], [2, 2]], 2) - 0.78333) < 1e-5
assert abs(sol.maxAverageRatio([[2, 4], [3, 9], [4, 5], [2, 10]], 4) - 0.53485) < 1e-5

assert sol.maxAverageRatio([[1, 1]], 0) == 1.0
assert sol.maxAverageRatio([[0, 1]], 1) == 0.5
assert sol.maxAverageRatio([[0, 1]], 10) == 0.9090909090909091
assert sol.maxAverageRatio([[1, 100000]], 100000) == 0.500005
assert sol.maxAverageRatio([[50000, 100000]], 50000) == 0.6666666666666666
assert sol.maxAverageRatio([[1, 2], [1, 2], [1, 2], [1, 2]], 4) == 0.6666666666666666
assert sol.maxAverageRatio([[0, 1], [0, 1], [0, 1]], 3) == 0.5
assert sol.maxAverageRatio([[99999, 100000]], 1) == 0.999990000099999
assert sol.maxAverageRatio([[1, 1], [1, 1], [1, 1], [1, 1]], 0) == 1.0
assert sol.maxAverageRatio([[0, 100000], [0, 100000]], 100000) == 0.3333333333333333
assert (
    abs(sol.maxAverageRatio([[1, 2], [2, 3], [3, 4], [4, 5], [5, 6]], 5) - 0.79666667)
    < 1e-8
)
assert sol.maxAverageRatio([[1, 100000]] * 100000, 100000) == 1.9999800001946303e-05
