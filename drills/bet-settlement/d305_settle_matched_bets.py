"""
DRILL: Settle Matched Bets
TRAINS: bet-settlement

A betting exchange operates a single market with one selection, such as "Team A wins."

Users submit bets before the event ends. Each bet is one of:

- BACK: The user bets that the selection will win.
- LAY: The user bets that the selection will not win.

Each bet specifies a user ID, decimal odds represented as an integer, and a stake in pence.

You are given already-matched bets. Each record describes one matched portion: its backer's user ID, its layer's user ID, its execution odds, and its matched stake. When the final `SETTLE` operation arrives, return each user's total profit or loss.

Odds and Stakes

Odds are represented in hundredths. For example:

- `200` means decimal odds of `2.00`.
- `235` means decimal odds of `2.35`.

For both BACK and LAY bets, stake means the backer's stake, not the layer's liability.

Every matched stake is a positive multiple of `100` pence, making all settlement calculations exact.

The backer and layer of a matched portion may be the same user. All bets are accepted without balance checks. There are no fees, cancellations, or bet modifications.

Settlement Rules

The final operation specifies whether the selection won.

For each matched portion with stake `s` pence and execution odds `o`, define:

    profit = (s // 100) * (o - 100)

This is both the backer's potential profit and the layer's liability.

    | Outcome | Backer's profit/loss | Layer's profit/loss |
    |---|---:|---:|
    | Selection won | `+profit` | `-profit` |
    | Selection did not win | `-s` | `+s` |

Return net profit or loss, not returned stakes or account balances.

A user's net profit or loss is the sum of their profit or loss across all matched portions, including both roles if they are the backer and layer of the same portion.

mu Function Signature

    class Solution
      def settle_market(operations: [list]) -> [[int]]

Input Format

`operations` contains matched-portion records followed by the final settlement operation:

- `["MATCH", backer_id, layer_id, odds, stake]`
  - `backer_id` is an integer identifying the backer.
  - `layer_id` is an integer identifying the layer.
  - `odds` is the integer representation of the execution odds.
  - `stake` is the matched stake in pence.
  - Each record represents a separate matched portion, even if it is identical to another record.
- `["SETTLE", won]`
  - `won` is `1` if the selection won, or `0` otherwise.

There is exactly one `SETTLE` operation, and it is the final operation.

Output Format

Return a list of `[user_id, net_profit_loss]` pairs, sorted by `user_id` in ascending order.

Include every user who appears as a backer or layer in at least one matched portion, even if their net profit or loss is `0`. All amounts are in pence.

Example 1

Input:
    operations = [
        ["MATCH", 1, 2, 235, 300],
        ["SETTLE", 1]
    ]

Output:
    [[1, 405], [2, -405]]

Explanation:

The selection wins, so user `1` earns:

    (300 // 100) * (235 - 100) = 405 pence

User `2` loses `405` pence.

Example 2

Input:
    operations = [
        ["MATCH", 10, 20, 220, 100],
        ["MATCH", 30, 10, 250, 200],
        ["SETTLE", 0]
    ]

Output:
    [[10, 100], [20, 100], [30, -200]]

Explanation:

The selection does not win. In the first portion, user `10` loses `100` pence and user `20` gains `100` pence. In the second portion, user `30` loses `200` pence and user `10` gains `200` pence.

User `10`'s net profit is `-100 + 200 = 100` pence.

Example 3

Input:
    operations = [
        ["MATCH", 7, 7, 250, 200],
        ["SETTLE", 1]
    ]

Output:
    [[7, 0]]

Explanation:

User `7` is both the backer and the layer. The backer's profit of `300` pence and the layer's loss of `300` pence cancel. User `7` is still included in the output.

Constraints:

- `2 <= len(operations) <= 2001`
- There are between `1` and `2000` `MATCH` operations.
- `1 <= backer_id, layer_id <= 10^9`
- `101 <= odds <= 10000`
- `100 <= stake <= 10^6`
- Every stake is a multiple of `100`.
- Every operation follows the specified format.
- The only `SETTLE` operation is the final operation.
- All calculations and returned values must use integer arithmetic.
"""


class Solution:
    def settle_market(self, operations: list) -> list:
        pass


sol = Solution()

operations = [
    ["MATCH", 10, 20, 220, 100],
    ["MATCH", 30, 10, 250, 200],
    ["SETTLE", 0],
]
print(operations)
print(sol.settle_market(operations))  # [[10, 100], [20, 100], [30, -200]]

# assert sol.settle_market(operations) == [[10, 100], [20, 100], [30, -200]]
# assert sol.settle_market([["MATCH", 1, 2, 235, 300], ["SETTLE", 1]]) == [[1, 405], [2, -405]]
# assert sol.settle_market([["MATCH", 7, 7, 250, 200], ["SETTLE", 1]]) == [[7, 0]]
# assert sol.settle_market([["MATCH", 1, 2, 101, 100], ["SETTLE", 1]]) == [[1, 1], [2, -1]]
# assert sol.settle_market([["MATCH", 1, 2, 10000, 1000000], ["SETTLE", 1]]) == [[1, 99000000], [2, -99000000]]
# assert sol.settle_market([["MATCH", 1, 2, 10000, 1000000], ["SETTLE", 0]]) == [[1, -1000000], [2, 1000000]]
# assert sol.settle_market([["MATCH", 1, 2, 200, 100], ["MATCH", 2, 1, 300, 100], ["SETTLE", 1]]) == [[1, -100], [2, 100]]
# assert sol.settle_market([["MATCH", 1, 2, 200, 100], ["MATCH", 2, 1, 300, 100], ["SETTLE", 0]]) == [[1, 0], [2, 0]]
# assert sol.settle_market([["MATCH", 9, 3, 200, 100], ["MATCH", 9, 3, 200, 100], ["SETTLE", 1]]) == [[3, -200], [9, 200]]
