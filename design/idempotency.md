# Idempotency

Last reviewed: 2026-11-27

A concept page: making an operation safe to repeat, so that doing it twice has the same effect as doing it once. Across a network you often can't tell whether a request worked, and the only safe way to find out is to ask again.

## Problem

When a request times out, there are three possibilities: it never arrived, it arrived and failed, or it arrived, worked, and the reply was lost. The caller can't tell which. Not retrying loses work that should have happened; retrying repeats work that already did. For reading data, repeating is harmless. For charging a card, sending an email or shipping a parcel, it isn't. The way out is to change the operation, so that repeating it is harmless too, and then retry freely.

## The story

In 2015 Valeria Ocampo built the payments for a food-delivery app in Bogotá. When a customer pressed *Pay*, the app's server asked a payment provider to charge the card, waited up to ten seconds, and, if no answer came, tried again, up to three times. Valeria had watched the logs: almost every timeout was a request lost on a flaky mobile network or a congested link, and the second try went straight through. Retrying turned lost orders into completed ones. It was the right call, and it kept the app's failure rate low for most of a year.

Then, one rainy Friday evening, the payment provider slowed down. Charges still went through, but the replies took twelve or fifteen seconds to come back. Valeria's server gave up at ten, assumed the charge had failed, and asked again. The second charge went through too, slowly, and sometimes so did the third. By the time the provider recovered, about 1,900 customers had paid two or three times for one dinner. The refunds took a week, and the support team spent the weekend apologising.

*Before reading on: retrying was meant to make payments more reliable. What did the server need to know that a timeout couldn't tell it?*

Valeria saw that a timeout carried no information about what had happened on the other side. Her server had treated "no answer" as "no charge", and that was a guess. She couldn't make the network tell her more, so she changed the question instead. Each payment attempt now got a unique key, made from the order number, before the first request was sent. Every retry carried the same key. The provider, which supported such keys, remembered each one for a day: the first request with a key did the work and stored its result, and any later request with the same key got the stored result back without charging again. The server could now retry as often as it liked. A charge that had succeeded before the reply was lost was simply reported again.

The same trouble was waiting one step earlier. The phone app also retried when the connection dropped, and a few customers had already received two identical orders. So the app made its own key when the customer first pressed *Pay*, and the server kept a table of keys it had seen: a second "place order" with a known key returned the order already created. She kept every retry she'd had before. What changed was that repeating a request was now harmless, so retrying was safe all the way down.

![Two timelines between the app's server and the payment provider. Top, without a key: the first charge succeeds but its reply is lost, the server times out after ten seconds and retries, and the provider charges the card a second time. Bottom, with an idempotency key: the retry carries the same key, the provider recognises it, and returns the first charge's result without charging again.](../images/figures/design-idempotency.svg)

*A timeout can't say whether the work happened. A key lets the other side say it for you.*

Looking back, Valeria thought the retries had been right and incomplete. A retry asks a question twice; idempotency is what makes the second asking safe. She'd needed both, and she'd built the easy half first.

## Where it shows up

| Page | The repeated work | What made it safe |
| --- | --- | --- |
| [5, Machines need to talk](../05-machines-need-to-talk.md) | Lin's resent blocks | Numbering every block let the other end recognise a duplicate and discard it, which is idempotency built into a protocol. |
| [Append-only logs](../dsa/append-only-logs.md) | Teresa's ledger, replayed to rebuild a balance | Each entry has its own identity, so applying the log again, or reading it twice, can't count a payment twice. |
| [Replication](../data/replication.md) | A replica applying changes it may already have | Changes are applied in order by position in the log, so a replica that reconnects knows where it got to. |
| [Rate limiting and backpressure](rate-limiting.md) | Clients retrying after a refusal | Retrying with backoff is safe only if the request can be repeated. |
| [Timeouts and circuit breakers](timeouts.md) | Any call that gave up waiting | A timeout leaves the outcome unknown; idempotency is what lets the caller find out by trying again. |

It shows up elsewhere too: a lift button that does nothing more when pressed a fourth time, a light switch marked "on" rather than a pull-cord that toggles, a cheque with a number so the bank pays it once, and a parcel's tracking number, which lets a courier ignore a second booking for the same delivery.

What the rows share is that a repeat can't be prevented, only recognised. Give each piece of work an identity that travels with it, and keep a record of what's been done, and the second attempt becomes a question with a known answer instead of new work.

