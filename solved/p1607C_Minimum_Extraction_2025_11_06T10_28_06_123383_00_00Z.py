"""
URL: https://codeforces.com/contest/1607/problem/C

1607C. Minimum Extraction

Yelisey has an array a of n integers.

If a has length strictly greater than 1, then Yelisey can apply an operation called minimum extraction to it:

First, Yelisey finds the minimal number m in the array. If there are several identical minima, Yelisey can choose any of them.
Then the selected minimal element is removed from the array. After that, m is subtracted from each remaining element.
Thus, after each operation, the length of the array is reduced by 1.

For example, if a = [1, 6, -4, -2, -4], then the minimum element in it is a3 = -4, which means that after this operation the array will be equal to a = [1 - (-4), 6 - (-4), -2 - (-4), -4 - (-4)] = [5, 10, 2, 0].

Since Yelisey likes big numbers, he wants the numbers in the array a to be as big as possible.

Formally speaking, he wants to make the minimum of the numbers in array a to be maximal possible (i.e. he wants to maximize a minimum). To do this, Yelisey can apply the minimum extraction operation to the array as many times as he wants (possibly, zero). Note that the operation cannot be applied to an array of length 1.

Help him find what maximal value can the minimal element of the array have after applying several (possibly, zero) minimum extraction operations to the array.

Input
The first line contains an integer t (1 ≤ t ≤ 10^4) — the number of test cases.

The next 2t lines contain descriptions of the test cases.

In the description of each test case, the first line contains an integer n (1 ≤ n ≤ 2⋅10^5) — the original length of the array a. The second line of the description lists n space-separated integers a_i (-10^9 ≤ a_i ≤ 10^9) — elements of the array a.

It is guaranteed that the sum of n over all test cases does not exceed 2⋅10^5.

Output
Print t lines, each of them containing the answer to the corresponding test case. The answer to the test case is a single integer — the maximal possible minimum in a, which can be obtained by several applications of the described operation to it.

Example
Input
8
1
10
2
0 0
3
-1 2 0
4
2 10 1 7
2
2 3
5
3 2 -4 -2 0
2
-1 1
1
-2
Output
10
0
2
5
2
2
2
-2

Note
In the first example test case, the original length of the array n=1. Therefore minimum extraction cannot be applied to it. Thus, the array remains unchanged and the answer is a1=10.

In the second set of input data, the array will always consist only of zeros.

In the third set, the array will be changing as follows: [-1, 2, 0] → [3, 1] → [2]. The minimum elements are highlighted with blue. The maximal one is 2.

In the fourth set, the array will be modified as [2, 10, 1, 7] → [1, 9, 6] → [8, 5] → [3]. Similarly, the maximum of the minimum elements is 5.

Constraints:
- 1 ≤ t ≤ 10^4
- 1 ≤ n ≤ 2⋅10^5
- Sum of n over all test cases ≤ 2⋅10^5
- -10^9 ≤ a_i ≤ 10^9
"""


def main():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        if len(a) == 1:
            print(a[0])
        else:
            a.sort(reverse=True)
            _max = 0
            offset = 0
            while a:
                _min = a.pop() - offset
                _max = max(_max, _min)
                offset += _min
            print(_max)


input1 = """8
1
10
2
0 0
3
-1 2 0
4
2 10 1 7
2
2 3
5
3 2 -4 -2 0
2
-1 1
1
-2
"""
print(run_with_input(input1, main))  # 10\n0\n2\n5\n2\n2\n2\n-2

assert run_with_input(input1, main) == "10\n0\n2\n5\n2\n2\n2\n-2"

input2 = """1
2
-1000000000 1000000000
"""
assert run_with_input(input2, main) == "2000000000"

input3 = """1
1
0
"""
assert run_with_input(input3, main) == "0"

input4 = """1
3
-1 -1 -1
"""
assert run_with_input(input4, main) == "0"

input5 = """1
3
5 5 5
"""
assert run_with_input(input5, main) == "5"

input6 = """1
3
-5 -3 -1
"""
assert run_with_input(input6, main) == "2"

input7 = """2
1
999999999
2
1 2
"""
assert run_with_input(input7, main) == "999999999\n1"
