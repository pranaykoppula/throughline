# 11. Software that must not go down

Last reviewed: 2026-10-24

## Problem

Once people depended on software every hour of every day, it couldn't just be fixed when someone noticed it was broken. Teams needed to know it was failing before users told them, and to agree on what "working" meant, because perfect wasn't on offer.

## The story

Rosa Mendes joined an online ticketing company in 2008 as one of three people who kept the site running. Concert tickets went on sale at ten in the morning, and for the next twenty minutes the site took more traffic than in the rest of the week. On the wall of the operations room a big screen showed a grid of servers, each one a green square if it was up and its processor was below ninety percent.

The first big on-sale she worked was for a band that sold out stadiums. At ten past ten every square on the screen was green. At twelve past, a support manager ran in holding a laptop showing a wall of angry posts from customers: the checkout page was spinning and then failing. Rosa stared at the screen. Everything was up. It took her forty minutes to find out that the payment provider was taking thirty seconds to answer, and the checkout gave up after twenty. Every server was healthy, and nobody could buy a ticket.

She went home that night thinking about the green squares. They'd answered the question *are the machines on?* Nobody had asked the question that mattered: *can people buy tickets?* The next week she built a robot that bought a real ticket, to a test event, every minute, and a chart of what fraction of real checkouts succeeded and how long they took. For the first time, the screen measured something a customer would recognise.

After a second bad on-sale, caused by a database that filled its disk overnight, the company's founders were clear: never again. Rosa took that literally. She added an alert for everything she could think of: every disk over seventy percent, every slow query, every error in every log, every queue longer than a hundred items. Within a month there were three hundred alerts, and the person on call was woken forty times a night.

Almost none of the alerts meant anything. A disk would hit seventy percent and stay there for a year. A slow query would run once at 3am for a report nobody read. The on-call engineers learned, quite reasonably, to glance at the pager and go back to sleep. Some quietly set filters to hide whole categories. Six weeks later the payments database started running out of connections at four in the morning. The alert fired, in among thirty-eight others that night, and nobody looked. The site was down for two hours before anyone noticed, and it was a customer who told them. Rosa had built the alerts to make sure nobody ever missed a problem, and the noise had guaranteed someone would.

*Before reading on: too few alerts had missed a real problem, and too many had buried one. How would you decide what's worth waking someone up for?*

Rosa started from the other end. Instead of asking what could go wrong, she asked what *working* meant, in terms a customer would use, and how much failure was acceptable. That second question started an argument. One of the founders said the answer was obviously zero. Rosa asked what zero would cost. No deploys during on-sales, she said, then no deploys at all, then two of everything in two data centres, and even then a network somewhere would fail. They settled, after a long afternoon, on a sentence: 99.9% of checkouts succeed within three seconds, measured over thirty days. That left a tenth of a percent, about forty-three minutes a month of failure, which they could spend.

The sentence changed everything after it. Rosa deleted most of the three hundred alerts. Only two things would wake someone up now: checkouts failing or slowing badly enough that the month's allowance would run out within hours, or the ticket robot failing. Everything else became a note for the morning. The pager went off twice a month, and when it did, people jumped. The allowance also settled arguments that used to be about feelings. When the team had burned most of the month's budget on a bad release, new features waited and reliability work came first. When the budget was nearly untouched, they could ship faster and take more risks. Reliability had become a number both sides could see.

Two years later a problem arrived that none of her charts could see. A small number of customers in Brazil, paying with one particular card on Android phones, were failing at checkout. Overall success was 99.95%, comfortably inside the target. Every chart showed an average or a total, and this group was too small to move any of them. Rosa could only answer the questions she'd thought to ask when she built the charts, and she hadn't thought of this one.

So the team changed what they recorded. Instead of adding to a few counters, every request now wrote down everything about itself: country, device, card type, which services it passed through, and how long each step took. They couldn't build a chart for every combination, but they could ask any question afterwards. The next odd problem, slow checkouts for one venue's tickets only, took twenty minutes to find instead of three days.

Looking back, Rosa thought her years on call came down to a few plain ideas. Everything fails, so the questions are how you'll know and what you've promised. Decide what "working" means, from the customer's side, before you measure anything. Only wake people for what threatens that promise. And record enough to answer questions you haven't thought of yet, because the next failure will be one you didn't predict.

## It really happened

