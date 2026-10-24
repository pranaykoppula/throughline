# 9. Buying computers is too slow

Last reviewed: 2026-10-24

## Problem

To run software you needed computers, and computers had to be bought, shipped, racked and paid for before anyone knew whether the software would be used. That was slow and expensive, and it decided who could start a company at all.

## The story

Tariq Haddad and two friends started a company in 2005 that let teachers record lessons and share them as video. Before they had a single customer, they needed servers. The quote was sixty thousand dollars for ten machines, six weeks for delivery, and a monthly fee for space in a data centre to put them in. They had raised a hundred and fifty thousand in total. Tariq spent a week on a spreadsheet trying to guess how many teachers might sign up in their first year, knowing the guess would decide how much of their money turned into metal. They bought six.

In their fourth month a popular education blog wrote about them, and in one morning more teachers signed up than in the previous three months together. Six servers weren't close to enough. The site slowed to a crawl and then stopped. Tariq ordered more machines that afternoon. They arrived five weeks later, by which time the teachers who'd tried the site and found it broken had long since moved on. The servers sat mostly idle for the rest of the year. He'd guessed too low, then paid to be ready for a day that had already passed.

In 2006 Amazon opened a beta of something it called EC2. You could rent a virtual computer, a slice of a machine in Amazon's data centre, by the hour, and start one in minutes from a web page. Tariq was sceptical. It was a bookshop renting out computers. But he tried it, and the next time a blog mentioned them he started forty machines in a quarter of an hour and switched them off again three days later. The bill was a few hundred dollars. He sold the servers they'd bought. For the first time, the cost of their computers rose and fell with how much they were used, and the next company like theirs could start with a credit card.

There were surprises. Some days a machine was slower for an hour for no reason he could find. His code hadn't changed. Another customer on the same physical host was busy, and they were sharing more than he'd assumed. He learned to build as though any single machine might be slow, or vanish, and to have the system replace it without anyone noticing. Machines stopped being things with names and became things you started and stopped.

The company grew. By 2013 it had sixty engineers, eight million students, and nearly two petabytes of video. Every team had been told to move fast and use whatever the cloud offered: a managed database here, a queue there, a search service, a transcoding service. Nobody was told to look at the bill, and for years nobody did. Then the finance director came to Tariq's desk with a printout. Last month's bill had been four hundred and ten thousand dollars, double what it was a year before. Revenue hadn't doubled.

*Before reading on: nothing had broken and no one had made an obvious mistake, but the bill had doubled. Where would you have looked first?*

Tariq expected to find the big compute machines at the top of the bill. He didn't. The largest single line was data transfer out: a charge for every gigabyte that left Amazon's network. Every time a student watched a lesson, the video was sent from storage straight across the internet, and each time it was paid for again. A partner's analytics system copied all their viewing logs to another cloud every night, and that was paid for too. Further down he found three test environments that nobody had turned off in a year, and a search cluster sized for a launch that never happened.

That was when he understood what renting really meant. With machines you'd bought, a careless design wasted the money you'd already spent. With machines you rented, a careless design cost money every hour, forever. Every architecture decision was also a line on a bill. So he redesigned for cost the way he'd once redesigned for speed. Popular lessons were cached closer to students, so each video crossed the expensive boundary once instead of thousands of times. The analytics sync was replaced with a summary a hundredth of the size. The idle environments were switched off and given automatic shutdowns. In four months the bill had halved.

A year later the board asked the obvious question. If the cloud cost four million dollars a year, why not buy their own servers again, like Dropbox was rumoured to be doing? Tariq did the arithmetic properly this time. Owning would probably save a third of the bill. It would also need six people they didn't have to run the hardware, a migration of most of a year, and moving two petabytes out of Amazon, at Amazon's price for data leaving. The cost of leaving had been built in all along, and he'd never noticed it while arriving. For a company their size, he concluded, staying was right. He also concluded that it should be a decision they made deliberately, every couple of years, with numbers, and not a default nobody questioned.

There was one more thing he only noticed later, preparing for a sales meeting. Schools rarely left them, and the main reason was years of recorded lessons that would be painful to move. He'd spent a month resenting how hard Amazon made it to leave. His own product had been built the same way, and it was the most valuable thing the company owned.

Looking back, Tariq thought the cloud had changed less about technology than about money. Machines were rented by the unit, so cost became something you designed, like speed. Paying as you went instead of up front had changed who could start a company. And the hardest advantages to compete with, the cost of leaving, the value of a network, the savings of size, were mostly things engineers built or wore away, often without anyone calling them that.

