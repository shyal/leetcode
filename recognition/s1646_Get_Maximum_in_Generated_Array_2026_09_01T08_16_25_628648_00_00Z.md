You are given an integer `n`. A **0-indexed** integer array `nums` of length `n + 1` is generated in the following way:

- `nums[0] = 0`
- `nums[1] = 1`
- `nums[2 * i] = nums[i]` when `2 <= 2 * i <= n`
- `nums[2 * i + 1] = nums[i] + nums[i + 1]` when `2 <= 2 * i + 1 <= n`

Return _the **maximum** integer in the array_ `nums`​​​.

**Example 1:**

```
Input: n = 7
Output: 3
Explanation: According to the given rules:
  nums[0] = 0
  nums[1] = 1
  nums[(1 * 2) = 2] = nums[1] = 1
  nums[(1 * 2) + 1 = 3] = nums[1] + nums[2] = 1 + 1 = 2
  nums[(2 * 2) = 4] = nums[2] = 1
  nums[(2 * 2) + 1 = 5] = nums[2] + nums[3] = 1 + 2 = 3
  nums[(3 * 2) = 6] = nums[3] = 2
  nums[(3 * 2) + 1 = 7] = nums[3] + nums[4] = 2 + 1 = 3
Hence, nums = [0,1,1,2,1,3,2,3], and the maximum is max(0,1,1,2,1,3,2,3) = 3.
```

**Example 2:**

```
Input: n = 2
Output: 1
Explanation: According to the given rules, nums = [0,1,1]. The maximum is max(0,1,1) = 1.
```

**Example 3:**

```
Input: n = 3
Output: 2
Explanation: According to the given rules, nums = [0,1,1,2]. The maximum is max(0,1,1,2) = 2.
```

**Constraints:**

- `0 <= n <= 100`

## <!-- answer -->

- `nums[0] = 0`
- `nums[1] = 1`
- `nums[2 * i] = nums[i]` when `2 <= 2 * i <= n`
- `nums[2 * i + 1] = nums[i] + nums[i + 1]` when `2 <= 2 * i + 1 <= n`

At least n is small, so in a solve i'd probably just implement it without thinking about it too much:

```
nums = [0, 1] + [-1] * 2

for i in range(n + 1, -1, -1):
    nums[i*2] =

```

Hmm no nevermind that, recursion will probably be much simpler, and i'm guessing that:

- `nums[0] = 0`
- `nums[1] = 1`

These are the base cases.

```
nums = [0, 1] + [-1] * 2

def num(i, n):
    # or instead of base case, just use memo
    if nums[i] != -1:
        return nums[i]
    if 0 <= i <= 1:
        v = num(2 * i)
        return v
    if 2 <= 2 * i <= n:
        nums[2 * i + 1] = num(i) + num(i + 1)

res = max(nums)

```

The above should be treated as pseudocode, as i wasn't able to run it. But the gist is to understand that this question is asking to build a recursive function that satisfies the recurrence relations in the problem statement.

<!-- spot {"problem": "1646", "target": "dp-1d-rolling", "reason": "failed to recognize last time, 159 problem(s) need only it", "seconds": 659} -->
