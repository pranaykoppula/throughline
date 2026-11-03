# Power and predictability

Last reviewed: 2026-11-03

A concept page: the more a language can express, the less you can know about what a program written in it will do. Regular expressions, parsers and Turing machines are rungs on one ladder, and every rung up trades certainty for power.

## Problem

Engineers pick languages constantly, often without noticing: a pattern for matching text, a configuration format, a template language, a query language, a rules engine. A more powerful one lets people say more, so it's the natural choice. But power has a price. The more a language can express, the less anyone can say in advance about a program written in it: how long it will run, what it will touch, or whether it will finish at all. When the input comes from strangers, that uncertainty is something they can use.

## The story

In 2009 Selim Demir ran the spam filter at a mail provider with a few million customers. The filter's rules were written as regular expressions, short patterns that matched text, so that the anti-spam analysts could add a rule within minutes of a new campaign appearing, without waiting for an engineer. Selim used the standard regular-expression library of the language the filter was written in. It was fast, well documented and full of features. The analysts loved its extras, such as *backreferences*, which let a pattern say "the same word again", and they wrote hundreds of rules with them.

One Tuesday afternoon a new rule went live to catch spam that hid words behind repeated punctuation. Within ten minutes every filtering server was at full CPU and incoming mail was piling up in queues. The rule had a pattern repeated inside another repeated pattern. On ordinary email it finished instantly. But one spam campaign included a long line that *almost* matched, and on that line the library tried one way of splitting the text between the two repetitions, failed at the very end, went back, and tried another way, and another. The number of ways grew exponentially with the length of the line. A single message could occupy a processor for minutes. Selim pulled the rule, and the queues took the rest of the afternoon to drain.

*Before reading on: the rule was correct, the library was standard, and one email could stall a server. What would you have changed?*

Selim learned that there were two quite different kinds of engine behind the same syntax. Some read the text once, from left to right, keeping track of every possible match at the same time. Their running time grew in step with the length of the input, whatever the pattern. They could do that because a true regular expression needs only a fixed amount of memory: which of a finite number of states the match is in. The engine he'd been using instead tried possibilities one at a time and backtracked on failure. That was what let it support backreferences, which need to remember earlier text and so can't be done with a fixed number of states. The extra power and the unpredictable running time were the same thing.

He moved the filter to an engine that guaranteed linear time. It refused patterns that needed backreferences. About thirty rules had to be rewritten, and the five that genuinely needed to compare one part of a message with another became small pieces of ordinary code, reviewed and tested like any other change. Every rule now ran against a set of deliberately hostile test messages before it went live, and every message had a time budget. When an analyst later asked for a rule that matched balanced brackets in HTML, Selim explained that no regular expression could do it, because counting nesting to any depth needs memory that grows, which is what a parser's stack is for. And when another asked whether the rule language could have loops and functions, he said no, and wrote down why.

Looking back, Selim thought he'd chosen the library for everything it could do, and that was exactly the problem. Less power had given him something he hadn't known to want: knowing, before any rule ran, the longest it could possibly take.

## Where it shows up

| Page | The language | What its power cost, or what limiting it bought |
| --- | --- | --- |
| [State machines](state-machines.md) | Chloe's nine order states | The bottom rung: a finite list of states and moves, so every order can be checked and nothing impossible can happen. |
| [Computability](computability.md) | Viktor's virus scanner, against programs that can do anything | The top rung: once a language can express everything, no tool can predict in general what its programs will do. |
| [Hashing](hashing.md) | A hash table fed keys chosen by strangers | The same attack as Selim's email: choose the input that makes the worst case happen. |
| [Input validation](../auth/input-validation.md) | Checks run on input from outside | A check whose running time an attacker controls is itself a way in. |
| [Build systems and package managers](../tooling/build-systems.md) | Build files | A build file that can run arbitrary code can't be analysed without running it, so the build can't know what depends on what. |