Rosa is fictional; her lessons were learned the hard way at much larger companies. Google's site reliability engineers wrote down the error budget: agree on a target below 100%, and treat the gap as a budget that both developers and operators can spend ([*Site Reliability Engineering*, "Embracing Risk"](https://sre.google/sre-book/embracing-risk/) <!-- verify -->). Google's 2010 paper on Dapper described tracing requests across many services, the idea behind recording each request's whole journey.

On 1 August 2012, Knight Capital deployed new trading code incorrectly. Old code that should have been dead was triggered by a reused setting. In the first 45 minutes of trading its systems sent more than four million orders, and the firm lost more than $460 million. The SEC's findings add a detail Rosa would recognise: before the market opened, an internal system had sent 97 automated emails flagging the error, and nobody acted on them ([SEC, 2013](https://www.sec.gov/news/press-release/2013-222)). In February 2017, an engineer running a routine command to remove a few servers from Amazon S3 typed one input wrong and removed far more. Large parts of the internet that depended on S3 failed for hours. Amazon's fix was to change the tool so it couldn't remove capacity that quickly, not to blame the engineer ([AWS post-incident summary](https://aws.amazon.com/message/41926/)). Both accounts are official and both are edited. The SEC was writing an enforcement order, and Amazon was writing to reassure customers. Read them for what happened, and be careful about why.

## What survived

Everything fails; the questions are how you'll know and what you've promised. Define "working" from the user's side, as a target below 100%, and treat the gap as a budget you can spend. Alert only on what threatens the promise, or the alerts will be ignored. Record enough about each request to answer questions you haven't asked yet. After a failure, fix the system that let a person's mistake become an outage.

## Where it gets misapplied

- **Dashboards nobody reads.** A wall of charts that measures the machines and not the customer.
- **Alerts everyone mutes.** Rosa's three hundred. An alert that's usually wrong is worse than no alert, because it teaches people to ignore the pager.
- **Three monitoring vendors.** Each bought to fix the last one's gap, none of them set up to answer the question you have today.
- **The mirror:** five nines for an internal report nobody opens at night. Reliability is bought with money and speed. Spend it where users notice.

## Connections

- Learning this is also learning [operating systems](02-one-machine-many-programs.md), because processes die and machines get stuck, and something has to notice.
- Learning this is also learning [scale](08-too-many-users-too-much-data.md), because with many machines, something is always partly broken.
- Learning this is also learning [collaboration](10-many-people-one-codebase.md), because incidents are handled by teams, and blameless reviews are a team practice.
- Learning this is also learning [cost](cost.md), because every extra nine costs more than the last.
- Learning this is also learning [math](math.md), because averages hide the tail, and the tail is where users suffer: measure percentiles.

## Resources

1. Google, [*Site Reliability Engineering*](https://sre.google/sre-book/table-of-contents/), chapters 3 to 6 (start here: free online; risk, targets, toil and monitoring). <!-- verify -->
2. Charity Majors, Liz Fong-Jones and George Miranda, *Observability Engineering* (go deeper: Rosa's Brazil problem, as a discipline).
3. [AWS, S3 post-incident summary, 2017](https://aws.amazon.com/message/41926/): a short, real postmortem.
4. John Allspaw, ["Blameless PostMortems and a Just Culture"](https://www.etsy.com/codeascraft/blameless-postmortems) (2012; reference: why blaming people hides the system). <!-- verify -->

## Names you'll hear

- **SLI, SLO, SLA:** what you measure, the target you set for it, and the contract with penalties if you miss.
- **Nines:** 99.9% is "three nines", about 43 minutes of failure a month; 99.999% is about 26 seconds.
- **Error budget:** the failure your target allows, spent on risk.
- **Observability:** being able to ask new questions of a running system without shipping new code.
- **Blameless postmortem:** a review of an incident that asks what let the mistake through, not who made it.

## Go and look

Find where "working" is actually defined for something you maintain (a test, a dashboard, a runbook) and who decided that definition. If nobody did, that's the answer.

## The model so far

New on this page: sentence 11, in bold. The full model is in [the-model.md](the-model.md).

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

9. Machines are rented by the unit, so cost is a live design variable: every architecture is also a bill. Subscription ties the vendor's revenue to the customer's continued use, and capex becoming opex changes who can start a company. An advantage competitors can't copy quickly is worth more than a better product, and most such advantages, switching costs, network effects, scale, are things engineers build or erode.

10. Systems are built by many people over time, so the codebase is itself a system, with its own data (history), protocols (branches, reviews), and trust boundaries. Practices live in tools; choosing a tool is choosing a practice.

11. **Everything fails; the questions are how you'll know and what you promised. Define what "working" means before measuring it. Instrument for questions you haven't asked yet.**
