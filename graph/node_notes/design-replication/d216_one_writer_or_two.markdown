REFERENCE: d216 One Writer Or Two
SOURCE: System Design Primer, "Master-slave replication" and "Master-master replication" https://github.com/donnemartin/system-design-primer#master-slave-replication

REQUIRED
- Master-slave: the master serves reads and writes and replicates writes to
  one or more slaves, which serve only reads.
- If the master goes offline, the system continues in read-only mode until a
  slave is promoted to master or a new master is provisioned.
- Master-master: both masters serve reads and writes and coordinate with
  each other on writes. If either goes down, the system continues with both
  reads and writes.
- Particular to master-slave: additional logic is needed to promote a slave
  to a master.
- Particular to master-master, one out of: a load balancer or application
  logic must decide where to write; most such systems are either loosely
  consistent, violating ACID, or have higher write latency from
  synchronisation; conflict resolution matters more as write nodes are
  added.
- Shared, two out of: data can be lost if the master fails before new writes
  are replicated; many writes bog the read replicas down with replaying
  them; more read slaves means more to replicate and greater replication
  lag; replication adds hardware and complexity.

ALSO TRUE
- Slaves can replicate to further slaves in a tree.
