REFERENCE: d281 Sales Rank Writes
SOURCE: System Design Primer, "Design Amazon's sales rank by category feature" https://github.com/donnemartin/system-design-primer/blob/master/solutions/system_design/sales_rank/README.md

REQUIRED
- Writes: 400 per second may be tough for a single SQL Write Master-Slave,
  which also calls for further scaling, federation, sharding, denormalization,
  SQL tuning, or moving data to NoSQL.

ALSO TRUE
- Keep a limited period of data in the database and the rest in a data
  warehouse or the Object Store.
