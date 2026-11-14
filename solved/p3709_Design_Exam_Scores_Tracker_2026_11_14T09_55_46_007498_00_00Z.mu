# URL: https://leetcode.com/problems/design-exam-scores-tracker/description/?envType=problem-list-v2&envId=vn57k9wr
#
# 3709. Design Exam Scores Tracker
#
# Alice frequently takes exams and wants to track her scores and calculate the total scores over specific time periods.
#
# Implement the ExamTracker class:
#
# - ExamTracker(): Initializes the ExamTracker object.
# - void record(int time, int score): Alice takes a new exam at time time and achieves the score score.
# - long long totalScore(int startTime, int endTime): Returns an integer that represents the total score of all exams taken by Alice between startTime and endTime (inclusive). If there are no recorded exams taken by Alice within the specified time interval, return 0.
#
# It is guaranteed that the function calls are made in chronological order. That is,
# - Calls to record() will be made with strictly increasing time.
# - Alice will never ask for total scores that require information from the future. That is, if the latest record() is called with time = t, then totalScore() will always be called with startTime <= endTime <= t.
#
# Example 1:
#
# Input:
# ["ExamTracker","record","totalScore","record","totalScore","totalScore","totalScore","totalScore"]
# [[],[1,98],[1,1],[5,99],[1,3],[1,5],[3,4],[2,5]]
#
# Output:
# [null,null,98,null,98,197,0,99]
#
# Explanation:
# ExamTracker examTracker = new ExamTracker();
# examTracker.record(1, 98); // Alice takes a new exam at time 1, scoring 98.
# examTracker.totalScore(1, 1); // Between time 1 and time 1, Alice took 1 exam at time 1, scoring 98. The total score is 98.
# examTracker.record(5, 99); // Alice takes a new exam at time 5, scoring 99.
# examTracker.totalScore(1, 3); // Between time 1 and time 3, Alice took 1 exam at time 1, scoring 98. The total score is 98.
# examTracker.totalScore(1, 5); // Between time 1 and time 5, Alice took 2 exams at time 1 and 5, scoring 98 and 99. The total score is 98 + 99 = 197.
# examTracker.totalScore(3, 4); // Alice did not take any exam between time 3 and time 4. Therefore, the answer is 0.
# examTracker.totalScore(2, 5); // Between time 2 and time 5, Alice took 1 exam at time 5, scoring 99. The total score is 99.
#
# Constraints:
#
# - 1 <= time <= 10^9
# - 1 <= score <= 10^9
# - 1 <= startTime <= endTime <= t, where t is the value of time from the most recent call of record().
# - Calls of record() will be made with strictly increasing time.
# - After ExamTracker(), the first function call will always be record().
# - At most 10^5 calls will be made in total to record() and totalScore().
#
# ---
# STAGE 1 of 3 - the approach. Write it in plain English under this line. Then run make solved.
#
# learning.. i read the hints in leetcode, then i got hinted to use bisect_right for hi.

# mu 0.18

class ExamTracker
  def __init__()
    self.prefix = []
    self.times = []

  def record(time: int, score: int) -> none
    self.times <- time
    self.prefix <- self.prefix ? self.prefix[-1] + score : score

  def totalScore(startTime: int, endTime: int) -> int
    lo = bisect_left(self.times, startTime)
    hi = bisect_right(self.times, endTime)
    rhi = (hi > 0 ? self.prefix[hi - 1] : 0)
    rlo = (lo > 0 ? self.prefix[lo - 1] : 0)
    rhi - rlo

sol = ExamTracker()

sol.record(1, 98)
print(sol.totalScore(1, 1))  # 98

# sol.record(5, 99)
# assert sol.totalScore(1, 3) == 98
# assert sol.totalScore(1, 5) == 197
# assert sol.totalScore(3, 4) == 0
# assert sol.totalScore(2, 5) == 99

# sequence asserts for the data-sync chain: misc/data_sync_asserts.py

# the values are the reference solution's; a read the statement leaves
# open is asserted over every answer it allows

sol = ExamTracker()  # one record, asked for its own time
sol.record(1, 98)
assert sol.totalScore(1, 1) == 98

sol = ExamTracker()  # a range before the first record
sol.record(5, 10)
sol.record(8, 20)
assert sol.totalScore(5, 5) == 10
assert sol.totalScore(6, 7) == 0
assert sol.totalScore(6, 8) == 20
assert sol.totalScore(1, 4) == 0

