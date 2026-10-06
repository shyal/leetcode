REFERENCE: d204 Slow For One Or Slow Under Load
SOURCE: System Design Primer, "Performance vs scalability" https://github.com/donnemartin/system-design-primer#performance-vs-scalability

REQUIRED
- A performance problem: the system is slow for a single user.
- A scalability problem: the system is fast for a single user but slow under
  heavy load.
- A service is scalable if its performance increases in proportion to the
  resources added.

ALSO TRUE
- More performance usually means serving more units of work; it can also
  mean handling larger units of work, as when datasets grow.
