REFERENCE: d257 Twitter Memory Bounds
SOURCE: System Design Primer, "Design the Twitter timeline and search" https://github.com/donnemartin/system-design-primer/blob/master/solutions/system_design/twitter/README.md

REQUIRED
- Two memory bounds out of: keep only several hundred tweets per home timeline
  in the cache; keep only active users' home timelines and rebuild the others
  from the SQL Database; store only a month of tweets in the Tweet Info
  Service; store only active users in the User Info Service.
