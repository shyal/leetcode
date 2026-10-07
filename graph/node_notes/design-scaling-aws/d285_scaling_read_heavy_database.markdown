REFERENCE: d285 Scaling Read Heavy Database
SOURCE: System Design Primer, "Design a system that scales to millions of users on AWS" https://github.com/donnemartin/system-design-primer/blob/master/solutions/system_design/scaling_aws/README.md

REQUIRED
- Read-heavy database: move frequently accessed content and session data to a
  Memory Cache, which makes the Web Servers stateless, and add MySQL Read
  Replicas with logic that separates reads from writes.