## It really happened

Tariq is fictional; the shift wasn't. Dividing one physical machine into many virtual ones began with IBM's CP-67 in 1967, so that one expensive mainframe could serve many users each with their own operating system ([page 2](02-one-machine-many-programs.md)). Amazon turned on the first EC2 beta instance in August 2006, six months after launching S3 storage ([TechCrunch](https://techcrunch.com/2021/08/28/how-amazon-ec2-grew-from-a-notion-into-a-foundational-element-of-cloud-computing/)). Its early machines ran on the open-source Xen hypervisor. Renting the hypervisor's slices by the hour is the business the hyperscalers were built on.

Two companies made opposite choices, and both were right for them. Netflix spent seven years moving everything to AWS after a database failure in 2008 stopped it shipping DVDs for three days, finishing in January 2016 ([Netflix](https://about.netflix.com/en/news/completing-the-netflix-cloud-migration)). It spent its engineering on what Amazon didn't sell, and kept its own delivery network ([page 5](05-machines-need-to-talk.md)). Ladder: up. Dropbox went the other way. It moved most of its users' files off a third-party provider onto its own storage system and reported saving about $75 million over two years in its 2018 filing to go public ([GeekWire](https://www.geekwire.com/2018/dropbox-saved-almost-75-million-two-years-building-tech-infrastructure/); [S-1](https://www.sec.gov/Archives/edgar/data/0001467623/000119312518055809/d451946ds1.htm)). Ladder: down, at exabyte scale, where storage was the product. More recently 37signals left the cloud and reported its bill falling from about $3.2 million a year to well under half that; its founder said plainly that others' results would vary ([DatacenterDynamics](https://www.datacenterdynamics.com/en/news/37signals-claims-it-saved-almost-2m-last-year-from-cloud-repatriation/)). Each company was describing its own decision, and each had a reason to make it look good.

Why does data leaving the cloud cost so much? A competitor argues it's priced far above cost ([Cloudflare](https://blog.cloudflare.com/aws-egregious-egress/)); Amazon says it pays for redundancy. Honestly, it's both a real cost and a switching cost, and also profit ([forces: switching costs](forces.md#switching-costs-and-lock-in)).

## What survived

Machines are rented by the unit, so cost is a live design variable: every architecture is also a bill, every hour. Paying as you go instead of up front changes who can start a company and how fast. Sharing physical machines means sharing their performance too. And the advantages hardest to compete with, switching costs, network effects, scale, are mostly built or eroded by engineering decisions, including the vendor's and your own ([forces: the moat](forces.md#composite-the-moat)).

## Where it gets misapplied

- **Kubernetes for a three-person team.** A platform built for running thousands of services, adopted to run three. The operating cost is paid in people.
- **Serverless for a workload that runs all the time.** Paying per request is cheap when requests are rare and expensive when they never stop.
- **"Cloud is cheaper" without a bill to prove it.** Or "owning is cheaper", without counting the people, the migration, and the cost of leaving.
- **The mirror:** a startup running its own data centre. Tariq's six servers in 2005, out of habit, when renting would do.

## Connections

- Learning this is also learning [hardware](01-one-machine-one-program.md), because a rented machine still has a memory hierarchy, now with a network at the bottom.
- Learning this is also learning [networking](05-machines-need-to-talk.md), because data transfer is a line on the bill and the round trip has a price.
- Learning this is also learning [reading a cloud bill](cost/cloud-bills.md), because this is the page where cost becomes something you design, and the bill is where you find out what you designed.
- Learning this is also learning [least privilege](auth/least-privilege.md), because cloud permissions decide who can start, read, or delete anything you rent, and the default is usually too much.
- Learning this is also learning [managed services](vendors/managed-services.md), because every managed service is a rung someone else built, and a dependency on their prices.
- Learning this is also learning [VM provisioning](cloud/vm-provisioning.md), because starting a machine from a web page hides a lot of work you'll eventually need to understand.
- Learning this is also learning [profiling](tooling/profiling.md), because Tariq expected compute at the top of the bill and found data transfer: a bill is a profile of where the money goes.
- Learning this is also learning [abstraction](03-programs-too-big-for-one-head.md), because a virtual machine hides the hardware but not the neighbours sharing it.
- Learning this is also learning [caching](latency/caching.md), because caching popular lessons near students is what made the data-transfer line shrink.

## Resources

1. Dan McKinley, ["Choose Boring Technology"](https://mcfunley.com/choose-boring-technology) (start here: on spending your limited capacity for new things carefully). <!-- verify -->
2. Armbrust et al., ["Above the Clouds: A Berkeley View of Cloud Computing"](https://www2.eecs.berkeley.edu/Pubs/TechRpts/2009/EECS-2009-28.pdf) (2009; the economic case, made early). <!-- verify -->
3. Wang and Casado, ["The Cost of Cloud, a Trillion Dollar Paradox"](https://a16z.com/the-cost-of-cloud-a-trillion-dollar-paradox/) (2021), with Corey Quinn's [rebuttal](https://www.lastweekinaws.com/blog/the-trillion-dollar-paradoxical-arguments-of-a16z) (go deeper: read both).
4. Your cloud provider's own pricing pages (reference: the truth is in the per-unit prices, especially for data transfer).

## Names you'll hear

- **IaaS, PaaS, SaaS:** renting machines, renting a platform to run code on, renting finished software.
- **Capex and opex:** money spent up front on things you own, and money spent as you go.
- **Hypervisor:** the layer that divides one physical machine into many virtual ones.
- **Containers:** a lighter way to share one machine, dividing up an operating system instead of the hardware.
- **Noisy neighbour:** another tenant on the same host slowing you down.
- **Innovation tokens** (McKinley): a team can afford only a few new technologies at once.

## Go and look

Pull up a real cloud bill, your team's or a published one, and find one line item that's a design decision wearing a price tag.

## The model so far

New on this page: sentence 9, in bold. The full model is in [the-model.md](the-model.md).

Engineering is turning what we have into what someone values, within limits, for a reason. Every step is a trade-off, and the engineer's job is to negotiate them.

0. Humans don't operate on the world directly; we build representations of it and operate on those. Every representation is a choice among others that could have been made, and every choice has an edge: decimal gave way to binary; naturals gave way to negatives, irrationals, and complex numbers; bits now have qubits beside them for a narrow class of problems; even formal axioms have an edge, since any consistent system rich enough for arithmetic contains true statements it can't prove (Gödel), and a cousin of that limit shows up in computation as the halting problem (Turing). This wiki hands out representations the same way every textbook does: cleanly, past their edges. Finding the edge is the reader's job.

1. A computer is a little fast memory near a processor and ever larger, slower, cheaper storage further away. Everything fast is small and near; everything big is slow and far. The cost of an operation is set by where the data is.

2. A machine's resources are shared, so something has to divide them: the operating system turns one machine into many processes and threads and decides who runs. Sharing creates waiting, and waiting, not computing, is where most time goes.

3. Programs outgrow a single head, so we build layers of abstraction: languages, libraries, types. Each layer trades control for ease. Building is mostly assembling existing abstractions; optimizing is mostly replacing one with something made for the case at hand, and the skill is knowing when the abstraction's cost has been measured and found to dominate. Data structures and algorithms are the reusable shapes inside those layers, chosen by the access pattern they serve.

4. Data outlives programs, so its shape is the longest-lived decision. A store is chosen by how data is read and written; indexes trade write cost for read speed; transactions define what the store promises.

5. Data is rarely where it's needed, so it moves, and moving it is slow, unreliable, and paid for in round trips. Protocols are contracts between parties that can't see each other. Anything that crosses a network can be lost, delayed, or duplicated, so systems retry and tolerate repeats. Once data moves cheaply, distribution is free, and value shifts from copies to services, relationships, and trust.

6. Client and server split the work: the server owns the truth, the client owns presentation and a copy of state. Most interface bugs are two sources of truth disagreeing. The browser won because shipping one server beats shipping a million installs; native shells survive where platforms control distribution.

7. Once strangers can reach a system, every boundary is a question of who is asking and what they may do. Trust nothing that crossed a boundary; give every party the least it needs. Harms from data fall on people other than those who collect it, so law steps in where incentives don't.

8. When one machine isn't enough, data is copied and split, and copies disagree for a while. Every distributed design chooses what to promise about consistency versus availability. Precompute what is read often; accept approximate answers where exactness costs too much.

9. **Machines are rented by the unit, so cost is a live design variable: every architecture is also a bill. Subscription ties the vendor's revenue to the customer's continued use, and capex becoming opex changes who can start a company. An advantage competitors can't copy quickly is worth more than a better product, and most such advantages, switching costs, network effects, scale, are things engineers build or erode.**
