REFERENCE: d213 Scale Out
SOURCE: System Design Primer, "Horizontal scaling" https://github.com/donnemartin/system-design-primer#horizontal-scaling

REQUIRED
- Horizontal scaling, scaling out, adds more commodity machines; vertical
  scaling, scaling up, moves a single server to more expensive hardware.
- Scaling out on commodity machines is more cost efficient and gives higher
  availability than scaling up one server.
- The servers must be stateless: they hold no user-related data such as
  sessions or profile pictures.
- Sessions are stored in a centralised data store: a database, SQL or NoSQL,
  or a persistent cache such as Redis or Memcached.
- Downstream servers such as caches and databases must handle more
  simultaneous connections as the upstream servers scale out.

ALSO TRUE
- Scaling horizontally adds complexity and involves cloning servers.
