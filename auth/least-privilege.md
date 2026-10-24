# Least privilege

Last reviewed: 2026-10-24

A concept page: give every person and program only the power it needs.

## Problem

Granting broad access is convenient: nothing breaks for lack of a permission, and nobody files a request. But every account, person, or program with more power than it needs is a bigger accident or a bigger breach waiting to happen. When something goes wrong, the damage is limited by what the thing that went wrong was allowed to do.

## The story

In 1999 Grace Okafor ran IT for a forty-person accounting firm in Manchester. She was also, unofficially, the person who fixed printers. Every week someone couldn't install a program, or update a driver, or change a setting, because their account didn't have permission. Each request took her twenty minutes and interrupted something else.

So she made everyone an administrator of their own computer and gave every account full access to the shared drive. The requests stopped. Her weeks got quieter. It was, by any measure she had then, a good decision.

In May 2000 an email arrived with the subject line *ILOVEYOU*. One of the junior accountants opened the attachment. It sent itself to everyone in his address book, and then it began overwriting files: images, documents, anything it could reach. Because his account could reach everything, it reached everything: the whole shared drive, every client's working papers. The backup was four days old. The firm spent a week rebuilding client files from paper, and lost two clients over it.

The virus hadn't been clever. It did what any program run by that user was allowed to do. Grace had made the user powerful to save time, and the virus inherited every bit of that power.

*Before reading on: Grace's convenient permissions had saved hours every week, and then cost a week of work in one morning. How would you have set them up instead?*

She rebuilt it slowly. Ordinary accounts went back to being ordinary. Each team could write to its own folder and only read the rest. She kept a separate administrator account for herself and stopped using it for email. Installing software went back to being a request, but she made it a quick one, with a list of approved programs people could install themselves. The requests came back, fewer than before, and she minded them less. The next time someone opened something they shouldn't, it damaged one person's documents, and they were restored from that morning's backup.

Looking back, Grace thought the lesson was that permissions are a decision about the worst day, not the average one. On the average day, broad access saves time. On the worst day, it decides how much you lose.

## Where it shows up

| Page | Who had too much power | What they got instead |
| --- | --- | --- |
| [7, Strangers on the network](../07-strangers-on-the-network.md) | The website's database account, which could read and delete everything | Read products, write orders and posts, nothing else. "A much smaller room." |
| [9, Buying computers is too slow](../09-buying-computers-is-too-slow.md) | Cloud accounts and services, which often start with broad permissions by default | Only the actions and resources each one uses. |
| [10, Many people, one codebase](../10-many-people-one-codebase.md) | Any single developer, who could put code into the product alone | Required review: nobody ships alone. |
| [12, Machines that learn from data](../12-machines-that-learn-from-data.md) | The support assistant, which could issue credits | It can only suggest a credit; a plain rule decides. |

It shows up elsewhere too: phone apps asking for your contacts, API keys that can do everything, and the old habit of running servers as the all-powerful root user.

What the pages share is that the extra power was always granted for a good reason: convenience, speed, fewer requests. And it was always discovered on a bad day. The fix is the same each time: decide what each party needs, grant only that, and make asking for more quick enough that people don't work around it.

## It really happened

Grace is fictional; ILOVEYOU was real. It spread worldwide in May 2000 and overwrote files on the computers and shared drives it could reach. The principle is older. Jerome Saltzer and Michael Schroeder listed "least privilege" among their design principles for protecting information in 1975: every program and every user should operate using the least set of privileges necessary to do the job ("The Protection of Information in Computer Systems", *Proceedings of the IEEE*). In 2019, an attacker who broke into a web application firewall at Capital One used the permissions of the role it ran under, which could read storage buckets full of customer data it had no reason to touch ([one analysis](https://www.rackspace.com/en-au/blog/capital-one-data-breach-two-security-controls-you-should-review)). The firewall needed to inspect traffic; it didn't need to read customer records.

## What it is

Least privilege means every person, program, and machine gets exactly the access its job requires, and no more. It doesn't prevent mistakes or breaches. It limits what they can reach. It works best when granting access is quick and routine, because a slow process for asking teaches people to ask for everything up front.

## Where it gets misapplied

- **Admin for everyone.** Grace's first year. It saves time on every day except the one that matters.
- **Permissions that only grow.** Access granted for a project and never removed. Review it, or let it expire.
- **One key for everything.** A single API key or service account shared by every program, so one leak exposes all of them.
- **The mirror:** so little access that people can't work. They'll share passwords, copy data to personal laptops, or run things on their own accounts, and you'll have less control than before.

## Connections

- Learning this is also learning [input validation](input-validation.md), because when you can't stop bad instructions getting in, least privilege limits what they can do.
- Learning this is also learning [cloud IAM](cloud-iam.md), because cloud permissions are least privilege made very detailed, and very easy to get wrong.
- Learning this is also learning [multi-tenancy](multi-tenancy.md), because each customer seeing only their own data is least privilege between customers.
- Learning this is also learning [code signing](code-signing.md), because proving who made a change is how review can be enforced.
- Learning this is also learning [prompt injection](../ai/prompt-injection.md), because for language models today, limiting power is the main defence that works.

## Resources

1. Saltzer and Schroeder, "The Protection of Information in Computer Systems" (1975) (start here: the design principles section is short and still right).
2. Ross Anderson, [*Security Engineering*](https://www.cl.cam.ac.uk/~rja14/book.html), the chapters on access control (go deeper). <!-- verify -->
3. Your cloud provider's guide to least-privilege permissions (reference).

## Names you'll hear

- **Root, administrator:** the account that can do anything.
- **RBAC:** role-based access control, permissions granted to roles rather than people.
- **Separation of duties:** no single person can complete a sensitive action alone, like Sofia's required review.
- **Blast radius:** how much breaks when one thing goes wrong.
- **Just-in-time access:** extra permission granted for a short time when needed, then removed.

## Go and look

Find one account, key, or service in something you run and list what it's allowed to do. Then list what it actually does. The difference is your blast radius.
