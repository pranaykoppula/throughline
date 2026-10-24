# Forces

Last reviewed: 2026-10-24

The limits that aren't hardware. Each one changed what engineers build, and the spine pages bring them in only where they did. Read this page once; come back when a page points here.

Links marked with an HTML `verify` comment haven't been checked against the live page yet.

## Marginal cost

When a copy costs nothing to make, the copy stops being what people pay for. Value moves to whatever surrounds it: the service that runs it, the updates, the support, the network of other users, the trust. This is why open source can be free and still fund companies, why software moved from boxes to subscriptions, and why giving away the layer next to yours can be a strategy rather than charity. Spine: [5](05-machines-need-to-talk.md), [9](09-buying-computers-is-too-slow.md), [10](10-many-people-one-codebase.md).

- Joel Spolsky, ["Strategy Letter V"](https://www.joelonsoftware.com/2002/06/12/strategy-letter-v/): commoditize your complement. <!-- verify -->
- Carl Shapiro and Hal Varian, *Information Rules* (1998): the economics of goods that are expensive to make and free to copy. Old, and still the clearest.

## Network effects

Some products get more valuable with every user, so the leader pulls further ahead and the market tips towards one or two winners. A better product often loses to a bigger one. Engineers build these effects (shared formats, integrations, social graphs) whether or not anyone calls them that. Spine: [6](06-anyone-can-publish.md), [10](10-many-people-one-codebase.md).

- NFX, ["The Network Effects Manual"](https://www.nfx.com/post/network-effects-manual): a taxonomy, written by investors, so read it as a pitch too. <!-- verify -->
- *Information Rules*, the chapters on positive feedback and standards.

## Who pays vs who benefits

When the harm from a system falls on people other than the ones who built it, the builders have no reason to prevent it, so law steps in. Privacy, accessibility, and payment security are all here, and each became engineering work: deletion pipelines, data inventories, audit logs, semantic markup. Regulation is a limit like any other. Spine: [6](06-anyone-can-publish.md), [7](07-strangers-on-the-network.md).

- [GDPR, the official text](https://eur-lex.europa.eu/eli/reg/2016/679/oj). Long; Articles 5, 17 and 25 are the ones engineers meet. <!-- verify -->
- [WCAG](https://www.w3.org/WAI/standards-guidelines/wcag/), the accessibility standard most law points to. <!-- verify -->
- [PCI Security Standards Council](https://www.pcisecuritystandards.org/), the card industry's rules, written by the card industry. <!-- verify -->

## Distribution and platform power

Whoever controls the path to users controls the margin. App stores decide what ships and take a cut; browsers and operating systems set defaults; search ranks. A thin native shell around a web app is often a distribution decision, not a technical one. Spine: [6](06-anyone-can-publish.md), [12](12-machines-that-learn-from-data.md).

- Ben Thompson, ["Aggregation Theory"](https://stratechery.com/2015/aggregation-theory/): why owning the user relationship beats owning supply. <!-- verify -->
- [Apple's App Store Review Guidelines](https://developer.apple.com/app-store/review/guidelines/): a primary source for what a platform can require. <!-- verify -->

## Switching costs and lock-in

Leaving costs money now; the benefits of leaving arrive later and are uncertain. So people stay, even on worse technology, and vendors price accordingly. Data is the heaviest thing to move, which is why moving it out is often the most expensive line on a cloud bill. Seen from the customer's side, a moat is a migration tax. Spine: [9](09-buying-computers-is-too-slow.md), [13](13-everything-still-exists-at-once.md).

- Cloudflare, ["AWS's Egregious Egress"](https://blog.cloudflare.com/aws-egregious-egress/) (2021): a competitor's argument that egress is priced far above cost. Cloudflare sells the alternative; read it as advocacy with numbers.
- *Information Rules*, the lock-in chapters.

## Capex to opex

When computers had to be bought up front, starting a company meant raising money for machines before you knew if anyone wanted the product. Renting them by the hour moved that cost to after you had users, which changed who could start a company and how fast. The trade reverses at scale: renting forever can cost more than owning, and some companies move back. Spine: [9](09-buying-computers-is-too-slow.md).

- Armbrust et al., ["Above the Clouds: A Berkeley View of Cloud Computing"](https://www2.eecs.berkeley.edu/Pubs/TechRpts/2009/EECS-2009-28.pdf) (2009): the case for renting, made early. <!-- verify -->
- Sarah Wang and Martin Casado, ["The Cost of Cloud, a Trillion Dollar Paradox"](https://a16z.com/the-cost-of-cloud-a-trillion-dollar-paradox/) (2021), with Corey Quinn's [rebuttal](https://www.lastweekinaws.com/blog/the-trillion-dollar-paradoxical-arguments-of-a16z). Both sides have something to sell; read both.

## User expectation ratchets

Once one product does something, users expect it everywhere. Pages that update without reloading, feeds that scroll forever, documents several people edit at once, answers that stream in as they're written: each started in one product and became the bar. Each also pulled new work into the backend: APIs instead of pages, query languages for mobile, cursor pagination, CRDTs, streaming responses. The interface drives the backend more often than the other way round. Spine: [6](06-anyone-can-publish.md), [8](08-too-many-users-too-much-data.md), [12](12-machines-that-learn-from-data.md).

- Facebook Engineering, ["GraphQL: A data query language"](https://engineering.fb.com/2015/09/14/core-infra/graphql-a-data-query-language/) (2015): a mobile news feed producing a new API style. <!-- verify -->
- Ink & Switch, ["Local-first software"](https://www.inkandswitch.com/local-first/): collaboration as a requirement, and what it costs the backend. <!-- verify -->

## Incentives inside the org

You build what you're measured on, and systems take the shape of the teams that build them (Conway's law). A reorg is an architecture change. A metric becomes a target and stops measuring anything. Most "technical" decisions that look strange from outside make sense once you know who was rewarded for what. Spine: [10](10-many-people-one-codebase.md), [11](11-software-that-must-not-go-down.md).

- Melvin Conway, ["How Do Committees Invent?"](http://www.melconway.com/Home/Committees_Paper.html) (1968): the original, and short. <!-- verify -->
- Martin Fowler, ["Conway's Law"](https://martinfowler.com/bliki/ConwaysLaw.html): what the idea became, including teams designed on purpose to get an architecture. <!-- verify -->

## Composite: the moat

A moat is whatever keeps a company's position hard to attack after competitors have copied the product. Products can be copied; moats are the things around the product that can't: the cost of leaving (switching costs), value that grows with users (network effects), unit costs that fall with size (scale), control of how customers are reached (distribution), or something nobody else can get (a cornered resource). Most are built, or destroyed, by engineering decisions, which is why engineers should be able to name them.

Where it shows up on the spine: why cloud egress costs what it does ([9](09-buying-computers-is-too-slow.md)); why Google open-sourced Kubernetes ([10](10-many-people-one-codebase.md)); whether a foundation-model company has one at all, which is still argued ([12](12-machines-that-learn-from-data.md)); and the moat seen from the customer's side, as a migration tax ([13](13-everything-still-exists-at-once.md)).

Connections: learning moats is also learning [strangers on the network](07-strangers-on-the-network.md), because reliability and accuracy become a brand · [data gravity](data/data-gravity.md), because history is the stickiest data · [reading a cloud bill](cost/cloud-bills.md), because lock-in is priced on purpose · [collaboration](10-many-people-one-codebase.md), because open source, standards and APIs are moat strategy whether anyone says so or not.

- Hamilton Helmer, *7 Powers* (2016): the taxonomy above, in depth.
- Ben Thompson, ["Aggregation Theory"](https://stratechery.com/2015/aggregation-theory/). <!-- verify -->
- ["Google: We Have No Moat, And Neither Does OpenAI"](https://semianalysis.substack.com/p/google-we-have-no-moat-and-neither) (2023): a leaked internal memo, one employee's view, published by SemiAnalysis.

Names: "moat" is Warren Buffett's word; "7 Powers" is Helmer's.

**Go and look.** Pick a product you use that has real competitors and name which kind of moat it has built, if any. Most products have none yet. That's worth noticing too.
