# Cloud IAM

Last reviewed: 2026-10-24

A concept page: who and what may do which actions on which resources in a cloud account, and why a leaked key can cost a fortune overnight.

## Problem

In a cloud account, anything can be created, read, changed or deleted by anyone holding the right credentials. Every person and every program needs some access, and the easy way to give it is one powerful key, used everywhere. Keys leak, and a key that can do everything does everything for whoever finds it.

## The story

In 2019 Leila Haddad was one of four engineers at a startup making scheduling software for gyms. Early on, someone had created one access key for the cloud account with full administrator rights, and it was used by everything: the web servers, the backup script, the deploy pipeline and, for convenience, each developer's laptop. It was simple. Nobody ever hit a permissions error.

On a Friday evening, a new developer pushed a small side project to a public code repository so a friend could look at it. A configuration file in it contained the key. By the time Leila's phone buzzed with a billing alert on Saturday morning, someone had used the key to start two hundred of the most expensive machines the provider offered, in regions the company had never used, mining cryptocurrency. The overnight bill was larger than the company's monthly revenue. Leila deleted the key, which also took down the website and the backups, because everything used it.

*Before reading on: one key with every permission had leaked, and deleting it broke everything. How would you have set up access instead?*

Leila rebuilt access over the next few weeks. Each service got its own identity with only the permissions it used: the web servers could read and write their database and one storage bucket, the backup job could write to the backup bucket and nothing else, and deploys could update the web servers and nothing more. None of them had long-lived keys at all. The cloud platform gave each running service short-lived credentials automatically, which expired within the hour. People logged in with their own accounts, with multi-factor authentication, and got administrator rights only temporarily, when they asked for them. Code repositories were scanned for anything that looked like a key, before and after pushing. And the account had spending alerts and limits, with expensive regions and machine types switched off entirely.

The provider waived part of the bill. Leila thought the company had been lucky.

Looking back, she thought the single key had made every permission decision once, in the most permissive way possible, and then forgotten it had made any decision at all.

## Where it shows up

| Page | The access | What went wrong, or right |
| --- | --- | --- |
| [9, Buying computers is too slow](../09-buying-computers-is-too-slow.md) | Permissions in a rented account | Who can start, read or delete anything you rent, and the default is usually too much. |
| [Least privilege](least-privilege.md) | Each service's permissions | Only what it uses, so a leak reaches less. |
| [Sessions and tokens](sessions-and-tokens.md) | Credentials for machines | The same rules as for people: short-lived, narrow, revocable. |
| [Multi-tenancy](multi-tenancy.md) | The provider's own isolation | Your account is one tenant among many, and IAM is your boundary inside it. |

It shows up elsewhere too: API keys for third-party services, deploy credentials in build pipelines, database passwords in configuration files, and tokens for coding agents.

What these share is that a credential's power is the size of the damage when it leaks, and that short-lived, narrow credentials make leaks small.

## It really happened

Leila is fictional; her Saturday morning is common enough to have been studied. Researchers at North Carolina State University scanned public GitHub over several months and found secrets, including cloud keys, leaking from over a hundred thousand repositories, many of them still valid ("How Bad Can It Git? Characterizing Secret Leakage in Public GitHub Repositories", NDSS 2019). Cloud providers and code hosts now scan public code for their own key formats and revoke or warn automatically. The larger cloud failure on this theme, the 2019 Capital One breach, came from a role with far more access than its job needed ([least privilege](least-privilege.md)).

## What it is

Cloud identity and access management controls which identities, people, services and machines, may perform which actions on which resources. Good practice gives every workload its own identity with only the permissions it uses, prefers short-lived credentials issued automatically over long-lived keys, requires multi-factor authentication and temporary elevation for people, scans for leaked secrets, and sets spending limits and alerts as a last line of defence.

## Where it gets misapplied

- **One administrator key for everything.** Leila's first year.
- **Long-lived keys in code or configuration.** They end up in repositories, logs and laptops.
- **Permissions copied from an example.** "Allow everything on everything" from a tutorial, shipped to production.
- **The mirror:** permissions so fine-grained that every change needs a ticket and a week. People will work around a process that slow, usually by sharing a powerful key.

## Connections

- Learning this is also learning [least privilege](least-privilege.md), because cloud IAM is least privilege made very detailed.
- Learning this is also learning [sessions and tokens](sessions-and-tokens.md), because cloud credentials are tokens for machines.
- Learning this is also learning [reading a cloud bill](../cost/cloud-bills.md), because a leaked key shows up first as a bill.
- Learning this is also learning [software supply chain](../vendors/supply-chain.md), because build pipelines hold some of the most powerful credentials you have.
- Learning this is also learning [coding agents](../tooling/coding-agents.md), because an agent should run with credentials scoped to its task.

## Resources

1. Your cloud provider's IAM best-practices guide (start here).
2. Meli, McNiece and Reaves, "How Bad Can It Git?" (NDSS 2019) (go deeper: how secrets leak, measured).
3. Your provider's documentation on short-lived credentials for workloads (reference).

## Names you'll hear

- **IAM:** identity and access management.
- **Role, policy:** an identity that services can assume, and the document listing what it may do.
- **Access key:** a long-lived credential, best avoided.
- **Workload identity:** short-lived credentials issued automatically to running services.
- **MFA:** multi-factor authentication, a second proof beyond a password.
- **Secret scanning:** automatically searching code for leaked credentials.

## Go and look

List the credentials that can change things in a cloud account you work with. For each, note who or what holds it, what it can do, and when it expires. Any that never expires is the first to fix.