sol = ExamTracker()  # ranges ending exactly on a record
sol.record(2, 1)
sol.record(4, 2)
sol.record(6, 3)
assert sol.totalScore(2, 4) == 3
assert sol.totalScore(3, 4) == 2
assert sol.totalScore(4, 6) == 5
assert sol.totalScore(1, 6) == 6
assert sol.totalScore(5, 6) == 3

sol = ExamTracker()  # a range between two records
sol.record(10, 5)
sol.record(20, 6)
assert sol.totalScore(11, 19) == 0
assert sol.totalScore(10, 19) == 5
assert sol.totalScore(11, 20) == 6
assert sol.totalScore(10, 20) == 11

sol = ExamTracker()  # reads between records
sol.record(1, 1)
assert sol.totalScore(1, 1) == 1
sol.record(3, 2)
assert sol.totalScore(1, 3) == 3
assert sol.totalScore(2, 3) == 2
sol.record(4, 4)
assert sol.totalScore(1, 4) == 7
assert sol.totalScore(4, 4) == 4
assert sol.totalScore(2, 2) == 0

sol = ExamTracker()  # the largest scores
sol.record(1, 1000000000)
sol.record(2, 1000000000)
sol.record(3, 1000000000)
assert sol.totalScore(1, 3) == 3000000000
assert sol.totalScore(2, 2) == 1000000000

sol = ExamTracker()  # the largest times
sol.record(999999999, 5)
sol.record(1000000000, 7)
assert sol.totalScore(1, 1000000000) == 12
assert sol.totalScore(1000000000, 1000000000) == 7
assert sol.totalScore(1, 999999999) == 5

sol = ExamTracker()  # records far apart, a range covering only the last
sol.record(1, 1)
sol.record(100, 2)
sol.record(10000, 3)
assert sol.totalScore(101, 10000) == 3
assert sol.totalScore(2, 9999) == 2
assert sol.totalScore(1, 100) == 3

sol = ExamTracker()  # random sequence 1
sol.record(1, 6)
assert sol.totalScore(1, 1) == 6
assert sol.totalScore(1, 1) == 6
sol.record(4, 1)
sol.record(7, 2)
assert sol.totalScore(3, 3) == 0
assert sol.totalScore(4, 5) == 1
assert sol.totalScore(3, 3) == 0
assert sol.totalScore(4, 4) == 1
assert sol.totalScore(7, 7) == 2
assert sol.totalScore(6, 7) == 2
sol.record(8, 4)
assert sol.totalScore(4, 6) == 1
sol.record(11, 6)
sol.record(12, 9)
sol.record(14, 9)
sol.record(17, 8)
assert sol.totalScore(3, 4) == 1
assert sol.totalScore(13, 15) == 9
assert sol.totalScore(2, 14) == 31
assert sol.totalScore(12, 13) == 9
sol.record(20, 4)
sol.record(23, 2)
assert sol.totalScore(19, 21) == 4
assert sol.totalScore(16, 22) == 12
sol.record(24, 3)
sol.record(25, 2)
sol.record(28, 8)
sol.record(30, 1)
assert sol.totalScore(8, 15) == 28

sol = ExamTracker()  # random sequence 2
sol.record(3, 4)
assert sol.totalScore(2, 2) == 0
sol.record(4, 8)
sol.record(6, 4)
assert sol.totalScore(4, 4) == 8
sol.record(7, 9)
assert sol.totalScore(5, 5) == 0
assert sol.totalScore(4, 6) == 12
assert sol.totalScore(7, 7) == 9
assert sol.totalScore(3, 6) == 16
assert sol.totalScore(1, 1) == 0
assert sol.totalScore(1, 2) == 0
assert sol.totalScore(5, 6) == 4
assert sol.totalScore(5, 5) == 0
sol.record(8, 2)
sol.record(11, 2)
sol.record(13, 3)
assert sol.totalScore(7, 9) == 11
sol.record(15, 2)
sol.record(17, 1)
sol.record(20, 8)
assert sol.totalScore(17, 19) == 1
assert sol.totalScore(1, 12) == 29
assert sol.totalScore(16, 20) == 9
assert sol.totalScore(5, 13) == 20
assert sol.totalScore(12, 14) == 3
sol.record(21, 8)
assert sol.totalScore(12, 14) == 3
sol.record(22, 3)
assert sol.totalScore(21, 21) == 8