It shows up elsewhere too: parsing HTML with regular expressions, configuration formats that grew conditionals and loops, template languages, spreadsheets (Excel's formulas became able to express any computation in 2020), smart contracts that charge for every step so that programs must stop, and forcing a language model to produce valid JSON by running a grammar alongside it.

What these share is the ladder. A language with a fixed amount of memory can always be checked and always finishes quickly. Add a stack and it can handle nesting, and still always finishes. Add unlimited memory and it can do anything, and you can no longer know in general what it will do. Each rung is worth climbing only if you need what's on it.

## It really happened

Selim is fictional; both kinds of engine are real. Stephen Kleene described regular languages in the early 1950s. In 1968 Ken Thompson published a way of compiling a regular expression into a machine that reads text once, in time proportional to its length. Many later libraries, following Perl, used backtracking instead, to support features such as backreferences, and gave up that guarantee. Russ Cox's 2007 article explaining the difference became widely read, and Google's RE2 library (2010) was built to give the guarantee back.

On 20 July 2016 Stack Overflow went down because a post contained about 20,000 consecutive whitespace characters, and a regular expression meant to trim whitespace from the ends of lines backtracked over them. It was replaced with a simple substring function ([ADTmag's account of the postmortem](https://adtmag.com/blogs/dev-watch/2016/07/stack-overflow-crash.aspx) <!-- verify -->). On 2 July 2019 a single new rule in Cloudflare's web application firewall contained a regular expression that backtracked badly, and exhausted the CPU on every core serving web traffic across its network worldwide for about 27 minutes ([Cloudflare's postmortem](https://blog.cloudflare.com/details-of-the-cloudflare-outage-on-july-2-2019/)).

The ladder itself was set out by Noam Chomsky in 1956, as a way of classifying grammars of human language. In 2006 Tim Berners-Lee and Noah Mendelsohn published "The Rule of Least Power" for the W3C: choose the least powerful language suitable for a purpose, because what it says can then be analysed and reused ([W3C TAG finding](https://www.w3.org/2001/tag/doc/leastPower-2006-2-13.html)). Bazel's configuration language, Starlark, follows the same idea and forbids recursion.

## What it is

Languages form a ladder of power, often called the Chomsky hierarchy. *Regular* languages are recognised by finite automata, which have a fixed number of states and no other memory; true regular expressions describe them, and they can be matched in linear time. *Context-free* languages add a stack, which is enough for nesting such as brackets, programming languages and JSON; parsers handle them, and still always finish. *Turing-complete* languages have unbounded memory and can express any computation, which is why the halting problem and its relatives apply to them. The rule of least power says to choose the lowest rung that does the job, and to notice when a convenient feature quietly climbs a rung.

## Where it gets misapplied

- **A backtracking engine on input strangers control.** Selim's afternoon, Stack Overflow's outage and Cloudflare's.
- **Regular expressions for nested structure.** HTML, JSON and code need a parser.
- **The configuration format that became a programming language.** Each feature made sense; together they made something nobody can check without running it.
- **The mirror:** contorting a weak language to do a strong one's job. A thousand-line configuration file full of templating tricks is worse than a short, honest program that's reviewed and tested like one.

## Connections

- Learning this is also learning [state machines](state-machines.md), because a finite automaton is a state machine reading text, and it's the bottom rung of the ladder.
- Learning this is also learning [computability](computability.md), because the top rung is where Turing's limits begin.
- Learning this is also learning [hashing](hashing.md), because both are attacks on the worst case, where the attacker chooses the input.
- Learning this is also learning [input validation](../auth/input-validation.md), because the check that keeps bad input out can be the thing bad input attacks.
- Learning this is also learning [language](../info/language.md), because the ladder began as a theory of grammar for human languages.
- Learning this is also learning [tokens and context windows](../ai/tokens.md), because a model can be made to produce valid structured output by allowing only the tokens a grammar accepts next.

## Resources

1. Russ Cox, ["Regular Expression Matching Can Be Simple And Fast"](https://swtch.com/~rsc/regexp/regexp1.html) (2007) (start here: the two kinds of engine, with graphs that make the difference obvious). <!-- verify -->
2. Cloudflare, ["Details of the Cloudflare outage on July 2, 2019"](https://blog.cloudflare.com/details-of-the-cloudflare-outage-on-july-2-2019/) (go deeper: a frank postmortem, with an appendix on backtracking).
3. Tim Berners-Lee and Noah Mendelsohn, ["The Rule of Least Power"](https://www.w3.org/2001/tag/doc/leastPower-2006-2-13.html) (2006) (short and general).
4. Michael Sipser, *Introduction to the Theory of Computation* (reference: the whole ladder, carefully).

## Names you'll hear

- **Regular expression, regular language:** a pattern, and the kind of text a fixed-memory machine can recognise.
- **Finite automaton (DFA, NFA):** a machine with a fixed set of states that reads input one symbol at a time.
- **Backtracking, catastrophic backtracking, ReDoS:** trying alternatives one by one, its exponential worst case, and the denial-of-service attack that exploits it.
- **Context-free grammar, parser, pushdown automaton:** rules for nested structure, and the stack-using machinery that reads it.
- **Turing-complete:** able to express any computation, and so subject to the halting problem.
- **Chomsky hierarchy:** the ladder of language classes.
- **Rule of least power:** choose the least powerful language that does the job.

## Go and look

Find a regular expression in something you run that's applied to input from users. Find out whether your language's engine backtracks, then time the pattern against a long string that nearly matches. If the time grows much faster than the string, you've found Selim's Tuesday.
