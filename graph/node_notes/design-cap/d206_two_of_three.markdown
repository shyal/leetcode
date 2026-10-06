REFERENCE: d206 Two Of Three
SOURCE: System Design Primer, "CAP theorem" https://github.com/donnemartin/system-design-primer#cap-theorem

REQUIRED
- Consistency: every read receives the most recent write or an error.
- Availability: every request receives a response, with no guarantee that it
  holds the most recent write.
- Partition tolerance: the system continues to operate despite arbitrary
  partitioning due to network failures.
- Networks are not reliable, so partition tolerance must be supported; the
  trade is between consistency and availability.
- CP: a request that waits on the partitioned node may end in a timeout
  error. It fits a business that needs atomic reads and writes.
- AP: a response returns the most readily available version on any node,
  which may not be the latest, and writes take time to propagate once the
  partition is resolved. It fits a business that allows eventual consistency
  or must keep working despite external errors.
