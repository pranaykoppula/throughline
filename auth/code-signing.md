# Code signing

Last reviewed: 2026-10-24

A concept page: proving who made a piece of software, and that nobody changed it on the way, and what that proof doesn't cover.

## Problem

Software travels a long way from the people who wrote it to the machine that runs it: build servers, download sites, mirrors, update systems. Anyone who can change it along the way can make it do anything. The person installing it needs a way to check that it's exactly what its makers released.

## The story

In 2009 Harriet Cole ran engineering at a small company that made accounting software for shops. Customers downloaded new versions from the company's website, and the app checked for updates and installed them automatically. To guard against corrupted downloads, Harriet published a checksum of each release on the download page, and the updater compared the file's hash with it before installing.

One Friday a customer phoned to ask why his antivirus was complaining about the update. Harriet found that someone had broken into the web server and replaced the installer with one that also installed a program for stealing card details. They had replaced the published checksum too, with the hash of their own file. The updater had checked the file against the checksum, found that they matched, and installed it on every shop that updated that day. The checksum had proved the file was the one on the website. It couldn't prove the file on the website was the company's.

*Before reading on: an attacker who controlled the server could change both the file and the checksum. What would the updater need to check instead?*

Harriet moved the proof somewhere the web server couldn't reach. She generated a signing key pair. The private key lived on a single machine that never connected to the internet, in a locked cupboard, and was used only to sign releases. The matching public key was built into the app itself. The updater now refused any file unless it carried a valid signature from that private key. Breaking into the web server let an attacker change files, but not sign them. Customers could also check the signature themselves, because the operating system recognised it.

Ten years later she read about an attack that went one step further, and it changed how she thought about the whole thing. Attackers hadn't touched the download servers at all. They'd got into the company's build system and inserted their code while the software was being compiled. The result was signed with the company's real key, in the usual way, because the build system was trusted to produce what got signed. The signature was perfectly valid. It proved the software came from that company. It said nothing about whether the company's own build had been tampered with.

Looking back, Harriet thought a signature answered exactly one question: did this come from the holder of this key, unchanged since? That question mattered enormously. But the key holder was only as trustworthy as everything that fed into what they signed.

## Where it shows up

| Page | What's signed | What the signature proves |
| --- | --- | --- |
| [TLS](tls.md) | A server's certificate | That this key belongs to this domain, vouched for by an authority the browser trusts. |
| [Software supply chain](../vendors/supply-chain.md) | Packages and their provenance | That a package came from who it claims, not that its author is trustworthy. |
| [Merkle DAGs](../dsa/merkle-dags.md) | A root hash | Signing one hash at the top signs everything beneath it, as signed git tags do. |
| [Least privilege](least-privilege.md) | Commits and releases | Who made each change, which is what makes required review enforceable. |

It shows up elsewhere too: phone app stores, operating system updates, drivers, browser extensions, and container images.

What these share is the same public-key idea: anyone can check with the public key, only the holder of the private key can sign, so guarding the private key, and what gets signed, is everything.

## It really happened

Harriet is fictional; the attack she read about was SolarWinds. In 2020 it emerged that attackers had compromised SolarWinds' build environment and inserted a backdoor into its Orion software during compilation. The updates were signed with SolarWinds' legitimate certificate and installed by thousands of customers ([The Register](https://www.theregister.com/2021/01/12/solarwinds_tech_analysis_crowdstrike/)). Ten years earlier, the Stuxnet worm had used stolen code-signing certificates to make its drivers look legitimate. Both showed that a signature is only as good as the key, and the process behind it.

## What it is

Code signing attaches a digital signature, made with a private key, to software or its hash. Anyone with the matching public key can verify that the software is unchanged and came from the key's holder. Keys are usually vouched for by certificates. Signing protects the path from release to installation. It doesn't protect against a compromised key, a compromised build, or a malicious author, which is why keys are kept offline or in hardware and builds are increasingly made reproducible and verified.

## Where it gets misapplied

- **A checksum next to the file.** Harriet's first design: whoever can change one can change both.
- **Signing keys on everyday machines.** A key on a build server or a laptop is a key an attacker can use.
- **Treating "signed" as "safe".** A signature identifies the source, not the intent or quality.
- **The mirror:** turning off signature checks because they're inconvenient during development, and shipping that setting.

## Connections

- Learning this is also learning [TLS](tls.md), because certificates are signatures on public keys.
- Learning this is also learning [software supply chain](../vendors/supply-chain.md), because signing protects one link in the chain, not the whole of it.
- Learning this is also learning [hashing](../dsa/hashing.md), because what's actually signed is usually a hash of the software.
- Learning this is also learning [Merkle DAGs](../dsa/merkle-dags.md), because signing a root hash covers a whole tree.
- Learning this is also learning [CI pipelines](../tooling/ci.md), because the build system is what gets signed, and SolarWinds showed it's a target.

## Resources

1. [Sigstore](https://www.sigstore.dev/) documentation (start here: modern signing for open-source software, and why it exists). <!-- verify -->
2. Coverage of the SolarWinds build compromise, such as [The Register's](https://www.theregister.com/2021/01/12/solarwinds_tech_analysis_crowdstrike/) (go deeper: how a signed update went wrong).
3. [Reproducible Builds](https://reproducible-builds.org/) (reference: making it possible to check that a binary matches its source). <!-- verify -->

## Names you'll hear

- **Signature, private key, public key:** the proof, what makes it, and what checks it.
- **Certificate:** a signed statement tying a public key to a name.
- **Reproducible build:** a build that always produces identical output from the same source, so anyone can check it.
- **HSM:** a hardware security module, a device that holds keys and signs without letting them out.
- **Provenance:** a signed record of how and where something was built.

## Go and look

Find out how the software you ship is signed, if it is: where the private key lives, who can use it, and what would happen if the build server that feeds it were compromised.
