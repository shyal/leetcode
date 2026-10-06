DRILL: One Box To Millions
TRAINS: design-scaling-aws

Design a system that grows from one user to 10 million. Assume relational
data, 1 billion writes and 100 billion reads per month, and 1 KB per write.
Write: (1) writes per second, reads per second and new content per month;
(2) the starting setup, the first way it is scaled, and two drawbacks of
that way; (3) the first two things moved off the single box; (4) what is
added when the web server bottlenecks at peak hours; (5) what is added when
the database suffers under reads at 100:1; (6) what autoscaling does and one
disadvantage; (7) the method repeated at every stage.

REQUIRED: three numbers, the single box scaled vertically with its
drawbacks, the object store and the separate database, the load balancer
with several web servers and master-slave failover, the cache and read
replicas, autoscaling, the benchmark and profile loop. Jumping to the final
design in one step is the fail.

## Answer
