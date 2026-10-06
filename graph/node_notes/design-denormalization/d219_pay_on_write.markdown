REFERENCE: d219 Pay On Write
SOURCE: System Design Primer, "Denormalization" https://github.com/donnemartin/system-design-primer#denormalization

REQUIRED
- Denormalization improves read performance at the expense of some write
  performance.
- Redundant copies of the data are written in multiple tables to avoid
  expensive joins.
- In most systems reads outnumber writes 100:1 or even 1000:1, and a read
  that needs a complex join is very expensive.
- Materialized views, in PostgreSQL and Oracle, store the redundant
  information and keep the copies consistent.
- Three disadvantages: data is duplicated; constraints that keep the copies
  in sync complicate the database design; under heavy write load a
  denormalized database may perform worse than its normalized counterpart.

ALSO TRUE
- Once data is federated or sharded, joins across databases are harder
  still, and denormalization can remove the need for them.
