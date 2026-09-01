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

First thought that comes to mind is that this is likely a BFS. Since we're given a bank
of mutations, the set of choices is small, and we likely need to be able to decide whether
a mutation is worth queing up.

It's strange that for both examples, the target is in the bank. This suggests a single mutation.
Let's check the asserts. Ah ok i'm guessing that we can't mutate to it, because it requires only
one letter change.

So we need to only mutate one letter, and land on a gene in the bank.


Bank:

"AACCGGTA","AACCGCTA","AAACGGTA"

AACCGGTT start
       |
       v
AACCGGTA
  |
  v
AAACGGTA end


So on each rep, we have a couple of choices, either we can generate mutation candidates,
and check if they're in the bank, or we can search the bank for a mutation that's only
one letter away.

And we also probably need to decide if the mutation actually gets us closer or
further from the target.

An optimization would be to create a hash of the string, to avoid costly string comparisons,
or create a list of sets with the allowed letters per position.

Hmm i don't really feel like i can't start coding this yet. Maybe some pseudocode.

- create a queue with the startGene and distance
- while queue
-   base case:
-       if it's the target gene, return the distance
-   grab a gene mutations from the bank that are 1 letter apart
-   put them onto the queue, with dist + 1

Let's try this first.

Ok this passes. Code could be optimized. The visited set is suboptimal,
and could use hashing.

Let's run this on lc.

"""


class Solution:
    def minMutation(self, startGene: str, endGene: str, bank: List[str]) -> int:
        q = deque([(startGene, 0)])
        visited = set([])
        visited.add(startGene)

        while q:
            gene, dist = q.pop()
            if gene == endGene:
                return dist

            for b in bank:
                if sum(x != y for x, y in zip(gene, b)) != 1 or b in visited:
                    continue
                else:
                    q.append((b, dist + 1))
                    visited.add(b)

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
