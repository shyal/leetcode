REFERENCE: d283 Scaling First Separation
SOURCE: System Design Primer, "Design a system that scales to millions of users on AWS" https://github.com/donnemartin/system-design-primer/blob/master/solutions/system_design/scaling_aws/README.md

REQUIRED
- First moves: store static content separately in an Object Store such as S3,
  and move the MySQL database to its own box, so that the two scale
  independently.
