# Multi-tenancy

Last reviewed: 2026-10-24

A concept page: many customers sharing one system, and the boundary that must keep each one's data their own.

## Problem

Running one copy of a system for all customers is far cheaper than running one each, and it's how most software-as-a-service works. But then every customer's data sits side by side in the same tables, the same caches and the same machines. One missing filter anywhere and a customer sees someone else's data. And one busy customer can slow everyone down.

## The story

In 2014 Chidi Nwosu built the reporting features for a company selling bookkeeping software to small businesses. Every customer's data lived in the same database. Each row carried a `company_id`, and every query was supposed to include *where company_id = ?*. It was the standard design, cheap and simple, and the team had a code review rule to check for the filter.

In the autumn a new engineer added a report of overdue invoices. His query joined three tables and filtered by company on the first, but one of the joins pulled in invoices without checking their company. On a quiet Tuesday, a bakery's owner opened the report and saw thirty overdue invoices from a plumbing firm in another city. She phoned, puzzled and then angry. Chidi found the query in ten minutes and the cause in twenty. The reviewer had checked for the filter, seen one, and approved it.

*Before reading on: every query was supposed to remember the filter, and one forgot. How would you make forgetting impossible?*

Chidi moved the rule out of the queries and into the database. Every table got a policy, enforced by the database itself: rows were visible only if their `company_id` matched the company set for the current connection. Each request set that once, at the start, from the logged-in user. A query that forgot the filter now simply returned nothing from other companies, because the database wouldn't show it. He added a test that ran every report as one company against data seeded for two, and failed if anything from the second appeared. For the few largest customers, whose heavy reports slowed everyone else's, he moved their reporting to a separate replica.

Looking back, Chidi thought the bug hadn't been in the overdue-invoices query. It was in a design where safety depended on every engineer remembering one line in every query, forever.

## Where it shows up

| Page | The shared thing | The boundary |
| --- | --- | --- |
| [4, Data outlives programs](../04-data-outlives-programs.md) | Rows in a shared database | Who may read which row is the line between one customer's data and another's. |
| [Least privilege](least-privilege.md) | Each customer's access | Each tenant sees only its own data: least privilege between customers. |
| [2, One machine, many programs](../02-one-machine-many-programs.md) | One machine's processor and devices | Sharing means one job's behaviour affects everyone's. |
| [9, Buying computers is too slow](../09-buying-computers-is-too-slow.md) | Cloud hosts shared between companies | Noisy neighbours: another tenant's load becomes your slowdown. |

It shows up elsewhere too: shared caches keyed without the tenant, search indexes, file storage, logs, and background jobs that process many customers' data at once.

What these share is that the cheapest way to serve many customers is to share everything, and every shared thing needs a boundary enforced in one place rather than remembered in many.

## It really happened

Chidi is fictional; the database feature he used is real. PostgreSQL added row-level security in version 9.5 (2016), letting a table enforce which rows each session can see. Cloud providers face the same problem at a much larger scale. In 2021 security researchers at Wiz reported a flaw in Microsoft Azure's Cosmos DB that could have let one customer obtain the keys to other customers' databases. Microsoft fixed it and notified affected customers. Isolation between tenants is the promise a shared service most needs to keep.

## What it is

Multi-tenancy is serving many customers, or tenants, from one shared deployment. Isolation can be by separate databases, separate schemas, or shared tables with a tenant column, in decreasing order of separation and cost. Whatever the model, tenant filtering should be enforced in one place, such as database policies, a single data-access layer, or separate credentials, and tested directly. Performance isolation, so one tenant can't starve others, needs limits and sometimes separate resources for the largest tenants.

## Where it gets misapplied

- **Filtering by convention.** Every query remembering `company_id`, until one doesn't.
- **Shared caches without tenant keys.** A cached report for one company served to another.
- **No limits per tenant.** One customer's huge import slowing everyone.
- **The mirror:** a separate full deployment for every small customer, multiplying cost and the number of systems to upgrade.

## Connections

- Learning this is also learning [least privilege](least-privilege.md), because tenant isolation is least privilege between customers.
- Learning this is also learning [partitioning](../data/partitioning.md), because tenants are a natural partition key, and large ones become hot spots.
- Learning this is also learning [caching](../latency/caching.md), because a cache shared between tenants must include the tenant in every key.
- Learning this is also learning [queueing](../latency/queueing.md), because fair sharing between tenants is the same problem as fair queues.
- Learning this is also learning [cloud IAM](cloud-iam.md), because the provider's own isolation between its customers is the same problem one level down.

## Resources

1. Your database's documentation on row-level security or equivalent (start here).
2. [OWASP's guidance on access control](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html) (go deeper). <!-- verify -->
3. Cloud providers' guides to SaaS tenant isolation (reference).

## Names you'll hear

- **Tenant:** one customer of a shared system.
- **Row-level security:** the database enforcing which rows each user can see.
- **Silo, pool:** a separate deployment per tenant, or shared resources for all.
- **Noisy neighbour:** one tenant's load affecting others.
- **Cross-tenant leak:** one customer seeing another's data, the failure to prevent.

## Go and look

Find where tenant filtering happens in a system you work on. Count how many places would have to remember it. If the answer is more than one, find out what stops one of them forgetting.
