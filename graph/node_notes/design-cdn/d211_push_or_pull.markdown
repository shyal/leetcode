REFERENCE: d211 Push Or Pull
SOURCE: System Design Primer, "Content delivery network" https://github.com/donnemartin/system-design-primer#content-delivery-network

REQUIRED
- A CDN is a globally distributed network of proxy servers that serves
  content from locations closer to the user, generally static files.
- It improves performance because users receive content from data centers
  close to them, and because your servers do not serve the requests the CDN
  fulfils.
- Push: you upload content to the CDN whenever it is new or changed and
  rewrite URLs to point to the CDN. It minimises traffic and maximises
  storage.
- Push fits sites with little traffic or content that is not often updated.
- Pull: the CDN grabs content from your server when the first user requests
  it, so that first request is slower; a TTL sets how long it is cached. It
  minimises storage on the CDN but can create redundant traffic when files
  expire and are pulled again unchanged.
- Pull fits sites with heavy traffic.
- Two disadvantages out of: the cost can be significant depending on
  traffic; content can be stale if it is updated before the TTL expires;
  URLs for static content must be changed to point to the CDN.

ALSO TRUE
- The site's DNS resolution tells clients which CDN server to contact.
