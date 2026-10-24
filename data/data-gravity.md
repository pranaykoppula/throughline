# Data gravity

Last reviewed: 2026-10-24

A concept page: the more data you have in one place, the harder it is to move, and the more everything else moves towards it.

## Problem

Small amounts of data move easily. Large amounts are slow and expensive to move, so applications, services and more data gather around wherever the data already is. That's usually efficient. It also means that where you first put your data can decide, years later, what you're able to do with it.

## The story

In 2017 Imogen Hart ran computing for a genetics research institute. Sequencing machines produced terabytes a week, and the institute had put all of it in one cloud provider's storage from the start. It was cheap, it scaled without anyone thinking about it, and the analysis pipelines ran on machines in the same provider, right next to the data. By 2020 there were four petabytes.

That year a rival provider released an analysis service the researchers badly wanted. It was faster, better suited to their work, and cheaper to run. Imogen priced the obvious plan: copy the data across. Moving four petabytes out of the first provider would cost several hundred thousand dollars in data transfer fees alone and take weeks over the network. A shipping service with physical drives was faster, and still expensive. Meanwhile the institute's pipelines, permissions and a dozen small tools all assumed the data lived where it did. The data had become heavy, and everything had settled around it.

*Before reading on: the data was too heavy to move, and the service the researchers wanted was somewhere else. What would you have done?*

Imogen stopped trying to move the data to the service. For most work she moved the computing to the data instead, running the rival's software, where its licence allowed, on machines in the first provider. For the few analyses that truly needed the new service, she sent only what they used: compact summaries and selected regions of genomes, a few terabytes rather than four petabytes. And she changed two habits for the future. New data was written in open, widely readable formats rather than a provider's own, and the institute negotiated its data transfer prices into its next contract, before signing rather than after.

Looking back, Imogen thought the first decision hadn't been wrong. Putting everything in one place had been simple and cheap for years. But each terabyte added had quietly raised the price of ever changing her mind, and nobody had been watching that price.

## Where it shows up

| Page | The heavy data | What it pulled towards it |
| --- | --- | --- |
| [9, Buying computers is too slow](../09-buying-computers-is-too-slow.md) | Tariq's two petabytes of video | The cost of leaving, built in all along; and his own customers, kept by years of recorded lessons. |
| [Reading a cloud bill](../cost/cloud-bills.md) | Data transfer out | Usually the line nobody expected, and the price of moving data anywhere else. |
| [Storage tiers](../cost/storage-tiers.md) | Petabytes in one store | The more there is, the more each move, between tiers or providers, costs. |
| [Forces: switching costs](../forces.md#switching-costs-and-lock-in) | Any data a customer has built up | The moat seen from the vendor's side; the migration tax from the customer's. |

It shows up elsewhere too: analytics teams moving their tools into the data warehouse, rather than exporting from it; companies choosing a cloud region because their biggest dataset is already there; and the long life of old databases nobody can afford to move.

What these share is that data's weight grows with its size, and compounds as other things come to depend on where it is. It's useful to keep compute close to data, and wise to know what it would cost to leave.

## It really happened

Imogen is fictional; the term is real. Dave McCrory coined "data gravity" in a 2010 blog post, describing how large datasets attract applications and services the way mass attracts mass. Data transfer pricing became a regulatory issue. In January 2024 Google Cloud said it would waive data transfer fees for customers moving all their data off its platform, with conditions ([CNBC](https://www.cnbc.com/2024/01/11/google-vows-not-to-charge-data-transfer-fees-when-cloud-customers-exit.html)). Under the EU's Data Act, providers may charge only their direct costs for switching until 12 January 2027, and nothing for switching after that. Ordinary data transfer during use can still be charged ([one summary](https://www.lw.com/en/insights/eu-data-act-significant-new-switching-requirements-due-to-take-effect-for-data-processing-services)). Regulators had noticed the same thing Tariq and Imogen did.

## What it is

Data gravity is the tendency of large datasets to be costly and slow to move, so that applications, services and further data accumulate around them. It pushes towards running computation where data lives. It also becomes a switching cost: the bigger the dataset in one provider or system, the more leaving costs. The practical responses are to move computation rather than data, move small derived data rather than raw data, use open formats, and know your exit price before you need it.

## Where it gets misapplied

- **Ignoring it until you want to leave.** The cost of moving grows every month; check it before it's a crisis.
- **Copying everything everywhere.** Spreading full datasets across providers "to avoid lock-in" doubles storage and creates [consistency](consistency.md) problems.
- **Choosing a provider for one feature.** The data you put there will stay long after the feature's advantage fades.
- **The mirror:** refusing to commit to any platform, and building everything twice. Some gravity is the price of getting work done.

## Connections

- Learning this is also learning [storage tiers](../cost/storage-tiers.md), because the size that makes data heavy is also what makes it expensive to store.
- Learning this is also learning [reading a cloud bill](../cost/cloud-bills.md), because data transfer out is where gravity shows up as money.
- Learning this is also learning [serialization formats](serialization.md), because data in an open format is lighter: more tools can read it where it is.
- Learning this is also learning [migrations](migrations.md), because moving heavy data is the hardest kind of migration.
- Learning this is also learning [managed services](../vendors/managed-services.md), because every service built next to your data adds to its pull.

## Resources

1. Dave McCrory's original 2010 post on data gravity (start here: short).
2. Cloudflare, ["AWS's Egregious Egress"](https://blog.cloudflare.com/aws-egregious-egress/) (go deeper: a competitor's argument about data transfer pricing; read it as advocacy).
3. A summary of the EU Data Act's switching rules, such as [Latham & Watkins's](https://www.lw.com/en/insights/eu-data-act-significant-new-switching-requirements-due-to-take-effect-for-data-processing-services) (reference).

## Names you'll hear

- **Egress:** data leaving a provider's network, usually charged.
- **Lock-in:** being kept by the cost of leaving rather than the value of staying.
- **Bring compute to data:** running analysis where the data is instead of copying it.
- **Data residency:** rules about which country data may be stored in, another kind of gravity.
- **Repatriation:** moving workloads back from the cloud to your own hardware.

## Go and look

Find the largest dataset you're responsible for and work out, roughly, what it would cost and how long it would take to move it to another provider. Write the number down, with today's date.
