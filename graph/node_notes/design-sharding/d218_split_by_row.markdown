REFERENCE: d218 Split By Row
SOURCE: System Design Primer, "Sharding" https://github.com/donnemartin/system-design-primer#sharding

REQUIRED
- Sharding distributes data across different databases so that each database
  manages only a subset of the data.
- A table of users is commonly sharded by the initial of the last name or by
  geographic location.
- Three benefits out of: less read and write traffic per shard; less
  replication; more cache hits; smaller indexes and so faster queries; if
  one shard goes down the others still operate; writes go in parallel, with
  no single central master serialising them.
- Three disadvantages out of: application logic must work with shards, which
  can mean complex SQL queries; data distribution can become lopsided, as
  when a set of power users loads one shard; joining data from several
  shards is more complex; it adds hardware and complexity.
- Rebalancing adds complexity; a sharding function based on consistent
  hashing reduces the amount of data transferred.

ALSO TRUE
- Each shard still needs some form of replication to avoid data loss.
