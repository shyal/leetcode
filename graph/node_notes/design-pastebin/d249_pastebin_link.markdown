REFERENCE: d249 Pastebin Link
SOURCE: System Design Primer, "Design Pastebin.com (or Bit.ly)" https://github.com/donnemartin/system-design-primer/blob/master/solutions/system_design/pastebin/README.md

REQUIRED
- The link: take the MD5 hash of the user's IP address plus a timestamp, Base
  62 encode it, keep the first 7 characters. 62^7 values cover the 360 million
  shortlinks of 3 years.

ALSO TRUE
- Base 62 encodes to [a-zA-Z0-9], which needs no escaping in a url; Base 64
  adds + and /.
