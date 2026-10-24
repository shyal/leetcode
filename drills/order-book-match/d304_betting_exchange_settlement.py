"""
A betting exchange operates a single market with one selection, such as "Team A wins."

Users submit bets before the event ends. Each bet is one of:

- BACK: The user bets that the selection will win.
- LAY: The user bets that the selection will not win.

Each bet specifies a user ID, decimal odds represented as an integer, and a stake in pence.

Process all bets in order, matching them according to the rules below. When the final `SETTLE` operation arrives, return each user's total profit or loss.

Odds and Stakes

Odds are represented in hundredths. For example:

- `200` means decimal odds of `2.00`.
- `235` means decimal odds of `2.35`.

For both BACK and LAY bets, stake means the backer's stake, not the layer's liability.

Every submitted stake is a positive multiple of `100` pence. Matched stakes therefore remain multiples of `100`, making all settlement calculations exact.

Matching Rules

A BACK bet with odds `b` and a LAY bet with odds `l` can match if and only if:

    b <= l

Thus, a BACK bet's submitted odds are its minimum acceptable odds, while a LAY bet's submitted odds are its maximum acceptable odds.

When a new bet arrives, match it against compatible, unmatched opposite bets that are already waiting:

1. Price priority
   - An incoming BACK bet matches waiting LAY bets with the highest odds first.
   - An incoming LAY bet matches waiting BACK bets with the lowest odds first.
2. Time priority
   - Among waiting bets with equal odds, match the bet submitted earliest first.
3. Execution odds
   - Each match uses the submitted odds of the waiting bet, not those of the incoming bet.
4. Matched stake
   - Each match uses the smaller of the two bets' remaining stakes.
   - Subtract that amount from both remaining stakes.
5. Continue until the incoming bet is fully matched or no compatible waiting bet remains.
6. Any unmatched portion of the incoming bet becomes a waiting bet at its submitted odds.

A partially matched waiting bet retains its original time priority.

Bets belonging to the same user may match each other. All bets are accepted without balance checks. There are no fees, cancellations, or bet modifications.

Settlement Rules

The final operation specifies whether the selection won.

For each matched portion with stake `s` pence and execution odds `o`, define:

    profit = (s // 100) * (o - 100)

This is both the backer's potential profit and the layer's liability.

    | Outcome               | Backer's profit/loss | Layer's profit/loss |
    |-----------------------|---------------------:|--------------------:|
    | Selection won         |            `+profit` |           `-profit` |
    | Selection did not win |                 `-s` |                `+s` |

Unmatched portions are void and contribute `0`. Return net profit or loss, not returned stakes or account balances.

mu Function Signature

    class Solution
      def settle_market(operations: [list]) -> [[int]]

Input Format

`operations` contains records in chronological order:

- `["BET", user_id, side, odds, stake]`
  - `user_id` is an integer identifying the user.
  - `side` is either `"BACK"` or `"LAY"`.
  - `odds` is the integer odds representation.
  - `stake` is the stake in pence.
- `["SETTLE", won]`
  - `won` is `1` if the selection won, or `0` otherwise.

There is exactly one `SETTLE` operation, and it is the final operation.

Output Format

Return a list of `[user_id, net_profit_loss]` pairs, sorted by `user_id` in ascending order.

Include every user who submitted at least one bet, even if their net profit or loss is `0`. All amounts are in pence.

Example 1

Input:

    operations = [
        ["BET", 1, "BACK", 235, 300],
        ["BET", 2, "LAY", 250, 200],
        ["BET", 3, "LAY", 220, 100],
        ["SETTLE", 1]
    ]

Output:

    [[1, 270], [2, -270], [3, 0]]

Explanation:

User `2`'s LAY bet matches `200` pence of user `1`'s waiting BACK bet at the waiting odds of `235`.

The remaining BACK stake of `100` pence cannot match user `3`'s LAY bet because `235 > 220`.

The selection wins, so user `1` earns:

    (200 // 100) * (235 - 100) = 270 pence

User `2` loses `270` pence. Both unmatched portions contribute nothing.

Example 2

Input:

    operations = [
        ["BET", 10, "LAY", 220, 100],
        ["BET", 20, "LAY", 250, 100],
        ["BET", 30, "LAY", 250, 200],
        ["BET", 40, "BACK", 210, 200],
        ["SETTLE", 0]
    ]

Output:

    [[10, 0], [20, 100], [30, 100], [40, -200]]

Explanation:

User `40`'s BACK bet takes the highest waiting LAY odds, `250`, before odds `220`.

At odds `250`, user `20` has time priority over user `30`. Therefore, user `40` matches:

- `100` pence with user `20` at odds `250`.
- `100` pence with user `30` at odds `250`.

The selection does not win. User `40` loses the total matched stake of `200` pence, while users `20` and `30` each gain `100` pence. All remaining stakes are void.

Constraints:

- `2 <= len(operations) <= 2001`
- There are between `1` and `2000` `BET` operations.
- `1 <= user_id <= 10^9`
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
    ["BET", 1, "BACK", 235, 300],
    ["BET", 2, "LAY", 250, 200],
    ["BET", 3, "LAY", 220, 100],
    ["SETTLE", 1],
]
print(operations)
print(sol.settle_market(operations))  # [[1, 270], [2, -270], [3, 0]]

# assert sol.settle_market(operations) == [[1, 270], [2, -270], [3, 0]]
# assert sol.settle_market([["BET", 10, "LAY", 220, 100], ["BET", 20, "LAY", 250, 100], ["BET", 30, "LAY", 250, 200], ["BET", 40, "BACK", 210, 200], ["SETTLE", 0]]) == [[10, 0], [20, 100], [30, 100], [40, -200]]
# assert sol.settle_market([["BET", 5, "BACK", 200, 100], ["SETTLE", 1]]) == [[5, 0]]
# assert sol.settle_market([["BET", 7, "BACK", 200, 100], ["BET", 7, "LAY", 200, 100], ["SETTLE", 1]]) == [[7, 0]]
# assert sol.settle_market([["BET", 1, "LAY", 300, 100], ["BET", 2, "LAY", 250, 200], ["BET", 3, "BACK", 240, 400], ["SETTLE", 1]]) == [[1, -200], [2, -300], [3, 500]]
# assert sol.settle_market([["BET", 1, "BACK", 210, 200], ["BET", 2, "BACK", 200, 100], ["BET", 3, "BACK", 200, 100], ["BET", 4, "LAY", 220, 300], ["SETTLE", 0]]) == [[1, -100], [2, -100], [3, -100], [4, 300]]
# assert sol.settle_market([["BET", 9, "LAY", 200, 100], ["BET", 2, "BACK", 210, 100], ["SETTLE", 0]]) == [[2, 0], [9, 0]]
# assert sol.settle_market([["BET", 1, "BACK", 200, 100], ["BET", 2, "LAY", 200, 100], ["SETTLE", 1]]) == [[1, 100], [2, -100]]
# assert sol.settle_market([["BET", 1, "LAY", 300, 100], ["BET", 2, "BACK", 150, 100], ["SETTLE", 1]]) == [[1, -200], [2, 200]]
# assert sol.settle_market([["BET", 1, "BACK", 101, 100], ["BET", 2, "LAY", 101, 100], ["SETTLE", 1]]) == [[1, 1], [2, -1]]
# assert sol.settle_market([["BET", 1, "LAY", 10000, 1000000], ["BET", 2, "BACK", 10000, 1000000], ["SETTLE", 1]]) == [[1, -99000000], [2, 99000000]]
# assert sol.settle_market([["BET", 1, "BACK", 200, 300], ["BET", 2, "BACK", 200, 100], ["BET", 3, "LAY", 200, 100], ["BET", 4, "LAY", 200, 200], ["SETTLE", 0]]) == [[1, -300], [2, 0], [3, 100], [4, 200]]
# assert sol.settle_market([["BET", 1, "LAY", 220, 100], ["BET", 2, "BACK", 200, 300], ["BET", 3, "LAY", 200, 200], ["SETTLE", 1]]) == [[1, -120], [2, 320], [3, -200]]
# assert sol.settle_market([["BET", 1, "BACK", 200, 100], ["BET", 2, "LAY", 200, 100], ["BET", 2, "BACK", 300, 100], ["BET", 1, "LAY", 300, 100], ["SETTLE", 1]]) == [[1, -100], [2, 100]]
# assert sol.settle_market([["BET", 3, "LAY", 200, 100], ["BET", 1, "LAY", 300, 100], ["SETTLE", 0]]) == [[1, 0], [3, 0]]
