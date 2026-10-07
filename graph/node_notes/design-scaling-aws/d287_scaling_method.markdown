REFERENCE: d287 Scaling Method
SOURCE: System Design Primer, "Design a system that scales to millions of users on AWS" https://github.com/donnemartin/system-design-primer/blob/master/solutions/system_design/scaling_aws/README.md

REQUIRED
- The method: benchmark or load test, profile for bottlenecks, address them
  while weighing alternatives and trade-offs, repeat.

ALSO TRUE
- Later stages: keep a limited period in MySQL and the rest in a data
  warehouse; SQL scaling patterns; NoSQL; queues and workers for work that
  need not be realtime.
