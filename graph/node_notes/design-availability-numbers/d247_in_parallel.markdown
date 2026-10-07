REFERENCE: d247 In Parallel
SOURCE: System Design Primer, "Availability in parallel vs in sequence" https://github.com/donnemartin/system-design-primer#availability-in-parallel-vs-in-sequence

REQUIRED
- In parallel: total = 1 - (1 - A) * (1 - B).
- 1 - 0.001 * 0.001 = 0.999999, so 99.9999%, higher than either component.

ALSO TRUE
- The pair is down only when both are down, and the probability that both
  are down is the product of the unavailabilities.
