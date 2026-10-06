REFERENCE: d221 Four Kinds Of NoSQL
SOURCE: System Design Primer, "NoSQL" https://github.com/donnemartin/system-design-primer#nosql

REQUIRED
- Key-value store: a hash table, O(1) reads and writes, often backed by
  memory or SSD. Used for simple data models or rapidly changing data, such
  as an in-memory cache layer. Redis, Memcached.
- Document store: a key-value store with documents, JSON or XML, as values,
  queryable on the internal structure of the document. Used for occasionally
  changing data, with high flexibility. MongoDB, CouchDB.
- Wide column store: a nested map, ColumnFamily<RowKey, Columns<ColKey,
  Value, Timestamp>>. Used for very large data sets, with high availability
  and high scalability. Bigtable, HBase, Cassandra.
- Graph database: a graph, each node a record and each arc a relationship.
  Used for data models with complex relationships, such as a social network.
  Neo4j.

ALSO TRUE
- NoSQL data is denormalized and joins are generally done in application
  code; most stores lack true ACID transactions and favour eventual
  consistency.
- BASE: basically available, soft state, eventual consistency.
- Wide column stores keep keys in lexicographic order, which allows
  efficient retrieval of key ranges.