## It really happened

Valeria is fictional, and so is her app. Idempotency keys are standard in payments. In 2017 Stripe described how its API accepts an `Idempotency-Key` header on every request that changes something: the first request with a key does the work, and a retry with the same key gets the saved result. Its own client libraries retry automatically with a key, with increasing delays and randomness ([Stripe, "Designing robust and predictable APIs with idempotency"](https://stripe.com/blog/idempotency)). Amazon's guide to timeouts and retries makes the same point from the other side: APIs with side effects aren't safe to retry unless they provide idempotency, and some, such as the call that starts EC2 instances, take a client token for exactly that reason ([Amazon Builders' Library, "Timeouts, retries, and backoff with jitter"](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/)).

The idea is older than payments APIs. HTTP has always distinguished methods that are meant to be safe to repeat, such as GET, PUT and DELETE, from POST, which isn't; the current definition is in [RFC 9110](https://www.rfc-editor.org/rfc/rfc9110#name-idempotent-methods), section 9.2.2. The word itself comes from mathematics, where an idempotent function gives the same result applied once or many times.

## What it is

An operation is idempotent if performing it more than once has the same effect as performing it once. Some operations are naturally idempotent: "set the balance to 100", "delete order 42", "mark as read". Others, such as "add 10 to the balance" or "send an email", aren't, and are made safe to repeat with an **idempotency key**: a unique identifier for the intended operation, created by the caller before the first attempt and sent with every retry. The receiver records each key with its result, atomically with doing the work, and answers repeats from the record. Keys need a lifetime, and a request that reuses a key with different contents should be rejected. Together, retries and idempotency give the effect people mean by "exactly once": the message may be delivered several times, but its effect happens once.

## Where it gets misapplied

- **Retrying without it.** The double charge, the duplicate order, the second email.
- **A key made on the server.** If the server creates the key after receiving the request, a retry of a lost request gets a new key. The caller must make it, before the first attempt.
- **Recording the key separately from the work.** If the work commits and the record of the key doesn't, or the other way round, a crash in between brings the duplicate back. Store both in one transaction.
- **Claiming "exactly once delivery".** Networks can't promise it. What can be promised is that repeated delivery has no extra effect.
- **The mirror:** keys on everything. Reads, and operations that already set a value rather than change it, are idempotent by nature, and wrapping them adds storage and complexity for nothing.

## Connections

- Learning this is also learning [timeouts and circuit breakers](timeouts.md), because a timeout is exactly the moment the outcome becomes unknown.
- Learning this is also learning [append-only logs](../dsa/append-only-logs.md), because a log of what's been done, with an identity for each entry, is how a repeat is recognised.
- Learning this is also learning [sagas](sagas.md), because each step and each compensation in a long operation may be retried, and all of them must be safe to repeat.
- Learning this is also learning [rate limiting and backpressure](rate-limiting.md), because clients told to retry later can only do so safely if the request can be repeated.
- Learning this is also learning [replication](../data/replication.md), because a replica that reconnects has to apply each change once, whatever it has already seen.

## Resources

1. Stripe, ["Designing robust and predictable APIs with idempotency"](https://stripe.com/blog/idempotency) (2017) (start here: keys, retries and backoff together).
2. Brandur Leach, ["Implementing Stripe-like Idempotency Keys in Postgres"](https://brandur.org/idempotency-keys) (go deeper: storing keys and results atomically, step by step).
3. Pat Helland, "Idempotence Is Not a Medical Condition", *ACM Queue* (2012) (reference: why messages are repeated, and what to do about it).

## Names you'll hear

- **Idempotent:** the same effect however many times it's repeated.
- **Idempotency key, request ID, client token:** an identity for an operation, made by the caller.
- **At-most-once, at-least-once, exactly-once:** what's promised about delivery; the third is really at-least-once plus idempotency.
- **Deduplication:** recognising and dropping a repeat.
- **Two Generals problem:** the proof that two parties communicating over an unreliable channel can never be sure they agree.

## Go and look

Find the call in something you've built that charges, sends or creates something, and find what happens when it times out. If the code retries, check whether the other side would recognise the retry. If it doesn't retry, find out how many operations are being lost.

Practise this: [the tutors' wages](../exercises/design/payments-ledger.md), a payments ledger, and [every click, once](../exercises/design/ad-click-counter.md), an ad-click counter that bills.
