REFERENCE: d282 Scaling Single Box
SOURCE: System Design Primer, "Design a system that scales to millions of users on AWS" https://github.com/donnemartin/system-design-primer/blob/master/solutions/system_design/scaling_aws/README.md

REQUIRED
- Start with a single box: a web server and a MySQL database. Scale it
  vertically, a bigger box. Drawbacks: vertical scaling can get very
  expensive, and there is no redundancy or failover.