sol = ExamTracker()  # random sequence 3
sol.record(1, 9)
assert sol.totalScore(1, 1) == 9
assert sol.totalScore(1, 1) == 9
sol.record(4, 7)
sol.record(6, 3)
assert sol.totalScore(5, 6) == 3
assert sol.totalScore(5, 6) == 3
sol.record(8, 6)
sol.record(10, 3)
sol.record(11, 3)
assert sol.totalScore(7, 9) == 6
sol.record(12, 6)
sol.record(13, 4)
sol.record(14, 2)
assert sol.totalScore(8, 13) == 22
sol.record(15, 5)
sol.record(17, 4)
assert sol.totalScore(4, 6) == 10
assert sol.totalScore(10, 13) == 16
sol.record(19, 1)
sol.record(22, 9)
assert sol.totalScore(19, 20) == 1
sol.record(25, 2)
sol.record(27, 2)
sol.record(29, 4)
sol.record(32, 2)
sol.record(33, 8)
sol.record(34, 3)
assert sol.totalScore(33, 34) == 11
assert sol.totalScore(13, 34) == 46

sol = ExamTracker()  # random sequence 4
sol.record(2, 1)
assert sol.totalScore(2, 2) == 1
assert sol.totalScore(2, 2) == 1
assert sol.totalScore(1, 2) == 1
sol.record(4, 3)
sol.record(5, 4)
assert sol.totalScore(1, 5) == 8
assert sol.totalScore(1, 1) == 0
assert sol.totalScore(3, 5) == 7
sol.record(7, 8)
assert sol.totalScore(2, 6) == 8
assert sol.totalScore(2, 4) == 4
assert sol.totalScore(5, 5) == 4
assert sol.totalScore(3, 5) == 7
sol.record(9, 5)
assert sol.totalScore(8, 9) == 5
assert sol.totalScore(3, 4) == 3
assert sol.totalScore(8, 8) == 0
sol.record(12, 9)
sol.record(13, 5)
assert sol.totalScore(1, 10) == 21
sol.record(15, 9)
sol.record(17, 8)
assert sol.totalScore(7, 12) == 22
assert sol.totalScore(11, 15) == 23
assert sol.totalScore(12, 14) == 14
assert sol.totalScore(15, 16) == 9
sol.record(20, 7)
assert sol.totalScore(8, 8) == 0
assert sol.totalScore(17, 20) == 15

sol = ExamTracker()  # random sequence 5
sol.record(3, 5)
sol.record(6, 1)
assert sol.totalScore(3, 4) == 5
assert sol.totalScore(1, 1) == 0
assert sol.totalScore(6, 6) == 1
assert sol.totalScore(5, 5) == 0
sol.record(9, 1)
assert sol.totalScore(7, 7) == 0
sol.record(12, 3)
assert sol.totalScore(3, 6) == 6
sol.record(15, 6)
assert sol.totalScore(3, 11) == 7
sol.record(16, 4)
sol.record(17, 4)
assert sol.totalScore(4, 17) == 19
assert sol.totalScore(16, 16) == 4
sol.record(18, 8)
assert sol.totalScore(18, 18) == 8
assert sol.totalScore(4, 15) == 11
assert sol.totalScore(9, 15) == 10
assert sol.totalScore(18, 18) == 8
sol.record(20, 4)
assert sol.totalScore(1, 1) == 0
assert sol.totalScore(6, 6) == 1
assert sol.totalScore(9, 16) == 14
assert sol.totalScore(9, 11) == 1
sol.record(22, 4)
assert sol.totalScore(3, 9) == 7
assert sol.totalScore(13, 22) == 30
sol.record(25, 3)

