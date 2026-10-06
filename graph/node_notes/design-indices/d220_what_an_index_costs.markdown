REFERENCE: d220 What An Index Costs
SOURCE: System Design Primer, "SQL tuning" https://github.com/donnemartin/system-design-primer#sql-tuning

REQUIRED
- Benchmark and profile first: benchmark by simulating high load, with a
  tool such as ab; profile with a tool such as the slow query log.
- Columns that are queried, in SELECT, GROUP BY, ORDER BY or JOIN, can be
  faster with indices.
- An index is usually a self-balancing B-tree: it keeps data sorted and
  allows searches, sequential access, insertions and deletions in
  logarithmic time.
- Cost: an index takes more space, and placing one can keep the data in
  memory.
- Cost: writes are slower, since the index must be updated too.

ALSO TRUE
- When loading large amounts of data it can be faster to disable indices,
  load, then rebuild them.
- Use DECIMAL for currency to avoid floating point representation errors.
