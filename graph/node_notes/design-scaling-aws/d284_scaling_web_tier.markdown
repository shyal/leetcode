REFERENCE: d284 Scaling Web Tier
SOURCE: System Design Primer, "Design a system that scales to millions of users on AWS" https://github.com/donnemartin/system-design-primer/blob/master/solutions/system_design/scaling_aws/README.md

REQUIRED
- Web server bottleneck: horizontal scaling. Add a Load Balancer and several
  Web Servers across availability zones, and run MySQL in master-slave
  failover.

ALSO TRUE
- Also separate the Web Servers from the Application Servers, and move static
  content to a CDN.
- Terminate SSL on the Load Balancer.
