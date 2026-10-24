# Tokens and context windows

Last reviewed: 2026-10-24

A concept page: the unit a language model reads, writes and bills in, and the limited space it reads from.

## Problem

A language model doesn't see words or pages. It sees tokens, small chunks of text, and it can only consider a fixed number of them at once, its context window. Everything you want it to use has to fit in that window, every token costs money and time, and a bigger window doesn't mean the model uses all of it equally well.

## The story

In 2024 Tomás Reyes built a tool for a law firm that answered questions about contracts. A lawyer uploaded a contract and asked something like *what's the notice period for termination?* The model had just gained a context window large enough to hold a three-hundred-page contract, so Tomás did the obvious thing: send the whole contract with every question. No splitting, no searching, nothing to get wrong. It was simple and, in the demo, it worked.

Two problems appeared within a month. The first was the bill. A three-hundred-page contract was around two hundred thousand tokens, and the lawyers asked dozens of questions per contract. Each question re-sent the entire document and paid for it again. The firm's monthly cost was ten times what Tomás had estimated from the demo, which had used a ten-page contract.

The second problem was worse. The answers were usually right about clauses near the start and the end of a contract, and noticeably less reliable about clauses in the middle. A lawyer caught it giving the wrong notice period. The right one was on page 140, and the model had quoted a different clause from page 3. The whole contract had been in the window. The model just hadn't attended to the middle of it as well.

*Before reading on: the contract fit in the window, but the answers were expensive and weakest in the middle. What would you have sent instead?*

Tomás stopped sending everything. He split each contract into sections once, when it was uploaded, and stored them with an index of what each was about. For each question, he found the handful of sections most likely to contain the answer and sent only those, a few thousand tokens. He put the most relevant section first, and asked the model to quote the clause it relied on, with its page number, so a lawyer could check. Costs fell by more than ninety percent. Accuracy on mid-contract questions went up, because the answer was no longer buried.

Looking back, Tomás thought the big window had tempted him to treat context as free and perfectly read. It was neither. What went into the window was the most important design decision in the whole tool.

## Where it shows up

| Page | The tokens | What it taught |
| --- | --- | --- |
| [12, Machines that learn from data](../12-machines-that-learn-from-data.md) | Nadia's whole help centre, sent with every question | Sending only the three most relevant articles cut the bill by ninety percent and improved the answers. |
| [Prompt injection](prompt-injection.md) | Everything in the window, instructions and material alike | To the model it's all just tokens, which is why hidden instructions work. |
| [Reading a cloud bill](../cost/cloud-bills.md) | Tokens in, tokens out | A design decision wearing a price tag, billed per word. |

It shows up elsewhere too: chat history that grows until it has to be summarised or cut, coding agents deciding which files to read, and the difference in cost between a short answer and a long one.

What these share is that the context window is a small, expensive, fast tier, like core memory on page 1. What you put in it, and in what order, decides both the cost and the quality.

## It really happened

Tomás is fictional; the middle problem was measured. Nelson Liu and colleagues found in 2023 that language models used information best when it was at the beginning or end of a long input, and noticeably worse when it was in the middle, even in models built for long inputs ([Liu et al., "Lost in the Middle"](https://arxiv.org/abs/2307.03172)). The standard response, finding the relevant pieces first and sending only those, is usually called retrieval-augmented generation. Providers have since added ways to reuse a repeated prefix between requests at a lower price, because so many applications send the same long instructions every time.

## What it is

A token is the unit of text a language model processes, often a word or part of a word; in English, roughly three-quarters of a word on average. The context window is the maximum number of tokens the model can consider at once, covering instructions, material, conversation history and its own answer. Cost and time scale with tokens in and out. Models don't attend to all positions equally. So choose what goes in, put what matters where it's used best, and don't re-send what you don't need.

## Where it gets misapplied

- **Filling the window because you can.** Tomás's whole contract. Bigger isn't free or evenly read.
- **Ignoring output tokens.** Asking for long answers when short ones would do; output often costs more per token than input.
- **Unbounded chat history.** Conversations that grow until they're slow, expensive, and cut off at the start without anyone noticing.
- **The mirror:** cutting context so hard the model can't do the job. Retrieval that misses the right section gives a confident wrong answer.

## Connections

- Learning this is also learning [prompt injection](prompt-injection.md), because everything in the window is just tokens, with no built-in difference between instruction and material.
- Learning this is also learning [round trips](../latency/round-trips.md), because each call to a model is a round trip whose cost grows with what you send.
- Learning this is also learning [reading a cloud bill](../cost/cloud-bills.md), because tokens are the line on the bill.
- Learning this is also learning [caching](../latency/caching.md), because reusing a repeated prefix is caching for models.
- Learning this is also learning [access patterns](../data/access-patterns.md), because retrieval is choosing what to read based on the question asked.

## Resources

1. Your model provider's documentation on tokens, context windows and pricing (start here).
2. Liu et al., ["Lost in the Middle: How Language Models Use Long Contexts"](https://arxiv.org/abs/2307.03172) (2023) (go deeper).
3. Simon Willison's blog, which tracks model prices and context sizes as they change (reference). <!-- verify -->

## Names you'll hear

- **Token, tokenizer:** the unit of text, and the program that splits text into tokens.
- **Context window:** how many tokens a model can consider at once.
- **RAG:** retrieval-augmented generation, fetching relevant material and putting only that in the prompt.
- **Prompt caching:** reusing a repeated beginning of a prompt more cheaply.
- **Input and output tokens:** what you send and what the model writes back, usually priced differently.

## Go and look

Take one request your product sends to a language model and count its tokens: instructions, material, history and answer. Then ask which of them the model actually needed.