sol = ExamTracker()  # random sequence 6
sol.record(1, 5)
assert sol.totalScore(1, 1) == 5
sol.record(4, 6)
sol.record(5, 8)
assert sol.totalScore(5, 5) == 8
sol.record(8, 4)
sol.record(11, 2)
assert sol.totalScore(11, 11) == 2
assert sol.totalScore(2, 10) == 18
assert sol.totalScore(6, 6) == 0
assert sol.totalScore(1, 9) == 23
sol.record(12, 8)
sol.record(13, 8)
assert sol.totalScore(12, 13) == 16
assert sol.totalScore(2, 11) == 20
sol.record(16, 5)
sol.record(18, 8)
sol.record(21, 2)
assert sol.totalScore(19, 20) == 0
sol.record(23, 3)
sol.record(26, 3)
assert sol.totalScore(16, 19) == 13
sol.record(29, 7)
assert sol.totalScore(16, 19) == 13
assert sol.totalScore(4, 6) == 14
assert sol.totalScore(17, 19) == 8
assert sol.totalScore(10, 12) == 10
assert sol.totalScore(28, 29) == 7
assert sol.totalScore(4, 11) == 20
sol.record(31, 2)

sol = ExamTracker()  # random sequence 7
sol.record(3, 8)
sol.record(4, 8)
sol.record(5, 3)
sol.record(7, 8)
sol.record(9, 9)
sol.record(12, 7)
assert sol.totalScore(8, 12) == 16
sol.record(15, 9)
sol.record(16, 1)
assert sol.totalScore(6, 15) == 33
assert sol.totalScore(16, 16) == 1
assert sol.totalScore(8, 10) == 9
sol.record(18, 1)
sol.record(20, 2)
assert sol.totalScore(15, 16) == 10
assert sol.totalScore(7, 14) == 24
sol.record(22, 2)
assert sol.totalScore(11, 22) == 22
assert sol.totalScore(5, 19) == 38
sol.record(23, 6)
assert sol.totalScore(17, 22) == 5
assert sol.totalScore(11, 16) == 17
sol.record(26, 2)
assert sol.totalScore(13, 23) == 21
assert sol.totalScore(13, 14) == 0
sol.record(29, 9)
sol.record(32, 2)
sol.record(34, 1)
assert sol.totalScore(1, 22) == 58
assert sol.totalScore(4, 23) == 56

sol = ExamTracker()  # random sequence 8
sol.record(1, 5)
assert sol.totalScore(1, 1) == 5
sol.record(3, 3)
assert sol.totalScore(1, 3) == 8
assert sol.totalScore(1, 3) == 8
assert sol.totalScore(1, 1) == 5
sol.record(4, 6)
sol.record(7, 6)
sol.record(9, 5)
assert sol.totalScore(4, 6) == 6
sol.record(11, 4)
assert sol.totalScore(5, 8) == 6
sol.record(13, 3)
assert sol.totalScore(12, 12) == 0
sol.record(15, 5)
assert sol.totalScore(15, 15) == 5
sol.record(17, 9)
assert sol.totalScore(11, 13) == 7
sol.record(19, 8)
assert sol.totalScore(7, 15) == 23
sol.record(21, 6)
assert sol.totalScore(13, 13) == 3
assert sol.totalScore(2, 12) == 24
assert sol.totalScore(12, 12) == 0
sol.record(24, 8)
assert sol.totalScore(18, 21) == 14
assert sol.totalScore(18, 24) == 22
sol.record(26, 8)
assert sol.totalScore(21, 24) == 14
assert sol.totalScore(9, 18) == 26

sol = ExamTracker()  # random sequence 9
sol.record(2, 4)
assert sol.totalScore(1, 2) == 4
sol.record(5, 5)
assert sol.totalScore(2, 5) == 9
assert sol.totalScore(1, 3) == 4
sol.record(7, 6)
assert sol.totalScore(5, 6) == 5
sol.record(9, 4)
assert sol.totalScore(8, 8) == 0
assert sol.totalScore(6, 6) == 0
sol.record(12, 6)
assert sol.totalScore(5, 12) == 21
assert sol.totalScore(3, 11) == 15
assert sol.totalScore(11, 12) == 6
sol.record(15, 1)
sol.record(16, 9)
assert sol.totalScore(16, 16) == 9
assert sol.totalScore(10, 16) == 16
assert sol.totalScore(3, 14) == 21
assert sol.totalScore(13, 13) == 0
assert sol.totalScore(7, 7) == 6
sol.record(18, 1)
assert sol.totalScore(15, 15) == 1
sol.record(19, 4)
assert sol.totalScore(4, 18) == 32
assert sol.totalScore(4, 19) == 36
sol.record(20, 9)
assert sol.totalScore(12, 13) == 6
sol.record(23, 4)
sol.record(24, 1)

