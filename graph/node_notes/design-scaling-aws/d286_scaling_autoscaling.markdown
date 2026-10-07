REFERENCE: d286 Scaling Autoscaling
SOURCE: System Design Primer, "Design a system that scales to millions of users on AWS" https://github.com/donnemartin/system-design-primer/blob/master/solutions/system_design/scaling_aws/README.md

REQUIRED
- Autoscaling provisions capacity as needed, keeping up with traffic spikes
  and cutting cost by powering down unused instances. Disadvantage, one out
  of: it adds complexity; it can take some time before the system scales up or
  down to meet demand.
