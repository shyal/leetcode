REFERENCE: d251 Pastebin Expiry
SOURCE: System Design Primer, "Design Pastebin.com (or Bit.ly)" https://github.com/donnemartin/system-design-primer/blob/master/solutions/system_design/pastebin/README.md

REQUIRED
- Expiry: scan the SQL Database for entries whose expiration timestamp is
  older than now, and delete them or mark them expired.
