REFERENCE: d233 Four Steps
SOURCE: System Design Primer, "How to approach a system design interview question" https://github.com/donnemartin/system-design-primer#how-to-approach-a-system-design-interview-question

REQUIRED
- Step 1: outline use cases, constraints and assumptions.
- Five questions out of: who is going to use it; how are they going to use
  it; how many users are there; what does the system do; what are its inputs
  and outputs; how much data is expected; how many requests per second are
  expected; what is the expected read to write ratio.
- Step 2: create a high level design: sketch the main components and their
  connections, and justify the ideas.
- Step 3: design the core components: go into the details of each one.
- Step 4: scale the design: identify and address bottlenecks given the
  constraints, and discuss the trade-offs.

ALSO TRUE
- The interview is an open-ended conversation, and you are expected to lead
  it.
- Bottleneck answers to consider in step 4: load balancer, horizontal
  scaling, caching, database sharding.
