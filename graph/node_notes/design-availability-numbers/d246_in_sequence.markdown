REFERENCE: d246 In Sequence
SOURCE: System Design Primer, "Availability in parallel vs in sequence" https://github.com/donnemartin/system-design-primer#availability-in-parallel-vs-in-sequence

REQUIRED
- In sequence: total = A * B.
- 0.999 * 0.999 = 0.998001, so 99.8%, lower than either component.

ALSO TRUE
- The pair is up only when both are up, and the probability that both are
  up is the product.
