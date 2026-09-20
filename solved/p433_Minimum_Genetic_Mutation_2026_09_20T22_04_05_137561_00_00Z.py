"""
URL: https://leetcode.com/problems/minimum-genetic-mutation/description/?envType=problem-list-v2&envId=vn57k9wr

433. Minimum Genetic Mutation

A gene string can be represented by an 8-character long string, with choices from 'A', 'C', 'G', and 'T'.

Suppose we need to investigate a mutation from a gene string startGene to a gene string endGene where one mutation is defined as one single character changed in the gene string.

For example, "AACCGGTT" --> "AACCGGTA" is one mutation.

There is also a gene bank bank that records all the valid gene mutations. A gene must be in bank to make it a valid gene string.

Given the two gene strings startGene and endGene and the gene bank bank, return the minimum number of mutations needed to mutate from startGene to endGene. If there is no such a mutation, return -1.

Note that the starting point is assumed to be valid, so it might not be included in the bank.

Example 1:

Input: startGene = "AACCGGTT", endGene = "AACCGGTA", bank = ["AACCGGTA"]
Output: 1

Example 2:

Input: startGene = "AACCGGTT", endGene = "AAACGGTA", bank = ["AACCGGTA","AACCGCTA","AAACGGTA"]
Output: 2

Constraints:

    0 <= bank.length <= 10
    startGene.length == endGene.length == bank[i].length == 8
    startGene, endGene, and bank[i] consist of only the characters ['A', 'C', 'G', 'T'].


---

bank = ["AACCGGTA","AACCGCTA","AAACGGTA"]

AACCGGTT start
       *

AAACGGTA end

LEETCODE: Accepted (0 ms, 19.5 MB)
"""


class Solution:
    def minMutation(self, startGene: str, endGene: str, bank: List[str]) -> int:
        q = deque([[startGene, 0]])
        seen = set([])
        while q:
            g, dist = q.popleft()
            seen.add(g)

            if g == endGene:
                return dist

            for b in bank:
                if b in seen:
                    continue
                one_mutation = sum(a != b for a, b in zip(g, b)) == 1
                if one_mutation:
                    q.append([b, dist + 1])

        return -1


sol = Solution()

print(sol.minMutation("AACCGGTT", "AACCGGTA", ["AACCGGTA"]))  # 1

assert sol.minMutation("AACCGGTT", "AACCGGTA", ["AACCGGTA"]) == 1
assert (
    sol.minMutation("AACCGGTT", "AAACGGTA", ["AACCGGTA", "AACCGCTA", "AAACGGTA"]) == 2
)
assert (
    sol.minMutation("AAAAACCC", "AACCCCCC", ["AAAACCCC", "AAACCCCC", "AACCCCCC"]) == 3
)
assert sol.minMutation("AACCGGTT", "AACCGGTA", []) == -1
assert (
    sol.minMutation("AACCGGTT", "AACCGGTT", ["AACCGGTA"]) == 0
)  # start == end, no mutation needed

assert (
    sol.minMutation(
        "AAAAAAAA",
        "CCCCCCCC",
        [
            "AAAAAAAA",
            "AAAAAAAC",
            "AAAAAACC",
            "AAAAACCC",
            "AAAACCCC",
            "AAACCCCC",
            "AACCCCCC",
            "ACCCCCCC",
            "CCCCCCCC",
        ],
    )
    == 8
)
assert sol.minMutation("AAAAAAAA", "AAAAAAAA", []) == 0
assert (
    sol.minMutation(
        "AAAAAAAA",
        "TTTTTTTT",
        [
            "AAAAAAAA",
            "AAAAAAAT",
            "AAAAAATT",
            "AAAAATTT",
            "AAAATTTT",
            "AAATTTTT",
            "AATTTTTT",
            "ATTTTTTT",
            "TTTTTTTT",
        ],
    )
    == 8
)
assert sol.minMutation("AACCGGTT", "AACCGGTA", ["AACCGGTA", "AACCGGTT"]) == 1
assert (
    sol.minMutation("AACCGGTT", "AACCGGTA", ["AACCGGTA", "AACCGGTC", "AACCGGTT"]) == 1
)
assert sol.minMutation("AACCGGTT", "AACCGGTA", ["AACCGGTC", "AACCGGTT"]) == -1
assert (
    sol.minMutation("AACCGGTT", "AACCGGTA", ["AACCGGTA", "AACCGGTT", "AACCGGTA"]) == 1
)
assert (
    sol.minMutation(
        "AACCGGTT", "AACCGGTA", ["AACCGGTA", "AACCGGTT", "AACCGGTA", "AACCGGTT"]
    )
    == 1
)
assert (
    sol.minMutation(
        "AACCGGTT",
        "AACCGGTA",
        ["AACCGGTA", "AACCGGTT", "AACCGGTA", "AACCGGTT", "AACCGGTA"],
    )
    == 1
)
assert (
    sol.minMutation(
        "AACCGGTT",
        "AACCGGTA",
        ["AACCGGTA", "AACCGGTT", "AACCGGTA", "AACCGGTT", "AACCGGTA", "AACCGGTT"],
    )
    == 1
)
assert (
    sol.minMutation(
        "AACCGGTT",
        "AACCGGTA",
        [
            "AACCGGTA",
            "AACCGGTT",
            "AACCGGTA",
            "AACCGGTT",
            "AACCGGTA",
            "AACCGGTT",
            "AACCGGTA",
            "AACCGGTT",
            "AACCGGTA",
            "AACCGGTT",
        ],
    )
    == 1
)
assert (
    sol.minMutation(
        "AACCGGTT",
        "AACCGGTA",
        [
            "AACCGGTA",
            "AACCGGTT",
            "AACCGGTA",
            "AACCGGTT",
            "AACCGGTA",
            "AACCGGTT",
            "AACCGGTA",
            "AACCGGTT",
            "AACCGGTA",
            "AACCGGTT",
        ],
    )
    == 1
)
