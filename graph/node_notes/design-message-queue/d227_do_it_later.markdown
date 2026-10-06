REFERENCE: d227 Do It Later
SOURCE: System Design Primer, "Message queues" https://github.com/donnemartin/system-design-primer#message-queues

REQUIRED
- A message queue receives, holds and delivers messages.
- An application publishes a job to the queue, then notifies the user of the
  job's status.
- A worker picks up the job from the queue, processes it, then signals that
  the job is complete.
- The user is not blocked; the job is processed in the background.
- Redis is useful as a simple message broker, but messages can be lost.
- RabbitMQ is popular, but you must adapt to the AMQP protocol and manage
  your own nodes.
- Amazon SQS is hosted, but can have high latency and may deliver a message
  twice.
- Disadvantage: inexpensive calculations and realtime workflows are better
  done synchronously, since queues add delays and complexity.

ALSO TRUE
- A posted tweet can appear on your own timeline at once while delivery to
  followers takes longer.
- Task queues, such as Celery, receive tasks with their data, run them and
  deliver results, and support scheduling.
