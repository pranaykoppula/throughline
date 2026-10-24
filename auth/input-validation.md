# Input validation

Last reviewed: 2026-10-24

A concept page: why input from outside must be treated as data, never as instructions.

## Problem

A system that takes input from outsiders, and also takes instructions from somewhere, will eventually meet an outsider who sends instructions disguised as input. If data and commands travel together, nothing but care keeps them apart.

## The story

In 1964 Frank Ruiz was an engineer at a long-distance telephone company in the American Midwest. Long-distance lines between exchanges carried a steady tone at 2600 hertz whenever they were idle. When a call ended, the tone came back, and the exchange at the far end knew the line was free and listened for the next number. It was a tidy design. The control signals travelled down the same line as the voices, so no extra wiring was needed.

That spring the billing department noticed something odd: long-distance calls that had happened but never been charged. Frank traced several of them. Each had started as a call to a free number. Then, partway through, someone on the line had played a pure 2600-hertz tone. The far exchange heard it, assumed the call was over, and waited for dialling. The caller then sent tones for whatever number they liked, anywhere in the country, while the billing system still thought they were on a free call. One of them, Frank later learned, had used a toy whistle from a cereal box that happened to hit the note.

The first fixes were filters. Exchanges were changed to ignore the tone if it arrived too early, or too briefly, or alongside other sounds. Each filter stopped one trick, and a few months later a new one appeared. People built small electronic boxes that played the tones perfectly. Frank came to dread new filters, because each one meant the next box would be more careful.

*Before reading on: the network listened for instructions on the same line that carried callers' voices. Filtering what callers sent never quite worked. What would you have changed?*

The real fix took years and cost a fortune, and Frank only saw its start. The control signals were moved off the voice line entirely, onto a separate data network between exchanges that callers had no way to reach. A caller could whistle any note they liked; the exchanges were no longer listening on that line. Nobody needed to filter the tones any more, because the tones no longer meant anything.

Looking back, Frank thought the whole episode came from one convenient decision: letting the line that carried strangers' sound also carry the network's commands. Every filter had been an attempt to tell the two apart after mixing them. The only thing that really worked was never mixing them in the first place.

## Where it shows up

| Page | The shared channel | The fix |
| --- | --- | --- |
| [6, Anyone can publish](../06-anyone-can-publish.md) | The browser sends requests the server acts on, and anyone can edit what their browser sends | The server checks everything; nothing the client says is taken on trust. |
| [7, Strangers on the network](../07-strangers-on-the-network.md) | A search term pasted into a database command | Parameterised queries: the input goes on a separate channel from the command, Frank's fix in software. |
| [12, Machines that learn from data](../12-machines-that-learn-from-data.md) | A customer's message and the assistant's instructions, in one prompt | No separate channel exists yet, so the model's power is limited instead ([least privilege](least-privilege.md)). |

It shows up elsewhere too: scripts injected into web pages, shell commands built from filenames, and spreadsheets that run formulas typed into a form.

The pages show the order of preference. First, separate the channels, so input can't be read as instructions at all, as with parameterised queries and the telephone company's separate signalling network. Where you can't separate them, check input against what's allowed instead of trying to spot what's forbidden. And where you can't reliably check either, as with language models today, limit what any instruction can do.

## It really happened

Frank is fictional; the tones were real. Long-distance trunks in North America used a 2600 Hz tone for in-band signalling, and "blue boxes" that reproduced it let people route calls for free. Telephone companies eventually moved to common-channel signalling, carrying control messages on a separate network callers couldn't reach, which made the trick impossible ([Blue box](https://en.wikipedia.org/wiki/Blue_box)). Forty years later, the same mistake had a new name. SQL injection, where text typed into a web form is run as a database command, has been near the top of the OWASP list of web risks for most of its history. In 2022 Simon Willison named the version that affects language models *prompt injection*, because no reliable way yet exists to separate a model's instructions from its input ([page 12](../12-machines-that-learn-from-data.md)).

## What it is

Input validation is the rule that anything crossing a trust boundary is data until proven otherwise. The strongest form isn't checking at all; it's structural. Input and instructions travel on separate channels, so input can't become instructions. Where that isn't possible, input is checked against an allow-list of what's expected. And where neither works, the system limits the damage any instruction can do.

## Where it gets misapplied

- **Block-lists.** Filtering out known-bad input is Frank's filters: each one invites a cleverer attack. Define what's allowed instead.
- **Validating only in the browser.** Checks in the client are for the user's convenience; the server must check again ([page 6](../06-anyone-can-publish.md)).
- **Escaping by hand.** Building commands by gluing strings together and remembering to escape them. Use interfaces that keep data and commands apart.
- **The mirror:** rejecting legitimate input. Names with apostrophes, addresses with accents, and emails with plus signs are real. Over-strict validation breaks things for real people.

## Connections

- Learning this is also learning [least privilege](least-privilege.md), because when you can't stop instructions getting through, you limit what they can do.
- Learning this is also learning [prompt injection](../ai/prompt-injection.md), because it's this problem without a separate channel.
- Learning this is also learning [serialization formats](../data/serialization.md), because parsing input safely starts with a format that can't smuggle code.
- Learning this is also learning [hashing](../dsa/hashing.md), because hash flooding was strangers choosing inputs designed to hurt.
- Learning this is also learning [TLS](tls.md), because knowing who sent the input is a different question from knowing it's safe, and both matter.

## Resources

1. [OWASP Top Ten](https://owasp.org/www-project-top-ten/) (start here: injection has been on it since the beginning). <!-- verify -->
2. [OWASP SQL Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html) (the practical rules). <!-- verify -->
3. Simon Willison's writing on [prompt injection](https://simonwillison.net/tags/prompt-injection/) (go deeper: the unsolved version). <!-- verify -->
4. Phil Lapsley, *Exploding the Phone* (2013) (reference: the full history of the telephone tones).

## Names you'll hear

- **Injection:** input that ends up being run as code: SQL injection, command injection, prompt injection.
- **In-band and out-of-band signalling:** control signals on the same channel as data, or a separate one.
- **Parameterised query, prepared statement:** sending a database the command and the data separately.
- **Allow-list, block-list:** defining what's permitted, or what's forbidden.
- **XSS (cross-site scripting):** injecting script into a web page other users will load.

## Go and look

Find one place in something you've built where text from a user ends up inside a command: a database query, a shell call, a prompt, a template. Check whether it travels on its own channel or is glued into the command.
