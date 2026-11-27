# Every hour, on the hour

A design case in the category **coordination**. It draws on [consensus and leader election](../../design/consensus.md), [time and ordering](../../design/time-and-ordering.md), [heaps](../../dsa/heaps.md) and [idempotency](../../design/idempotency.md).

## The situation

A company runs a platform where customers schedule work: send this report every Monday at 9, retry this payment in three days, delete this account in thirty, run this cleanup every hour. Customers have scheduled about 50 million tasks between them. The first version was a single machine that checked a database table every minute for tasks that were due. When it was down for an hour, nothing ran; when the team added a second machine for safety, both of them ran every task; and at midnight on the first of each month, when a huge number of tasks fell due at the same moment, the run took two hours to clear.

## Requirements and numbers

- Run each task at its due time, within a few seconds, at least once, and almost never twice.
- Survive the loss of any machine without missing tasks.
- Handle one-off tasks (in thirty days) and recurring ones (every Monday at 9, in the customer's time zone).
- Handle peaks: a large share of recurring tasks fall due on round hours and especially at midnight.
- About 50 million scheduled tasks; on average 5,000 fall due a second, with peaks of over 500,000 in the first second after midnight on the first of the month.

## The questions that matter

From [how to approach a design](../../design/approach.md):

- **What must always work?** Every task runs; no task runs twice when it matters.
- **What's the peak?** The round hours, which people choose far more than any other time.
- **How does it fail?** A scheduler machine dies, or pauses, while holding tasks that are due.

## The tempting first design

A table of tasks with a due time. Every minute, a scheduler selects all tasks due before now, runs each, and updates its next due time. A second scheduler runs the same loop for safety.

Scanning a table of 50 million rows every minute is slow, and a minute's granularity misses the "within a few seconds" requirement. Two schedulers both select the same due tasks and both run them. And at midnight, half a million tasks due in the same second all start at once, on the same machines.

## Hints

<details markdown="1"><summary>Hint 1</summary>

Which structure always knows the next thing that's due, without scanning everything? How could the 50 million tasks be split so that each piece fits in one machine's version of it?

</details>

<details markdown="1"><summary>Hint 2</summary>

Each piece of the schedule needs exactly one machine running it at a time. What happens if that machine pauses and another takes over, and how would the first be stopped from running tasks when it wakes?

</details>

<details markdown="1"><summary>Hint 3</summary>

Half a million tasks due at exactly midnight don't all have to start in the same second. What would you change about when they run, and what would you tell customers?

</details>

## Two designs

<details markdown="1"><summary>Show the designs</summary>

### Rough numbers first

50 million tasks at a few hundred bytes each is about 15 gigabytes: too much for one machine to handle safely, fine split across a few dozen. 5,000 due a second on average is easy; 500,000 in one second is not, and it's created by people choosing round numbers, so the design should both absorb it and soften it ([estimates](../../design/estimates.md)).

### Design A: partitioned schedules, one owner each, idempotent execution

- **Partitions.** Tasks are split into, say, 256 partitions by hashing the task's ID, and stored durably ([partitioning](../../data/partitioning.md)). Each partition is owned by exactly one scheduler process at a time.
- **Ownership by lease, with fencing.** Owners hold leases on their partitions from a coordination service built on consensus. Each lease carries an increasing number, and every action an owner takes, such as marking a task as started, carries that number; storage refuses actions with an old one. A paused owner that wakes after its lease has moved on can't run anything ([consensus and leader election](../../design/consensus.md)).
- **A heap of what's next.** Each owner keeps the tasks of its partition that fall due in the next hour in a [heap](../../dsa/heaps.md), or a timing wheel, ordered by due time, loaded from storage in the background. It sleeps until the top of the heap is due, so no scanning.
- **Hand off, don't run.** When a task is due, the owner writes "started, attempt 1" and puts it on a queue for workers, then computes the next due time for recurring tasks in the customer's time zone and stores it ([asynchronous work](../../design/async-work.md)).
- **At least once, made safe.** Workers acknowledge tasks when done. If a worker dies, the task is retried, so tasks run at least once, and each run carries an execution ID made from the task and its due time, so the customer's system can ignore a repeat ([idempotency](../../design/idempotency.md)).
- **Spread the peaks.** Recurring tasks scheduled "at midnight" get a fixed, random offset of a few seconds or minutes, chosen once per task, and the documentation says so. The queue absorbs what's left ([rate limiting](../../design/rate-limiting.md)).
- **Time zones.** Due times are stored in UTC and computed from the customer's time zone for each occurrence, so that "9 o'clock every Monday" stays at 9 through daylight-saving changes, and the ambiguous hours are handled by a written rule ([time and ordering](../../design/time-and-ordering.md)).

**What it costs:** a coordination service, partitions to rebalance as the scheduler fleet changes, and execution that's at least once rather than exactly once.

### Design B: a database as the scheduler

Keep tasks in a database table indexed by due time. Many workers repeatedly claim a batch of due tasks with a single statement that selects and locks rows that aren't already locked, and mark them started in the same transaction.

**What it gives:** no separate coordination service, no leases, and the database's own locking ensures each task is claimed once. It's simple, and it's how many smaller systems do it.

**What it costs:** polling load on the database, and a ceiling set by how many claims a second one database can handle. It's a good design up to a few thousand tasks a second, and Design A is what it grows into.

</details>

## What breaks at ten times the size

- **Rebalancing.** Adding scheduler machines moves partitions; the hand-over must keep fencing, or a task runs twice during the move.
- **Tasks far in the future.** Hundreds of millions of tasks due next year needn't be in memory; load each hour's tasks shortly before it starts.
- **Downstream systems.** Running a customer's half-million midnight tasks on time may overwhelm the customer's own systems; let customers set their own rate.

## Where people slip

- **Two schedulers for safety, without fencing.** Every task runs twice.
- **Scanning the whole table.** Keep what's due soon in a structure that knows the next one.
- **Promising exactly once.** Promise at least once, and give each run an identity so repeats can be ignored.
- **Storing local times.** Daylight saving moves them; store UTC and recompute.
- **Everyone at midnight.** Spread recurring tasks, or the round hours set the size of the whole system.

## Related

- The other case in this category: [a hundred requests a minute, across forty servers](shared-rate-limiter.md), a shared rate limiter.
- Design pages: [consensus and leader election](../../design/consensus.md), [time and ordering](../../design/time-and-ordering.md), [idempotency](../../design/idempotency.md), [asynchronous work](../../design/async-work.md), [rate limiting](../../design/rate-limiting.md).
- Other pages: [heaps](../../dsa/heaps.md), [partitioning](../../data/partitioning.md), [queues](../../dsa/queues.md), [2, One machine, many programs](../../02-one-machine-many-programs.md), where a scheduler first decided who runs next.
