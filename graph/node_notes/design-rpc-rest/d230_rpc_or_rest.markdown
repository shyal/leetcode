REFERENCE: d230 RPC Or REST
SOURCE: System Design Primer, "Remote procedure call (RPC)" and "Representational state transfer (REST)" https://github.com/donnemartin/system-design-primer#remote-procedure-call-rpc

REQUIRED
- RPC exposes behaviours: the client causes a procedure to execute on a
  remote server, coded as if it were a local call. It is often used for
  internal communication, for performance.
- REST exposes data: the client acts on a set of resources managed by the
  server. It is often used for public HTTP APIs.
- All REST communication must be stateless and cacheable.
- RPC: POST /removeItem with the body {"itemid": "456"}. REST: DELETE
  /items/456.
- RPC, two disadvantages out of: clients become tightly coupled to the
  service implementation; a new API must be defined for every new operation;
  it can be difficult to debug; existing technology such as caching servers
  may not work out of the box.
- REST, two disadvantages out of: it fits badly when resources are not
  naturally a simple hierarchy; a few verbs do not fit every use case;
  nested resources need several round trips to render one view; payloads
  bloat as fields are added, since old clients receive all of them.

ALSO TRUE
- Being stateless, REST suits horizontal scaling and partitioning.
- Popular RPC frameworks: Protobuf, Thrift, Avro.
- GET, PUT and DELETE are idempotent; POST and PATCH are not.