sol = ExamTracker()  # random sequence 10
sol.record(2, 7)
assert sol.totalScore(1, 2) == 7
assert sol.totalScore(2, 2) == 7
assert sol.totalScore(1, 2) == 7
assert sol.totalScore(2, 2) == 7
assert sol.totalScore(2, 2) == 7
sol.record(4, 9)
sol.record(5, 5)
assert sol.totalScore(4, 4) == 9
sol.record(7, 3)
sol.record(10, 8)
sol.record(11, 5)
assert sol.totalScore(10, 10) == 8
assert sol.totalScore(9, 11) == 13
assert sol.totalScore(5, 8) == 8
sol.record(14, 2)
sol.record(15, 9)
sol.record(17, 9)
assert sol.totalScore(7, 16) == 27
sol.record(20, 3)
assert sol.totalScore(20, 20) == 3
assert sol.totalScore(2, 3) == 7
assert sol.totalScore(12, 19) == 20
sol.record(23, 8)
assert sol.totalScore(22, 22) == 0
sol.record(26, 4)
assert sol.totalScore(17, 26) == 24
assert sol.totalScore(15, 22) == 21
sol.record(28, 4)
assert sol.totalScore(10, 15) == 24

sol = ExamTracker()  # random sequence 11
sol.record(1, 1)
sol.record(4, 2)
sol.record(6, 6)
assert sol.totalScore(3, 4) == 2
assert sol.totalScore(5, 6) == 6
assert sol.totalScore(6, 6) == 6
assert sol.totalScore(4, 5) == 2
sol.record(7, 6)
sol.record(8, 9)
sol.record(9, 7)
sol.record(11, 1)
sol.record(14, 9)
sol.record(15, 3)
sol.record(18, 6)
sol.record(20, 7)
sol.record(21, 9)
sol.record(23, 4)
sol.record(25, 7)
sol.record(28, 3)
sol.record(30, 5)
assert sol.totalScore(1, 18) == 50
assert sol.totalScore(18, 22) == 22
sol.record(31, 8)
assert sol.totalScore(17, 26) == 33
assert sol.totalScore(11, 11) == 1
assert sol.totalScore(27, 30) == 8
assert sol.totalScore(9, 26) == 53
sol.record(34, 2)
sol.record(36, 1)
assert sol.totalScore(9, 21) == 42

sol = ExamTracker()  # random sequence 12
sol.record(1, 3)
assert sol.totalScore(1, 1) == 3
sol.record(4, 7)
assert sol.totalScore(4, 4) == 7
assert sol.totalScore(2, 2) == 0
assert sol.totalScore(4, 4) == 7
assert sol.totalScore(3, 3) == 0
sol.record(6, 7)
assert sol.totalScore(5, 6) == 7
sol.record(9, 1)
sol.record(12, 4)
sol.record(15, 1)
sol.record(16, 1)
sol.record(19, 7)
sol.record(20, 3)
assert sol.totalScore(10, 10) == 0
assert sol.totalScore(19, 19) == 7
sol.record(22, 6)
assert sol.totalScore(7, 16) == 7
sol.record(23, 1)
assert sol.totalScore(18, 20) == 10
sol.record(25, 5)
sol.record(27, 5)
assert sol.totalScore(5, 27) == 41
assert sol.totalScore(26, 27) == 5
assert sol.totalScore(10, 26) == 28
assert sol.totalScore(11, 18) == 6
assert sol.totalScore(13, 25) == 24
assert sol.totalScore(22, 26) == 12
assert sol.totalScore(16, 25) == 23

sol = ExamTracker()  # random sequence 13
sol.record(1, 6)
sol.record(4, 2)
assert sol.totalScore(1, 4) == 8
assert sol.totalScore(1, 4) == 8
assert sol.totalScore(3, 4) == 2
sol.record(5, 1)
assert sol.totalScore(2, 2) == 0
assert sol.totalScore(5, 5) == 1
sol.record(8, 2)
assert sol.totalScore(2, 5) == 3
assert sol.totalScore(7, 7) == 0
sol.record(9, 6)
assert sol.totalScore(3, 4) == 2
sol.record(12, 5)
sol.record(15, 1)
assert sol.totalScore(11, 11) == 0
sol.record(16, 9)
assert sol.totalScore(2, 10) == 11
assert sol.totalScore(7, 14) == 13
sol.record(18, 6)
sol.record(20, 4)
assert sol.totalScore(18, 19) == 6
sol.record(22, 2)
sol.record(25, 7)
assert sol.totalScore(18, 20) == 10
sol.record(28, 6)
sol.record(31, 5)
sol.record(34, 8)
assert sol.totalScore(24, 26) == 7
sol.record(36, 6)

