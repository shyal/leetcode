# REFERENCE: d137 Subarrays Summing To Target
def countSubarrays(vals: [int], target: int) -> int
  D = counter([0])
  sum for prefix in scan(+, vals)
    got = D[prefix - target]
    D[prefix] += 1
    got
