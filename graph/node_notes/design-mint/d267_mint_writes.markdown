REFERENCE: d267 Mint Writes
SOURCE: System Design Primer, "Design Mint.com" https://github.com/donnemartin/system-design-primer/blob/master/solutions/system_design/mint/README.md

REQUIRED
- Writes: 2,000 per second is tough for a single SQL Write Master-Slave, so
  apply SQL scaling patterns, federation, sharding, denormalization, SQL
  tuning, and consider moving data to NoSQL; keep only a month of transactions
  in the database and the rest in a data warehouse or the Object Store.

ALSO TRUE
- MapReduce over the raw transaction files can categorise and aggregate,
  taking load off the database.
- Reads of summaries and recent transactions go through a Memory Cache, cache-
  aside.
