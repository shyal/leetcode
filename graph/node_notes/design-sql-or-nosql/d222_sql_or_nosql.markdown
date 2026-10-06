REFERENCE: d222 SQL Or NoSQL
SOURCE: System Design Primer, "SQL or NoSQL" https://github.com/donnemartin/system-design-primer#sql-or-nosql

REQUIRED
- SQL, four out of: structured data; strict schema; relational data; need
  for complex joins; transactions; clear patterns for scaling; more
  established developers, community, code and tools; lookups by index are
  very fast.
- NoSQL, four out of: semi-structured data; dynamic or flexible schema;
  non-relational data; no need for complex joins; many TB or PB of data; a
  very data intensive workload; very high throughput for IOPS.
- Data that suits NoSQL, two out of: rapid ingest of clickstream and log
  data; leaderboard or scoring data; temporary data such as a shopping cart;
  frequently accessed hot tables; metadata and lookup tables.
