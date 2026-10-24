# Managed services

Last reviewed: 2026-10-24

A concept page: renting a database, a queue or a search engine already running, and what you hand over with it.

## Problem

Running your own database, queue or search cluster takes people, time and expertise. A cloud provider will run one for you, patched and backed up, for a fee. That's usually a good deal. But each one is a dependency on another company's prices, priorities, outages and product decisions, and the more you use, the more of your system is something you can't change.

## The story

In 2017 Tamsin Doyle was the first engineer at a startup building an app for dog walkers. She had no operations team and no wish to become one. So everything was managed: the provider's database, its queue, its search, its login service, its push notifications, its serverless functions. In two months she had a working product that would have taken a team a year to build from parts. It was the right call, and she'd make it again.

The costs arrived over the next three years, one at a time. The provider's search service raised its prices by forty percent. Its login service didn't support a feature their biggest customer needed, and there was nothing to do but wait. One December day, the provider's main region had a long outage, and the app, every part of which lived there, went down with it for most of a day. Tamsin could only watch the status page. Then the provider announced it was retiring the notifications service the app used, with a year's notice.

*Before reading on: managed services had made the company possible, and every one of them was a decision someone else could change. What would you have done differently, without giving up the speed?*

Tamsin didn't move off managed services; that would have been the expensive mistake. She sorted them. The ones that were truly commodity, storage, queues and the database, she kept, because they were standard enough that several providers offered them and the code using them was ordinary. Where a service was unusual or tied the app's design to one provider, as login and notifications had, she put a thin layer of their own code in front of it, so replacing it meant changing one module, not the whole app. She wrote down, for each service, what they'd do if it disappeared or doubled in price. For the few features that had to survive a regional outage, she paid for a standby elsewhere. For the rest, she accepted the risk on purpose and told the founders so.

Looking back, Tamsin thought managed services were the right default for a small team, and that the mistake was treating them as free of decisions. Each one was a rung someone else had built and could move.

## Where it shows up

| Page | The service | What it cost |
| --- | --- | --- |
| [9, Buying computers is too slow](../09-buying-computers-is-too-slow.md) | Every managed service the teams adopted | Speed early on, and a bill that doubled without anyone looking. |
| [Data gravity](../data/data-gravity.md) | Services built next to the data | Each one adds to the pull that keeps you where you are. |
| [Software supply chain](supply-chain.md) | Code and services from others | Trust in their decisions, extended without review. |
| [The cost of reliability](../cost/reliability.md) | A provider's availability | Your availability can't exceed theirs unless you pay for more. |

It shows up elsewhere too: hosted login and payments, email delivery, analytics, error tracking, and large language model APIs.

What these share is the control-versus-ease ladder: a managed service is a step up towards ease. It's usually the right step, and it's best taken knowing what's being handed over.

## It really happened

Tamsin is fictional; her December day happens to real companies. On 7 December 2021 a problem in AWS's largest region, us-east-1, caused hours of disruption for many companies whose services depended on it. Providers also retire products: Google, for example, shut down its Cloud IoT Core service in 2023, giving customers about a year to move. Netflix's move to AWS on [page 9](../09-buying-computers-is-too-slow.md) is the other side: a company choosing managed infrastructure deliberately, and spending its own engineering on what the provider didn't sell.

## What it is

A managed service is infrastructure, such as a database, queue, cache, search, login or messaging system, run by a provider and rented by use or by the hour. It trades control for ease: no patching, scaling or backups to run yourself, in exchange for dependence on the provider's prices, features, reliability and roadmap. Good use keeps commodity services standard, isolates unusual ones behind your own interfaces, plans for retirement and price changes, and matches redundancy to what truly needs it.

## Where it gets misapplied

- **Everything in one region of one provider, unexamined.** Fine, until the region has a bad day.
- **Unusual services woven through the code.** A provider-specific feature in a hundred places is a migration nobody can afford.
- **No exit plan.** Not knowing what you'd do if a service vanished or doubled in price.
- **The mirror:** running everything yourself to avoid lock-in, and spending the team's time on what a provider does better and cheaper.

## Connections

- Learning this is also learning [data gravity](../data/data-gravity.md), because managed services cluster around your data and make it heavier.
- Learning this is also learning [reading a cloud bill](../cost/cloud-bills.md), because every managed service has its own pricing units.
- Learning this is also learning [the cost of reliability](../cost/reliability.md), because a provider's outage is your outage unless you've paid otherwise.
- Learning this is also learning [VM provisioning](../cloud/vm-provisioning.md), because the step below a managed service is running it yourself on machines you start.
- Learning this is also learning [software supply chain](supply-chain.md), because a managed service is a dependency you can't even read.

## Resources

1. Dan McKinley, ["Choose Boring Technology"](https://mcfunley.com/choose-boring-technology) (start here: on spending your limited capacity for new things). <!-- verify -->
2. Your provider's service-level agreements and deprecation policies (go deeper: what they actually promise).
3. Public post-incident reports from cloud providers (reference).

## Names you'll hear

- **Managed service, PaaS:** infrastructure run for you.
- **SLA:** the provider's contractual promise, usually a credit if missed, not a guarantee.
- **Deprecation, end of life:** a provider retiring a service.
- **Vendor lock-in:** being kept by the cost of leaving.
- **Undifferentiated heavy lifting:** work that's necessary but gives you no advantage, the case for renting it.

## Go and look

List the managed services a project you work on depends on. For each, write one line: what would you do if it doubled in price or was retired next year?
