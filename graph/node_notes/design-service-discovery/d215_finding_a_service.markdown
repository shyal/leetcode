REFERENCE: d215 Finding A Service
SOURCE: System Design Primer, "Application layer" https://github.com/donnemartin/system-design-primer#application-layer

REQUIRED
- Separating the web layer from the application layer lets you scale and
  configure the two independently; a new API adds application servers
  without necessarily adding web servers.
- Microservices are a suite of independently deployable, small, modular
  services; each runs a unique process and communicates through a
  well-defined, lightweight mechanism.
- A service discovery system keeps track of registered names, addresses and
  ports so that services can find each other. Consul, Etcd and Zookeeper are
  such systems.
- Health checks verify service integrity, often through an HTTP endpoint.
- One disadvantage out of: loosely coupled services need a different
  approach to architecture, operations and process than a monolith;
  microservices add complexity in deployments and operations.

ALSO TRUE
- Workers in the application layer also enable asynchronism.
- Consul and Etcd have a built-in key-value store, useful for config values
  and other shared data.
