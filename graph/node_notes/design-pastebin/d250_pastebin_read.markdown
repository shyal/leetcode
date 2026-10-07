REFERENCE: d250 Pastebin Read
SOURCE: System Design Primer, "Design Pastebin.com (or Bit.ly)" https://github.com/donnemartin/system-design-primer/blob/master/solutions/system_design/pastebin/README.md

REQUIRED
- Read: Client to Web Server to Read API server, which looks the url up in the
  SQL Database; if it is there, it fetches the contents from the Object Store;
  otherwise it returns an error.
