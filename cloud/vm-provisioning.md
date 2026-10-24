# VM provisioning

Last reviewed: 2026-10-24

A concept page: getting a working server from nothing, repeatably, and why hand-built servers become a problem.

## Problem

A rented virtual machine starts as a bare operating system. Before it can serve anything, it needs software installed, settings changed, users and keys added, and the application deployed. Doing that by hand is easy the first time and impossible to do identically the twentieth. Servers set up by hand drift apart, and the one that matters most is the one nobody can rebuild.

## The story

In 2013 Mateus Rocha looked after the servers for an online magazine: twelve machines rented from a cloud provider, each set up by hand by following a long page on the company wiki. Install these packages, edit these files, add these users, open these ports, start these services. He'd written most of it himself and he was careful. It was how servers were looked after.

One night the main database server's virtual disk failed. The provider replaced the machine in minutes; making it a database server again took Mateus two days. The wiki page was out of date. Over three years, people had made small changes directly on the server, a tuning setting here and a new library there, and recorded some of them. When the rebuilt server went live, the site was slow, and stayed slow for a week, until a colleague remembered a memory setting someone had changed by hand in 2011. Each of the twelve servers, it turned out, was slightly different from the others in ways nobody could list. Mateus had been caring for twelve individuals.

*Before reading on: the servers were set up carefully by hand and had quietly drifted apart, and rebuilding one took days. How would you have made them rebuildable?*

Mateus moved every step from the wiki into code. One set of files described the machines themselves: their size, disks, network and firewall rules, which a tool created in the cloud account. Another described everything installed and configured on them. Both lived in version control and were reviewed like any other change. From then on, nobody changed a server by hand. If a server needed a new setting, the code changed, and the server was rebuilt from it, or replaced with a fresh one. Building a new database server went from two days to twenty minutes, and it came out identical to the last one, every time. Months later, a server failed during a big story's traffic spike, and the replacement was serving within a quarter of an hour.

Looking back, Mateus thought the wiki had described what the servers were meant to be, and the servers had kept changing while the wiki didn't. Making the description the only way to build a server meant the two couldn't drift apart.

## Where it shows up

| Page | The machines | What changed |
| --- | --- | --- |
| [9, Buying computers is too slow](../09-buying-computers-is-too-slow.md) | Machines rented by the hour | Tariq learned to treat machines as things you start and stop, not things with names. |
| [13, Everything still exists at once](../13-everything-still-exists-at-once.md) | Infrastructure drift | Deployed reality and declared configuration moving apart: a runbook for a server that no longer exists. |
| [2, One machine, many programs](../02-one-machine-many-programs.md) | The hypervisor underneath | Every virtual machine is a slice of a physical one. |
| [Managed services](../vendors/managed-services.md) | The step above | A managed service is a provisioned machine someone else looks after. |

It shows up elsewhere too: container images built from a file, test environments created per change, and disaster recovery plans.

What these share is that a server described in code can be rebuilt, compared and reviewed, and a server built by hand can only be remembered.

## It really happened

Mateus is fictional. The shift he made is often summed up as "pets versus cattle", a phrase popularised in cloud talks around 2012: pets have names and are nursed back to health, cattle are numbered and replaced. Netflix described "baking" complete machine images and replacing servers rather than updating them in place, early in its move to AWS. Tools for describing infrastructure as code, such as Puppet (2005), Chef (2009), Ansible (2012) and Terraform (2014), made it practical for ordinary teams.

## What it is

Provisioning is creating machines and preparing them to run software: allocating the virtual machine, its storage and network, then installing and configuring what runs on it. Infrastructure as code describes both in files under version control, applied by tools, so every machine can be recreated identically. Immutable infrastructure goes further: servers are never changed after creation; changes mean building a new image and replacing the old servers.

## Where it gets misapplied

- **Hand changes on live servers.** Each one is a difference nobody will remember.
- **Code that describes servers, plus hand changes as well.** The code is then a wish, not a description.
- **Rebuilding never tested.** If you've never rebuilt a server from code, you don't know that you can.
- **The mirror:** a full infrastructure-as-code setup for one server that hosts a personal blog. A short script and a backup may be enough.

## Connections

- Learning this is also learning [managed services](../vendors/managed-services.md), because they're provisioning someone else does for you.
- Learning this is also learning [cloud IAM](../auth/cloud-iam.md), because every new machine needs an identity with the right permissions.
- Learning this is also learning [build systems and package managers](../tooling/build-systems.md), because building a machine image is a build, and the same rules about declared inputs apply.
- Learning this is also learning [CI pipelines](../tooling/ci.md), because infrastructure changes deserve the same review and testing as code.
- Learning this is also learning [the cost of reliability](../cost/reliability.md), because how fast you can rebuild decides how long an outage lasts.

## Resources

1. Kief Morris, *Infrastructure as Code* (start here).
2. The documentation for an infrastructure-as-code tool, such as Terraform, OpenTofu or Pulumi (go deeper: try describing one small server).
3. Your cloud provider's documentation on machine images and instance startup scripts (reference).

## Names you'll hear

- **Provisioning, configuration management:** creating machines, and setting them up.
- **Infrastructure as code:** describing infrastructure in version-controlled files.
- **Machine image:** a saved disk from which identical servers can be started.
- **Immutable infrastructure:** replacing servers instead of changing them.
- **Pets versus cattle:** servers cared for individually, or replaced without ceremony.
- **Drift:** live infrastructure differing from its description.

## Go and look

Pick one server or environment you depend on and ask how long it would take to rebuild it from scratch, and from what. If the answer is a person's memory, start writing it down as code.
