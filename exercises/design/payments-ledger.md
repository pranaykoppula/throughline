# The tutors' wages

A design case in the category **money that must be exact**. It draws on [idempotency](../../design/idempotency.md), [sagas](../../design/sagas.md), [append-only logs](../../dsa/append-only-logs.md) and [timeouts](../../design/timeouts.md).

## The situation

An online marketplace connects students with private tutors. A student pays for a lesson by card; the platform keeps 15% and owes the tutor the rest, paid out to their bank account every Friday. Students sometimes cancel and are refunded, and sometimes dispute a charge with their bank weeks later. The company's first version kept a balance for each tutor and updated it as payments came in. Last month a tutor showed that she'd been paid for nine lessons when she'd taught eleven, and nobody could work out from the database where the other two had gone. The finance team now spends three days at the end of every month matching the platform's numbers against the card provider's and the bank's.

## Requirements and numbers

- Take card payments, issue refunds, record disputes, and pay tutors weekly.
- Never lose a payment or count one twice. Every balance must be explainable, entry by entry.
- Match every movement of money against the card provider's and the bank's reports each day.
- Show tutors their current balance and history quickly.
- About 2 million payments a month, with a peak of about 200 a second on Sunday evenings in exam season. Around 200,000 tutors.

## The questions that matter

From [how to approach a design](../../design/approach.md), the ones this case turns on:

- **What must always work?** Money in equals money out plus what's held, at every moment, and anyone can see why.
- **What breaks at ten times the size?** Probably not the database. The harder limits are correctness under retries, crashes and concurrent updates.
- **How does it fail?** The card provider is slow sometimes. A timeout doesn't say whether a charge happened.

## The tempting first design

A `balance` column for each tutor and each student. When a payment succeeds, call the card provider, then add the tutor's share to their balance and the fee to the platform's. A refund subtracts. Payouts read the balance, send it to the bank, and set it to zero.

It's what the company built, and it fails in four ways. A retry after a timeout charges the card twice and adds the money twice. A crash between charging the card and updating the balance loses the payment. Two updates to the same balance at the same moment can overwrite each other. And a balance that's been changed in place can't explain itself: the two missing lessons left no trace.

## Hints

<details markdown="1"><summary>Hint 1</summary>

What record would let you explain any balance, at any moment in the past, to a tutor or an auditor? Accountants have had an answer for six centuries.

</details>

<details markdown="1"><summary>Hint 2</summary>

The process can die at any point between deciding to charge a card and recording that it did. What would let a restarted process find out what happened, and finish the job without doing it twice?

</details>

<details markdown="1"><summary>Hint 3</summary>

A payout is three steps across systems you don't control: reserve the tutor's money, send it to the bank, record that it left. Which of those can be undone, and what happens if the bank rejects the transfer on Monday?

</details>

## Two designs

<details markdown="1"><summary>Show the designs</summary>

### Rough numbers first

Two million payments a month is under one a second on average, and the peak is 200 a second. Each payment writes three or four ledger entries, so about 10 million entries a month, or about 120 million a year. At a couple of hundred bytes each, that's about 25 gigabytes a year. One well-run relational database holds this for many years. This is a correctness problem, not a scale problem ([estimates](../../design/estimates.md)).

### Design A: a double-entry ledger in one database

- **Accounts and entries.** Every holder of money is an account: each student's card payments, each tutor's earnings, the platform's fees, money in transit at the card provider, money in transit to banks. Every movement is a **transaction** of two or more **entries** that sum to zero: a £40 lesson is −£40 from the card-clearing account, +£34 to the tutor and +£6 to fees. Entries are only ever added. A refund or a correction is a new transaction that reverses the old one ([append-only logs](../../dsa/append-only-logs.md)).
- **Balances are derived.** A balance is the sum of an account's entries. For speed, each account keeps a cached balance updated in the same database transaction as its entries, so the two can't disagree, and the cache can always be rebuilt from the entries.
- **Payments as a state machine with a key.** Before calling the card provider, the platform writes a payment record in state `pending`, with an idempotency key made from the booking. It calls the provider with that key. When the answer comes, it writes the entries and moves the payment to `succeeded` or `failed`, in one transaction. On a timeout it asks again with the same key, which can't charge twice ([idempotency](../../design/idempotency.md), [state machines](../../dsa/state-machines.md)). A job sweeps up payments left `pending` too long and asks the provider what happened.
- **Payouts as a saga.** On Friday, each tutor's balance is moved into an "in transit to bank" account (cheap to undo), then the bank transfer is requested with its own key, then the entries are settled when the bank confirms. If the bank rejects the transfer, a reversing transaction moves the money back to the tutor's account, and they're told why ([sagas](../../design/sagas.md)).
- **Daily reconciliation.** A job reads the card provider's and the bank's reports and matches every line to a ledger transaction. Anything unmatched on either side is a ticket for a person. This is what turns three days of month-end work into a short daily list.

**What it costs:** more tables and more rows than a balance column, and every change written as a transaction. The cached balances of very busy accounts, such as the platform's fee account, are touched by every payment and become a point of contention (see below).

### Design B: an event log with ledger views

Every payment event (requested, succeeded, refunded, disputed, paid out) is written to a durable, partitioned log. A ledger service reads the log and writes entries; separate services build tutors' balances, the finance team's reports and the reconciliation from the same log, each as its own view.

**What it gives:** services that scale and deploy separately, and the ability to replay history to build a new report or fix a bug in an old one.

**What it costs:** many more moving parts, views that lag behind the log by seconds, and the need for every consumer to be idempotent, since the log delivers at least once ([asynchronous work](../../design/async-work.md)). At this company's size, Design A does everything needed in one place; B is worth it when the volume or the number of teams outgrows one database.

</details>

## What breaks at ten times the size

- **Hot accounts.** At 2,000 payments a second, every one updating the platform's single fee account serialises on one row. Split it into several sub-accounts chosen at random and sum them for reports, or don't keep a cached balance for it at all.
- **Reconciliation.** Matching ten times as many lines needs to run continuously rather than once a day.
- **Currencies and countries.** Each currency needs its own accounts and the conversions recorded as transactions, never as a rate applied later.

## Where people slip

- **Floating-point money.** Store amounts as whole numbers of the smallest unit, such as pence ([floating point](../../math/floating-point.md)).
- **Balances updated in place.** They can't explain themselves, and concurrent updates lose money.
- **Treating a timeout as a failure.** The charge may have happened. Ask again with the same key.
- **Deleting or editing entries.** Corrections are new, reversing entries, so the history stays true.
- **No reconciliation.** Without it, the first sign of a bug is a tutor counting her own lessons.

## Related

- The other case in this category: a flash ticket sale that must never oversell (coming in a later batch).
- Design pages: [idempotency](../../design/idempotency.md), [sagas](../../design/sagas.md), [timeouts and circuit breakers](../../design/timeouts.md), [back-of-the-envelope estimates](../../design/estimates.md).
- Other pages: [append-only logs](../../dsa/append-only-logs.md), [state machines](../../dsa/state-machines.md), [floating point](../../math/floating-point.md), [consistency](../../data/consistency.md).
