"""
URL: https://codeforces.com/contest/2162/problem/A

2162a. Beautiful Average

You are given an array a of length n.

Your task is to find the maximum possible average value of any subarray of the array a.

Formally, for any indices l, r such that 1 ≤ l ≤ r ≤ n, define the average of the subarray a_l, a_{l+1}, ..., a_r as the sum of elements divided by the number of elements or:
avg(l, r) = (1 / (r - l + 1)) * sum_{i=l to r} a_i

Output the maximum value of avg(l, r) over all choices of l, r.

* An array b is a subarray of an array a if b can be obtained from a by deletion of several (possibly, zero or all) elements from the beginning and several (possibly, zero or all) elements from the end. In particular, an array is a subarray of itself.

Input
The first line contains a single integer t (1 ≤ t ≤ 10^4) — the number of test cases.

The first line of each testcase contains a single integer n (1 ≤ n ≤ 10) — the length of the array a.

The second line of each testcase contains n integers a_1, a_2, ..., a_n (1 ≤ a_i ≤ 10) — the elements of the array.

Output
For each testcase, output a single integer — the maximum average of any subarray of the given array.

It can be shown that the answer is always an integer.

Example

Input
3
4
3 3 3 3
5
7 1 6 9 9
5
3 4 4 4 3

Output
3
9
4


Constraints:

- 1 ≤ t ≤ 10^4
- 1 ≤ n ≤ 10
- 1 ≤ a_i ≤ 10
"""


def main():
    t = int(input())
    for _ in range(t):
        n = int(input())
        nums = list(map(int, input().split()))
        print(max(nums))


input1 = """3
4
3 3 3 3
5
7 1 6 9 9
5
3 4 4 4 3
"""
# print(run_with_input(input1))  # 3\n9\n4

assert run_with_input(input1, main) == "3\n9\n4"

input2 = """1
1
5
"""
assert run_with_input(input2, main) == "5"

input3 = """1
2
1 10
"""
assert run_with_input(input3, main) == "10"

input4 = """1
10
1 1 1 1 1 1 1 1 1 1
"""
assert run_with_input(input4, main) == "1"

input5 = """1
10
10 10 10 10 10 10 10 10 10 10
"""
assert run_with_input(input5, main) == "10"

input6 = """2
1
1
1
2
"""
assert run_with_input(input6, main) == "1\n2"

input7 = """1
5
1 2 10 2 1
"""
assert run_with_input(input7, main) == "10"

input8 = """1
3
10 1 10
"""
assert run_with_input(input8, main) == "10"

input9 = """1
1
1
"""
assert run_with_input(input9, main) == "1"

input10 = """1
1
10
"""
assert run_with_input(input10, main) == "10"
