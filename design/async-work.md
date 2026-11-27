# Asynchronous work and message queues

Last reviewed: 2026-11-27

A concept page: separating asking for work from doing it. A message queue lets a caller hand off a job and move on, which makes the system faster and steadier. It also means each job will sometimes arrive twice, arrive late, or never succeed, and the design has to say what happens then.

## Problem

Some work takes too long to do while someone waits: resizing images, sending emails, generating reports, calling a slow partner. Doing it inside the request makes every request as slow as its slowest job, and a burst of jobs becomes a burst of timeouts. Putting the job on a queue for workers to pick up later lets the request return at once and lets the work proceed at its own pace. But "later" moves the job out of anyone's sight, and work nobody is watching fails in ways nobody notices until much later.

## The story

In 2017 Siobhán Kelly ran the back end of a property-listings site in Dublin. Estate agents uploaded photographs of each house, and the site made six sizes of each one, from a thumbnail to a full-screen view. At first the resizing happened inside the upload: the agent's browser waited while the server made all six. That took about eight seconds a photo, and an agent uploading forty photos of a large house often hit the thirty-second limit and had to start again.

So Siobhán moved the resizing out of the request. The upload stored the original, put a message on a queue saying *resize photo 81233*, and answered straight away. A pool of worker machines took messages off the queue, did the resizing, and deleted each message once it was done. If a worker died halfway, the queue made the message visible again after a few minutes, and another worker picked it up. Uploads became instant, the workers kept up easily, and in a busy week the queue simply got longer for an hour and then caught up. It was the textbook move, and it was right.

Eight months later an agent uploaded a photograph saved in an unusual format, from an old scanner. The image library crashed on it, taking the worker process down. The message reappeared a few minutes later, a second worker picked it up, and crashed too. Then a third. Within the hour every worker was crashing on the same photo, being restarted, taking a message, and some of them took that one again. Meanwhile about 40,000 other photos waited behind them, and new listings went up with grey squares where the pictures should have been. The queue's length looked alarming but not unusual for a busy morning, so nobody was woken until agents started phoning.

When Siobhán looked closer, she found a second, quieter problem. Some large photos took longer to resize than the time before their message reappeared, so a second worker started the same job while the first was still on it. Every listing that had been through it had its pictures made twice. Nothing had broken only because making the same picture twice happened to be harmless.

*Before reading on: the queue had done exactly what it promised, and every message eventually reappeared. What should happen to a message that will never succeed?*

Siobhán saw that the queue's promise was *at least once*, and she had built as if it were *once*. At least once meant two things her design ignored. A message might be delivered again even after it had been processed, so processing had to be safe to repeat. And a message that failed would be delivered again forever, so something had to decide when to stop.

She kept the queue and the workers. Each message now carried a count of how many times it had been tried, and after five failures it was moved to a separate **dead-letter queue**, where it waited for a person instead of a worker, and an alert said so. The workers were made explicitly idempotent: each resized image was saved under a name made from the photo's number and the size, so doing a job twice wrote the same files again. A worker on a slow job now extended its message's invisibility while it worked. And she stopped watching the queue's length and started watching the age of its oldest message, which said how long the unluckiest job had been waiting: ten minutes on a busy day, never two hours.

![A line chart of the age of the oldest waiting photo during the morning of the bad photo. Without a retry limit, every worker crashes on the same photo in turn and the oldest age climbs steadily to about two hours. With a limit of five tries and a dead-letter queue, the bad photo is set aside after about twenty minutes and the oldest age falls back to a few minutes.](../images/figures/design-async-work.svg)

*A queue promises to deliver every message at least once. Something else has to decide what happens to the one that never succeeds.*

Looking back, Siobhán thought the queue had made her system faster and her failures quieter. Work that used to fail in front of an agent now failed out of sight, and the design hadn't said who would look. The dead-letter queue, the idempotent workers and the oldest-message alarm were all the same answer: decide, in advance, what happens to the work nobody is watching.

## Where it shows up

| Page | The work handed off | What it taught |
| --- | --- | --- |
| [2, One machine, many programs](../02-one-machine-many-programs.md) | Ruth's jobs, queued for the processor overnight | Handing work to a queue lets the machine stay busy, and the people stop waiting on it, at the price of answers arriving later. |
| [Queues](../dsa/queues.md) | Yusuf's email, one line or three | A queue also decides who goes next; one big sender can hold up everyone else. |
| [Idempotency](idempotency.md) | Valeria's retried charges | At-least-once delivery means every job must be safe to repeat. |
| [Timeouts and circuit breakers](timeouts.md) | Ji-woo's waiting threads | The time before a message reappears is a timeout, and it has to be longer than the slowest real job. |
| [Rate limiting and backpressure](rate-limiting.md) | Farida's flooded database | A queue absorbs a burst, but one that's allowed to grow forever only hides an overload. |
| [Event loops and threads](../languages/event-loops-and-threads.md) | Omar's two ways of sharing time | The same move inside one program: start the slow work, do something else, come back for the result. |

