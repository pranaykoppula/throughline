# The school's messages

A design case in the category **real-time messaging**. It draws on [time and ordering](../../design/time-and-ordering.md), [load balancing](../../design/load-balancing.md), [asynchronous work](../../design/async-work.md) and [partitioning](../../data/partitioning.md).

## The situation

A messaging app for schools connects teachers and parents. Every class has a group, and every school has one big group for announcements. Parents expect a teacher's message to appear within a second or two, in the same order for everyone, with ticks showing it was delivered and read; parents who aren't in the app get a notification on their phone. At 8 o'clock on a school morning, half the users open the app within the same twenty minutes. The first version had phones ask the server for new messages every three seconds, and on the first Monday of term the servers spent most of their time answering "nothing new".

## Requirements and numbers

- One-to-one chats, class groups of about 30, and school groups of up to 2,000.
- Messages appear for online members within about a second, in the same order for everyone in a group.
- Delivery and read receipts. Phone notifications for members who aren't connected.
- History kept for a year, and synced to a phone that's been offline for a week.
- About 5 million users, a million connected at once at the morning peak, and 200 million messages a day.

## The questions that matter

From [how to approach a design](../../design/approach.md):

- **What do we have?** Messages are small and written once, but each one goes to many people.
- **What breaks at ten times?** The number of open connections, and the work of delivering one message to 2,000 phones.
- **How does it fail?** Phones drop off and come back constantly. Nobody's clock can be trusted.

## The tempting first design

Phones poll: every few seconds, each asks "anything new since my last message?" Messages are stored with the time the sender's phone sent them, and shown in that order. A receipt is stored for every message and every reader.

At a million connected phones polling every three seconds, that's over 300,000 requests a second, nearly all with empty answers. Ordering by the sender's clock puts messages in different orders on different screens whenever phones' clocks disagree ([time and ordering](../../design/time-and-ordering.md)). And one message to a 2,000-member group creates 2,000 read receipts, each of which is itself a message.

## Hints

<details markdown="1"><summary>Hint 1</summary>

Instead of every phone asking constantly, what if the server could tell each phone the moment there was something new? What would it need to know about where each phone is connected?

</details>

<details markdown="1"><summary>Hint 2</summary>

Order needs one decider. For each conversation, what single place could hand out the next number?

</details>

<details markdown="1"><summary>Hint 3</summary>

A read receipt says "I've read everything up to here". How many numbers does that take per member per conversation?

</details>

## Two designs

<details markdown="1"><summary>Show the designs</summary>

### Rough numbers first

200 million messages a day is about 2,300 a second on average; the morning peak is perhaps ten times that, about 25,000 a second. With an average group of about 30, delivery is around 700,000 messages a second at the peak. A million open connections at perhaps 50,000 per gateway server is about twenty gateways, plus spares. Stored once per conversation, at about 300 bytes each, messages are about 60 gigabytes a day, or about 20 terabytes a year ([estimates](../../design/estimates.md)).

### Design A: connections, a sequence per conversation, store once

- **Gateways.** Each phone keeps one long-lived connection to a gateway server. A small, fast registry records which gateway each connected user is on. The load balancer spreads new connections, but a connection stays where it lands ([load balancing](../../design/load-balancing.md)).
- **One sequence per conversation.** Every conversation is owned by one partition of the message service, chosen by hashing the conversation's ID ([partitioning](../../data/partitioning.md)). The owner gives each new message the conversation's next number and stores it once. Everyone sees messages in number order, whatever any phone's clock says.
- **Client message IDs.** The phone makes an ID for each message before sending, so a send retried on a bad connection is recognised and stored once ([idempotency](../../design/idempotency.md)).
- **Fan-out through a queue.** After storing, the message is put on a queue. Workers look up which members are connected and pass it to their gateways; for members who aren't, they hand it to a notification service, which has its own rate limits from the phone platforms ([asynchronous work](../../design/async-work.md)).
- **Sync by number.** A phone that reconnects says "I have conversation 812 up to number 4,051", and gets everything after. Gaps are visible, so nothing is silently missed.
- **Receipts as positions.** Each member stores one number per conversation: "read up to 4,051". Delivery works the same way. In groups above about 100, the app shows how many have read a message, not who.

**What it costs:** stateful gateways that are harder to deploy (every restart disconnects thousands of phones, which must reconnect with random delays, or the reconnections arrive as a storm), and a sync step on every phone that reads many conversations.

### Design B: an inbox per user

Instead of storing each message once per conversation, the fan-out writes a copy, or a pointer, into each member's personal inbox, a single ordered log per user. A phone syncs one log, "everything in my inbox after position N", however many conversations it's in.

**What it gives:** much simpler syncing for the phone, and fast loading of the conversation list.

**What it costs:** a message to a 2,000-member group becomes 2,000 writes; edits and deletions must touch every copy. It suits one-to-one and small groups. Many real systems combine them: inboxes for small conversations, store-once for big groups.

</details>

## What breaks at ten times the size

- **The announcement group.** A message to every parent in a large school district is read by tens of thousands of people in the same minute; cache it, and send pointers, not copies.
- **Gateways.** Ten million connections need hundreds of gateways, and deploying them without reconnection storms needs gradual rollouts.
- **Notifications.** The phone platforms' own limits become the bottleneck; queue and prioritise notifications rather than send them all at once ([rate limiting](../../design/rate-limiting.md)).

## Where people slip

- **Ordering by the sender's clock.** Different screens, different orders.
- **A receipt per message per reader.** A number per reader per conversation does the same job.
- **No client message ID.** Retries on bad connections duplicate messages.
- **Treating "connected" as "online".** A connection can be dead for a minute before anyone notices; send heartbeats, and time out quietly dead connections ([timeouts](../../design/timeouts.md)).
- **Everyone reconnecting at once.** After a gateway restart, add random delays before reconnecting.

## Related

- The other case in this category: a document several people edit at once (coming in a later batch).
- Design pages: [time and ordering](../../design/time-and-ordering.md), [load balancing](../../design/load-balancing.md), [asynchronous work and message queues](../../design/async-work.md), [idempotency](../../design/idempotency.md), [rate limiting](../../design/rate-limiting.md).
- Other pages: [partitioning](../../data/partitioning.md), [append-only logs](../../dsa/append-only-logs.md), [queues](../../dsa/queues.md).