sol = ExamTracker()  # random sequence 14
sol.record(1, 7)
sol.record(3, 5)
assert sol.totalScore(2, 2) == 0
sol.record(4, 1)
assert sol.totalScore(4, 4) == 1
sol.record(7, 2)
assert sol.totalScore(7, 7) == 2
sol.record(9, 7)
assert sol.totalScore(9, 9) == 7
sol.record(10, 3)
assert sol.totalScore(7, 9) == 9
assert sol.totalScore(4, 9) == 10
assert sol.totalScore(4, 4) == 1
sol.record(12, 9)
assert sol.totalScore(6, 9) == 9
sol.record(14, 1)
assert sol.totalScore(11, 12) == 9
sol.record(16, 6)
sol.record(19, 5)
sol.record(20, 4)
assert sol.totalScore(4, 18) == 29
assert sol.totalScore(15, 20) == 15
sol.record(23, 6)
sol.record(24, 7)
sol.record(25, 3)
assert sol.totalScore(6, 20) == 37
assert sol.totalScore(12, 22) == 25
sol.record(28, 3)
sol.record(29, 8)
assert sol.totalScore(5, 16) == 28

sol = ExamTracker()  # random sequence 15
sol.record(3, 9)
sol.record(6, 5)
sol.record(8, 9)
sol.record(9, 8)
assert sol.totalScore(5, 7) == 5
assert sol.totalScore(6, 9) == 22
sol.record(10, 9)
sol.record(13, 1)
assert sol.totalScore(5, 12) == 31
sol.record(16, 9)
sol.record(18, 5)
sol.record(20, 7)
assert sol.totalScore(20, 20) == 7
sol.record(21, 7)
sol.record(24, 4)
assert sol.totalScore(23, 24) == 4
assert sol.totalScore(15, 24) == 32
assert sol.totalScore(17, 22) == 19
assert sol.totalScore(8, 20) == 48
sol.record(27, 8)
assert sol.totalScore(25, 26) == 0
sol.record(28, 4)
assert sol.totalScore(25, 28) == 12
sol.record(30, 3)
sol.record(31, 9)
sol.record(34, 9)
assert sol.totalScore(5, 31) == 88
assert sol.totalScore(21, 33) == 35
assert sol.totalScore(24, 31) == 28
assert sol.totalScore(1, 26) == 73

sol = ExamTracker()  # random sequence 16
sol.record(2, 3)
assert sol.totalScore(2, 2) == 3
sol.record(5, 8)
assert sol.totalScore(4, 4) == 0
assert sol.totalScore(5, 5) == 8
sol.record(6, 4)
assert sol.totalScore(2, 3) == 3
assert sol.totalScore(3, 6) == 12
sol.record(9, 7)
sol.record(12, 9)
assert sol.totalScore(1, 10) == 22
assert sol.totalScore(9, 12) == 16
sol.record(14, 3)
sol.record(15, 8)
assert sol.totalScore(13, 14) == 3
assert sol.totalScore(4, 4) == 0
assert sol.totalScore(9, 15) == 27
assert sol.totalScore(11, 14) == 12
assert sol.totalScore(7, 15) == 27
assert sol.totalScore(6, 13) == 20
assert sol.totalScore(5, 11) == 19
sol.record(17, 7)
sol.record(18, 3)
assert sol.totalScore(16, 18) == 10
assert sol.totalScore(1, 17) == 49
assert sol.totalScore(12, 16) == 20
assert sol.totalScore(18, 18) == 3
sol.record(20, 8)
assert sol.totalScore(16, 20) == 18
sol.record(21, 6)