It shows up elsewhere too: a restaurant's order tickets on the rail between the waiters and the kitchen, the post, a dry cleaner's numbered ticket, and the in-tray on a desk, with the pile of letters nobody can deal with set aside in a folder of its own.

What the rows share is the trade at the heart of handing work off. The person asking stops waiting, and the work stops being watched. Every queue needs a rule for repeats, a rule for work that will never succeed, and a measure of how long the oldest job has waited.

## It really happened

Siobhán is fictional, and so is her site. Queues between programs are much older than the web: IBM's MQSeries, from 1993, carried messages between banks' and airlines' systems, and Amazon's Simple Queue Service opened to the public in 2004, before almost anything else Amazon now rents. Dead-letter queues are a standard feature. In SQS, a *redrive policy* sets how many times a message may be received before it's moved to a dead-letter queue, where it can be examined and, once the problem is fixed, sent back ([Amazon SQS documentation](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-dead-letter-queues.html)). The documentation warns against setting the limit to 1, because a single ordinary failure would then send a message straight to the dead-letter queue.

The promise Siobhán missed is stated plainly by most queue services: standard queues deliver each message at least once, and occasionally more than once, so consumers are expected to be idempotent. Amazon's own guidance on retries makes the same point about any call with side effects ([Amazon Builders' Library, "Timeouts, retries, and backoff with jitter"](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/) <!-- verify -->).

## What it is

A **message queue** stores messages from producers until consumers take them. Most queues give **at-least-once** delivery: a consumer receives a message, it becomes invisible to others for a **visibility timeout**, and it's deleted only when the consumer says it's done; if the consumer fails or takes too long, the message reappears. Consumers must therefore be idempotent. A **dead-letter queue** receives messages that have failed a set number of times, so one bad message can't block the work or loop forever. Some queues preserve order, usually within a key or partition, at a cost in throughput; most don't. The health of a queue is best measured by the **age of the oldest message**, which shows how long work is actually waiting, rather than by its length, which depends on how busy the day is. Queues are used for background work, for smoothing bursts, and for decoupling services so that one can be down while the other keeps accepting work.

## Where it gets misapplied

- **Assuming each message arrives once.** It will sometimes arrive twice; make processing safe to repeat.
- **No limit on retries.** One message that can never succeed occupies the workers forever.
- **Watching the queue's length.** A long queue on a busy day is normal; an old message is the alarm.
- **A visibility timeout shorter than the slowest job.** The job is started again while it's still running.
- **Queuing work the user is waiting for.** If the answer is needed now, a queue only adds delay and a place to lose it.
- **The mirror:** doing everything synchronously because queues are complicated. Slow work inside a request makes every user wait for it and every burst a failure.

## Connections

- Learning this is also learning [queues](../dsa/queues.md), because a message queue is the same structure, with the added question of who goes next.
- Learning this is also learning [idempotency](idempotency.md), because at-least-once delivery is only safe when repeating a job does no harm.
- Learning this is also learning [timeouts and circuit breakers](timeouts.md), because the visibility timeout decides when a job is presumed lost.
- Learning this is also learning [queueing](../performance/queueing.md), because a queue near capacity grows without limit, however patient its consumers.
- Learning this is also learning [event loops and threads](../languages/event-loops-and-threads.md), because asynchronous work inside one program is the same idea at a smaller scale.
- Learning this is also learning [batch or stream](batch-or-stream.md), because a queue of jobs is a stream, and draining it overnight is a batch.

## Resources

1. Amazon SQS documentation, ["Using dead-letter queues"](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-dead-letter-queues.html) (start here: the mechanics, and the warnings).
2. Gregor Hohpe and Bobby Woolf, *Enterprise Integration Patterns* (2003) (go deeper: the vocabulary of messaging, including the dead letter channel).
3. Martin Kleppmann, *Designing Data-Intensive Applications*, chapter 11 (reference: message brokers and logs compared).

## Names you'll hear

- **Producer, consumer, broker:** who sends, who processes, and what holds the messages between them.
- **At-least-once, at-most-once delivery:** delivered possibly twice, or possibly never.
- **Visibility timeout, acknowledgement:** how long a taken message stays hidden, and the consumer saying it's done.
- **Dead-letter queue, redrive:** where repeatedly failing messages go, and sending them back once fixed.
- **Poison message:** one that fails every time it's processed.
- **Oldest message age, consumer lag:** how long work has been waiting.
- **SQS, RabbitMQ, Kafka:** a queue service, a broker, and a log often used like one.

## Go and look

Find a queue in something you run and find three numbers: the age of its oldest message right now, how many times a message may be retried, and where it goes after that. If any of them is unknown, that's the place a bad message will hide.

Practise this: [the school's messages](../exercises/design/group-chat.md), where every message fans out through a queue.
