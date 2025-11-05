"""
URL: https://codeforces.com/contest/2167/problem/B

2167B. Your Name

khba is writing his girlfriend's name. He has 𝑛 cubes, each with one lowercase Latin letter written on it. They are arranged in a row, forming a string 𝑠. His girlfriend's name is also a string 𝑡, consisting of 𝑛 lowercase Latin letters.

To prove his love, he must check whether it is possible to rearrange the letters of string 𝑠 so that it becomes her name 𝑡.

Input
The first line contains an integer 𝑞 (1≤𝑞≤1000) — the number of test cases.

The first line of each test case contains an integer 𝑛 (1≤𝑛≤20).

The second line of each test case contains two distinct strings 𝑠 and 𝑡, each consisting of 𝑛 lowercase Latin letters.

Output
For each test case, output "YES" if the letters of 𝑠 can be arranged to form 𝑡; otherwise, output "NO".

You can output the answer in any case (upper or lower). For example, the strings "yEs", "yes", "Yes" and "YES" will be recognized as positive responses.

Example
Input
5
7
humitsa mitsuha
4
orhi hori
6
aakima makima
6
nezuqo nezuko
6
misaka mikasa
Output
YES
YES
NO
NO
YES

Note
In the first example, the initial string is "humitsa", and the following operations can be performed:

swap the first and third characters, resulting in "muhitsa"
swap the second and fourth characters, resulting in "mihutsa"
swap the third and fifth characters, resulting in "mithusa"
swap the fourth and sixth characters, resulting in "mitsuha"
In the second example, the initial string is "orhi", and the following operations can be performed:

swap the second and third characters, resulting in "ohri"
swap the first and second characters, resulting in "hori"

Constraints:
- 1 ≤ q ≤ 1000
- 1 ≤ n ≤ 20
- s and t consist of lowercase Latin letters
- s and t are distinct
"""


def solve(n: int, s: str, t: str) -> str:
    return ["NO", "YES"][Counter(s) == Counter(t)]


def main():
    q = int(input())
    for _ in range(q):
        n = int(input())
        s, t = input().split()
        print(solve(n, s, t))


input1 = """5
7
humitsa mitsuha
4
orhi hori
6
aakima makima
6
nezuqo nezuko
6
misaka mikasa
"""
# print(run_with_input(input1, main))
assert run_with_input(input1, main) == "YES\nYES\nNO\nNO\nYES"

input2 = """1
1
a b
"""
# print(run_with_input(input2, main))
assert run_with_input(input2, main) == "NO"

input3 = """1
2
ab ba
"""
# print(run_with_input(input3, main))
assert run_with_input(input3, main) == "YES"

input4 = """1
2
aa ab
"""
# print(run_with_input(input4, main))
assert run_with_input(input4, main) == "NO"

input5 = """2
3
abc acb
3
abc abd
"""
# print(run_with_input(input5, main))
assert run_with_input(input5, main) == "YES\nNO"

input6 = """1
20
abcdefghijklmnopqrst abcdefghijklmnopqrts
"""
# print(run_with_input(input6, main))
assert run_with_input(input6, main) == "YES"

input7 = """1
5
aaabb ababa
"""
# print(run_with_input(input7, main))
assert run_with_input(input7, main) == "YES"

input8 = """1
5
aaabb aaaab
"""
# print(run_with_input(input8, main))
assert run_with_input(input8, main) == "NO"

print("All tests passed")
