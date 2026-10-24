# Reading a cloud bill

Last reviewed: 2026-10-24

A concept page: the bill as a record of design decisions, and how to read it.

## Problem

When computers are rented by the unit, every design choice keeps costing money for as long as it runs. The bill is the only place all those choices add up, and it's written in units, such as gigabytes transferred, requests, and terabytes scanned, that don't look like the decisions that caused them.

## The story

In 2019 Priya Nair led the data platform at an online retailer. The company had moved its analytics to a cloud data warehouse that charged by the amount of data each query read. Priya's team had made a deliberate, popular decision: anyone in the company could query anything, with no approvals and no tickets. Analysts loved it. Marketing built its own dashboards. It felt like the point of having data.

Three months in, the finance director sent her a one-line email: why had analytics cost ninety thousand dollars last month, against a budget of fifteen?

Priya opened the bill expecting to find something exotic. Instead she found ordinary things, multiplied. The biggest single cost was one marketing dashboard. It showed yesterday's sales by region, refreshed itself every five minutes, and each refresh read the entire four-year sales table, eleven terabytes, to find one day. Nobody had thought about what a refresh cost, because nobody saw a price when they built it. The second biggest was an analyst's habit of starting every query with "select everything" and filtering afterwards.

*Before reading on: nobody had done anything foolish, and the bill was six times the budget. What would you have changed: the access, the data, or what people could see?*

Priya didn't take away the open access; it was why people used the data at all. She changed three other things. First, the sales table was split by date, so a query about yesterday read yesterday and nothing else. The dashboard's refresh went from eleven terabytes to a few gigabytes. Second, every query showed its estimated cost before it ran, in dollars, not terabytes. People who'd never thought about cost started rewriting queries on their own. Third, each team got a monthly budget with an alert at eighty percent. The next month's bill was eleven thousand dollars.

Looking back, Priya thought the bill had been the most honest document in the company. Every line on it was a design decision someone had made without seeing its price. The cure wasn't to make decisions harder. It was to show the price at the moment of deciding.

## Where it shows up

| Page | The line on the bill | The decision behind it |
| --- | --- | --- |
| [9, Buying computers is too slow](../09-buying-computers-is-too-slow.md) | Data transfer out | Sending every video straight from storage across the internet, every time it was watched. |
| [12, Machines that learn from data](../12-machines-that-learn-from-data.md) | Tokens | Sending the whole help centre with every question. Sending only the relevant articles cut it by ninety percent. |
| [Profiling](../tooling/profiling.md) | Any of them | A bill is a profile of where the money goes, and the biggest line is rarely the one you'd guess. |

It shows up elsewhere too: idle machines nobody switched off, logs kept forever, test environments left running, and storage that's never read.

The lines share Priya's lesson. In each case the cost came from a reasonable design whose price was invisible when it was chosen. The fixes were the same kinds of things: read or send less data, keep it closer, and show the cost to the person making the decision.

## It really happened

Priya is fictional; pricing by data scanned is standard for cloud data warehouses, and splitting tables by date, called partitioning, is the usual first fix. Cloud costs became important enough that in 2019 practitioners founded the FinOps Foundation, later part of the Linux Foundation, to share practices for managing them. The argument about whether renting is cheaper than owning at scale is on [page 9](../09-buying-computers-is-too-slow.md), with Dropbox, Netflix and 37signals. And the argument about data transfer prices, made by a competitor, is in [forces](../forces.md#switching-costs-and-lock-in).

## What it is

A cloud bill lists usage by unit, multiplied by price: machine hours, gigabytes stored and transferred, requests, data scanned, tokens. Each unit traces back to a design decision. Reading it well means grouping costs by team and feature, finding the biggest lines, tracing each to the decision that causes it, and putting prices in front of the people who make those decisions.

## Where it gets misapplied

- **Looking at the total.** A single monthly number tells you something is wrong, not what. Break it down by service, team and feature.
- **Cutting the visible line, not the cause.** Buying discounts for machines that shouldn't be running at all.
- **Approval queues as cost control.** Making every query or machine need sign-off kills the reason you rented in the first place. Show prices instead.
- **The mirror:** optimising a bill that doesn't matter. A thousand-dollar bill for a product earning millions isn't where engineers' time should go.

## Connections

- Learning this is also learning [profiling](../tooling/profiling.md), because a bill is a profile of money, and the same rules apply: measure the whole, fix the top line, measure again.
- Learning this is also learning [storage tiers](storage-tiers.md), because what you store, and how fast you need it, is a large part of most bills.
- Learning this is also learning [access patterns](../data/access-patterns.md), because partitioning by date is shaping data for how it's actually read.
- Learning this is also learning [tokens and context windows](../ai/tokens.md), because language models are billed by the word, in and out.
- Learning this is also learning [data gravity](../data/data-gravity.md), because the cost of moving data out shapes what it costs to leave.

## Resources

1. Your cloud provider's pricing pages and cost explorer (start here: the truth is in the per-unit prices).
2. Corey Quinn's writing on cloud costs at [Last Week in AWS](https://www.lastweekinaws.com/) (go deeper: funny, sharp, and he sells cost consulting, so read with that in mind). <!-- verify -->
3. [FinOps Foundation](https://www.finops.org/) (reference: shared practices for cloud cost management). <!-- verify -->

## Names you'll hear

- **Egress:** data leaving a cloud provider's network, usually the line people don't expect.
- **Partitioning:** splitting a table, usually by date, so queries read only what they need.
- **Reserved instances, savings plans:** discounts for committing to use capacity in advance.
- **Tagging:** labelling resources by team or feature so the bill can be broken down.
- **FinOps:** the practice of managing cloud costs as an ongoing engineering and finance discipline.

## Go and look

Find one line on a real cloud bill, your team's or a published one, and trace it to the decision that caused it. Then ask whether whoever made that decision could see its price at the time.
