REFERENCE: d245 One Box To Millions
SOURCE: System Design Primer, "Design a system that scales to millions of users on AWS" https://github.com/donnemartin/system-design-primer/blob/master/solutions/system_design/scaling_aws/README.md

REQUIRED
- 400 writes per second, 40,000 reads per second, 1 TB of new content per
  month.
- Start with a single box: a web server and a MySQL database. Scale it
  vertically, a bigger box. Drawbacks: vertical scaling can get very
  expensive, and there is no redundancy or failover.
- First moves: store static content separately in an Object Store such as
  S3, and move the MySQL database to its own box, so that the two scale
  independently.
- Web server bottleneck: horizontal scaling. Add a Load Balancer and several
  Web Servers across availability zones, and run MySQL in master-slave
  failover.
- Also separate the Web Servers from the Application Servers, and move
  static content to a CDN.
- Read-heavy database: move frequently accessed content and session data to
  a Memory Cache, which makes the Web Servers stateless, and add MySQL Read
  Replicas with logic that separates reads from writes.
- Autoscaling provisions capacity as needed, keeping up with traffic spikes
  and cutting cost by powering down unused instances. Disadvantage, one out
  of: it adds complexity; it can take some time before the system scales up
  or down to meet demand.
- The method: benchmark or load test, profile for bottlenecks, address them
  while weighing alternatives and trade-offs, repeat.

ALSO TRUE
- Later stages: keep a limited period in MySQL and the rest in a data
  warehouse; SQL scaling patterns; NoSQL; queues and workers for work that
  need not be realtime.
- Terminate SSL on the Load Balancer.
