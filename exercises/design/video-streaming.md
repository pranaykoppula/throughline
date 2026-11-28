# The lecture that buffered

A design case in the category **large media**. It draws on [asynchronous work](../../design/async-work.md), [caching](../../performance/caching.md), [service boundaries](../../design/service-boundaries.md) and [storage tiers](../../economics/storage-tiers.md).

## The situation

An online-learning company lets teachers upload recorded lectures, and students watch them on phones, laptops and televisions, on everything from fibre to a weak mobile signal in a rural village. The first version stored each uploaded file as it was and streamed it straight from the company's servers. Lectures recorded on new cameras were too large for most phones; students on slow connections watched a spinning wheel; and in exam season, when a hundred thousand students watched the same revision lecture in the same evening, the servers' network links were full and the bill for data transfer was the largest line in the company's accounts.

## Requirements and numbers

- Teachers upload lectures of up to three hours, from unreliable connections.
- Lectures are watchable within half an hour of uploading.
- Playback starts within two seconds and adapts to the student's connection, without stalling.
- Popular lectures watched by tens of thousands at once; most lectures watched rarely after their first term.
- About 20,000 hours uploaded a month; about 2 million hours watched a day.

## The questions that matter

From [how to approach a design](../../design/approach.md):

- **Where does the data live, and where is it needed?** Uploaded once, in one place; watched many times, everywhere.
- **What's the bill?** For video, it's mostly moving bytes to viewers, and storing many copies.
- **How does it fail?** Uploads break halfway; a viewer's connection changes mid-lecture.

## The tempting first design

Upload the file in one request to a server, store it, and when a student presses play, send them the file from that server.

A three-hour upload over a café's connection fails near the end and starts again from nothing. A single file at the camera's quality is far too much for a phone on a mobile signal, so playback stalls. And every view, from every country, is served from the company's own servers, paying for every byte at the most expensive rate, while the same popular lecture crosses the same links a hundred thousand times.

## Hints

<details markdown="1"><summary>Hint 1</summary>

If an upload could be sent in pieces, each confirmed separately, what would a broken connection cost?

</details>

<details markdown="1"><summary>Hint 2</summary>

A viewer's connection can't be known in advance and changes while they watch. What would let the player switch quality halfway through without starting again?

</details>

<details markdown="1"><summary>Hint 3</summary>

A hundred thousand students watching the same lecture all want the same bytes. Where should those bytes be by the time they ask for them?

</details>

## Two designs

<details markdown="1"><summary>Show the designs</summary>

### Rough numbers first

2 million hours watched a day at an average of about 2 megabits a second is about 1.8 petabytes a day of data sent to viewers, about 20 gigabytes a second on average and more in the evening. Uploads are 20,000 hours a month; stored in five quality levels at an average of about 1.5 gigabytes an hour each, that's about 150 terabytes of new video a month. Delivery, not storage or processing, dominates the bill ([estimates](../../design/estimates.md), [reading a cloud bill](../../economics/cloud-bills.md)).

### Design A: chunked upload, a transcoding pipeline, and a CDN

- **Upload in chunks.** The teacher's browser splits the file into pieces of a few megabytes and uploads them directly to object storage, each confirmed separately and safe to resend, then marks the upload complete. A broken connection resends one chunk, not the whole file ([idempotency](../../design/idempotency.md)).
- **Transcoding as async work.** Completing an upload puts a job on a queue. Workers split the lecture into segments of a few seconds and encode each segment at several qualities, from a small one for weak mobile signals to full quality for televisions, in parallel across many machines. A failed segment is retried on its own; a file that can't be decoded goes to a dead-letter queue and the teacher is told ([asynchronous work](../../design/async-work.md)).
- **Adaptive playback.** The output is a set of short segments at each quality, and a playlist listing them. The player measures how fast segments arrive and chooses the quality of the next one accordingly, so a student moving from Wi-Fi to a mobile signal sees the picture soften rather than stop.
- **Delivery from the edge.** Segments are served through a content delivery network, with copies cached on servers close to viewers. The first student in a city fetches a segment from the origin; the next hundred thousand get it from a server down the road ([caching](../../performance/caching.md), [data gravity](../../data/data-gravity.md)).
- **Separate services, separate reasons.** Uploads, transcoding and playback are separate: transcoding needs bursts of computing power, playback needs to be close to viewers and almost never changes, and uploads need to be reliable over poor connections ([service boundaries](../../design/service-boundaries.md)).
- **Cold storage for old lectures.** After a term, rarely watched lectures move their lower qualities to cheaper, slower storage, and are re-encoded if someone asks ([storage tiers](../../economics/storage-tiers.md)).

**What it costs:** five or more copies of every lecture, a pipeline with several moving parts, and dependence on a CDN provider's prices.

### Design B: encode on demand

Store only the original and one standard version. Produce other qualities the first time someone asks for them, segment by segment, and cache the results.

**What it gives:** far less storage, and no work for lectures nobody watches. Most lectures in an archive are watched rarely.

**What it costs:** the first viewer of each quality waits for encoding, and a lecture that becomes suddenly popular causes a burst of encoding at the worst moment. A mix is common: encode popular qualities up front, the rest on demand.

</details>

## What breaks at ten times the size

- **Delivery cost.** At 18 petabytes a day, the CDN bill dominates everything; negotiate it, or place caching servers inside large internet providers' networks.
- **Live lectures.** Live streaming needs segments produced and delivered within seconds, so transcoding moves into the stream itself.
- **Long tail storage.** Old lectures accumulate; decide what to keep in which tier, and when to delete lower qualities that can be regenerated.

## Where people slip

- **Uploading in one piece.** Large uploads over real connections fail; chunk and resume.
- **One quality for everyone.** It's too much for phones and too little for televisions.
- **Serving from the origin.** Popular videos should never cross the origin's links more than a few times.
- **Transcoding inside the upload request.** It takes longer than any request should; hand it to workers.
- **Forgetting the bill.** For video, the cost is mostly moving bytes, and the design decides where they move from.

## Related

- The other case in this category: [the three laptops](file-sync.md), file sync across devices.
- Design pages: [asynchronous work and message queues](../../design/async-work.md), [service boundaries](../../design/service-boundaries.md), [idempotency](../../design/idempotency.md), [back-of-the-envelope estimates](../../design/estimates.md).
- Other pages: [caching](../../performance/caching.md), [storage tiers](../../economics/storage-tiers.md), [reading a cloud bill](../../economics/cloud-bills.md), [data gravity](../../data/data-gravity.md), [sampling](../../signals/sampling.md), [perception](../../signals/perception.md).
