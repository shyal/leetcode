REFERENCE: d248 Pastebin Create
SOURCE: System Design Primer, "Design Pastebin.com (or Bit.ly)" https://github.com/donnemartin/system-design-primer/blob/master/solutions/system_design/pastebin/README.md

REQUIRED
- Create: the Client sends the request to the Web Server, a reverse proxy,
  which forwards it to the Write API server.
- The Write API generates a unique url, checking the SQL Database for a
  duplicate and generating another if it is taken; saves a row to the SQL
  pastes table; saves the paste data to the Object Store; returns the url.
- The SQL Database works as a large hash table from the shortlink to the path
  of the paste file; the contents live in an Object Store such as S3.
