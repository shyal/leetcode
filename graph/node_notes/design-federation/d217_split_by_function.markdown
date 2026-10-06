REFERENCE: d217 Split By Function
SOURCE: System Design Primer, "Federation" https://github.com/donnemartin/system-design-primer#federation

REQUIRED
- Federation, or functional partitioning, splits databases by function: for
  example forums, users and products in three databases instead of one.
- Each database gets less read and write traffic, and so less replication
  lag.
- Smaller databases mean more of the data fits in memory, which gives more
  cache hits.
- With no single central master serialising writes, writes go in parallel,
  which increases throughput.
- Three disadvantages out of: it is not effective if the schema requires
  huge functions or tables; application logic must decide which database to
  read and write; joining data from two databases is more complex, with a
  server link; it adds hardware and complexity.