sol = ExamTracker()  # random sequence 17
sol.record(3, 5)
assert sol.totalScore(1, 3) == 5
sol.record(5, 2)
sol.record(7, 2)
sol.record(9, 5)
sol.record(12, 8)
sol.record(14, 7)
sol.record(15, 3)
assert sol.totalScore(3, 12) == 22
assert sol.totalScore(15, 15) == 3
sol.record(17, 4)
sol.record(19, 6)
assert sol.totalScore(8, 8) == 0
assert sol.totalScore(2, 10) == 14
sol.record(20, 4)
sol.record(22, 9)
sol.record(24, 8)
sol.record(26, 2)
assert sol.totalScore(6, 19) == 35
sol.record(28, 4)
sol.record(30, 1)
sol.record(33, 8)
sol.record(34, 3)
assert sol.totalScore(31, 34) == 11
sol.record(37, 4)
assert sol.totalScore(17, 31) == 38
sol.record(39, 8)
assert sol.totalScore(37, 37) == 4
sol.record(40, 1)
sol.record(42, 2)

sol = ExamTracker()  # random sequence 18
sol.record(2, 3)
sol.record(4, 2)
assert sol.totalScore(1, 3) == 3
sol.record(6, 8)
assert sol.totalScore(3, 5) == 2
sol.record(7, 3)
sol.record(10, 8)
sol.record(12, 5)
assert sol.totalScore(8, 9) == 0
assert sol.totalScore(9, 10) == 8
assert sol.totalScore(4, 12) == 26
sol.record(13, 8)
sol.record(16, 5)
sol.record(19, 6)
sol.record(20, 9)
sol.record(21, 6)
sol.record(24, 8)
sol.record(27, 1)
assert sol.totalScore(20, 25) == 23
assert sol.totalScore(21, 25) == 14
assert sol.totalScore(19, 20) == 15
assert sol.totalScore(14, 17) == 5
assert sol.totalScore(16, 19) == 11
assert sol.totalScore(5, 13) == 32
sol.record(29, 1)
sol.record(32, 8)
assert sol.totalScore(22, 29) == 10
assert sol.totalScore(20, 22) == 15
assert sol.totalScore(8, 24) == 55
sol.record(35, 2)

sol = ExamTracker()  # random sequence 19
sol.record(2, 1)
assert sol.totalScore(1, 1) == 0
assert sol.totalScore(1, 1) == 0
sol.record(3, 9)
assert sol.totalScore(1, 2) == 1
sol.record(6, 9)
assert sol.totalScore(2, 3) == 10
assert sol.totalScore(6, 6) == 9
assert sol.totalScore(1, 2) == 1
assert sol.totalScore(4, 4) == 0
sol.record(7, 2)
sol.record(9, 5)
sol.record(11, 2)
assert sol.totalScore(8, 11) == 7
assert sol.totalScore(10, 10) == 0
assert sol.totalScore(3, 9) == 25
sol.record(14, 1)
assert sol.totalScore(4, 5) == 0
assert sol.totalScore(4, 12) == 18
assert sol.totalScore(12, 12) == 0
assert sol.totalScore(7, 10) == 7
sol.record(15, 3)
sol.record(17, 4)
sol.record(18, 5)
sol.record(19, 3)
assert sol.totalScore(7, 16) == 13
sol.record(22, 3)
sol.record(25, 8)
assert sol.totalScore(4, 8) == 11
assert sol.totalScore(7, 23) == 28

sol = ExamTracker()  # random sequence 20
sol.record(3, 1)
assert sol.totalScore(3, 3) == 1
assert sol.totalScore(1, 2) == 0
sol.record(6, 9)
assert sol.totalScore(5, 6) == 9
sol.record(7, 1)
assert sol.totalScore(3, 5) == 1
sol.record(10, 5)
assert sol.totalScore(6, 6) == 9
assert sol.totalScore(5, 8) == 10
sol.record(12, 7)
sol.record(13, 2)
sol.record(16, 7)
assert sol.totalScore(11, 11) == 0
sol.record(18, 7)
assert sol.totalScore(5, 10) == 15
sol.record(19, 8)
assert sol.totalScore(8, 18) == 28
sol.record(22, 5)
sol.record(25, 8)
assert sol.totalScore(25, 25) == 8
sol.record(26, 2)
sol.record(28, 8)
assert sol.totalScore(8, 15) == 14
sol.record(31, 4)
sol.record(32, 4)
sol.record(35, 8)
sol.record(38, 6)
assert sol.totalScore(36, 38) == 6
assert sol.totalScore(7, 20) == 37
