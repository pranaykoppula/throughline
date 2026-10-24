# Round trips

Last reviewed: 2026-10-24

A concept page: why the number of times you wait for a reply matters more than how much you send.

## Problem

Every request across a network costs a wait for the reply, set largely by distance, and it costs the same whether you send ten bytes or ten thousand. A design that asks many small questions one after another pays that wait every time. On a slow or distant connection, the waiting is the whole experience.

## The story

In 2011 Ayesha Rahman led the team building a social app's first iPhone version. The backend team had built a tidy, well-documented API, with one endpoint for each kind of thing: a user, a post, a comment, a photo. Ayesha's home screen used it the obvious way. Fetch the list of posts, then for each post fetch its author, its photo and its first comments. The code was clean, and it matched the API's design exactly.

In the office it was fine. The screen loaded in under a second on the company's wifi. Then the app went to a small group of test users, and the feedback was blunt: the home screen took ten seconds or more, and on a train it often never loaded at all.

Ayesha borrowed a phone with a weak mobile signal and watched the requests go out. The home screen made thirty-one of them, most waiting for the one before, because each post's details couldn't be asked for until the list of posts arrived. On wifi each round trip took twenty milliseconds. On the mobile network that day, each took about three hundred. The data itself was small. Thirty-one waits were the problem.

*Before reading on: each request was quick to process and the data was small, but there were thirty-one waits in a row. What would you have changed?*

She asked the backend team for one new endpoint: everything the home screen needed, in one response. They pushed back, reasonably. It broke the tidy design, and the next screen would want its own endpoint. They compromised on a way for the app to say, in one request, exactly which fields it wanted from which related things, and get them all back together. The home screen went from thirty-one round trips to two. On the borrowed phone it loaded in under a second.

Looking back, Ayesha thought the API had been designed for a fast network and clean diagrams. The users were on trains. Counting round trips, not bytes, was the habit she kept.

## Where it shows up

| Page | The round trips | What fixed it |
| --- | --- | --- |
| [5, Machines need to talk](../05-machines-need-to-talk.md) | Lin waited for each block's confirmation before sending the next | Sending several blocks before waiting. TCP does it for everyone now. |
| [6, Anyone can publish](../06-anyone-can-publish.md) | Every click reloaded the whole page from the server | Fetching only the data that changed, in the background. |
| [Latency numbers](latency-numbers.md) | Daniel's search page made a dozen lookups across the Atlantic, one after another | A cache in each region, and asking for all twelve prices at once. |
| [12, Machines that learn from data](../12-machines-that-learn-from-data.md) | Each question to a language model is a round trip, paid in time and tokens | Sending only what each question needs. |

It shows up elsewhere too: database queries made in a loop (the "N+1" problem), connection and encryption handshakes before any data moves, and microservices that call each other in chains.

The pages share one fix in different forms: fewer, larger exchanges instead of many small ones, and doing in parallel whatever doesn't depend on a previous answer.

## It really happened

Ayesha is fictional; her compromise is close to how GraphQL began. Facebook built it in 2012 for its mobile news feed, so that one request could ask for exactly the nested data a screen needed, and released it publicly in 2015 ([Facebook Engineering](https://engineering.fb.com/2015/09/14/core-infra/graphql-a-data-query-language/) <!-- verify -->). HTTP/2, standardised in 2015, let a browser send many requests over one connection at once instead of waiting on each. Every new secure connection still costs extra round trips before the first byte of data, which is why newer protocols work to cut those handshakes down.

## What it is

A round trip is a message going out and its reply coming back. Its cost is mostly distance and the number of network hops, not the size of the message. Total delay is roughly the round-trip time multiplied by the number of round trips that must happen one after another. Reducing that count, by batching requests, sending in parallel, keeping connections open, or moving data closer, is usually the biggest speed-up available.

## Where it gets misapplied

- **Chatty APIs.** One request per thing, in a loop.
- **Testing only on fast networks.** Office wifi hides round-trip costs that users on mobile pay in full.
- **Batching everything into one giant request.** One huge response can be slow to build and wasteful when the screen needs a tenth of it.
- **The mirror:** an endpoint for every screen, forever. That's fast, but it couples the backend to every interface. Ayesha's compromise was a middle path.

## Connections

- Learning this is also learning [latency numbers](latency-numbers.md), because a round trip's cost is set by distance, and the table says how much.
- Learning this is also learning [caching](caching.md), because the fastest round trip is the one you don't make.
- Learning this is also learning [distributions and percentiles](../math/percentiles.md), because a page that waits on many calls pays the tail of each.
- Learning this is also learning [TLS](../auth/tls.md), because a secure connection costs round trips before it carries anything.
- Learning this is also learning [serialization formats](../data/serialization.md), because what you put in each exchange, and how compactly, is the other half of the cost.

## Resources

1. Ilya Grigorik, [*High Performance Browser Networking*](https://hpbn.co/), the early chapters on latency and TCP (start here: free). <!-- verify -->
2. Facebook Engineering, ["GraphQL: A data query language"](https://engineering.fb.com/2015/09/14/core-infra/graphql-a-data-query-language/) (2015) (go deeper: mobile round trips producing a new API style). <!-- verify -->
3. Jacobson and Karels, ["Congestion Avoidance and Control"](https://people.eecs.berkeley.edu/~sylvia/cs268/papers/congavoid.pdf) (1988) (reference: what happens to round trips under load).

## Names you'll hear

- **RTT:** round-trip time.
- **N+1 queries:** one query for a list, then one more for each item in it.
- **Batching, pipelining:** sending many requests together, or sending the next before the last reply arrives.
- **Handshake:** the round trips to set up a connection before data flows.
- **Chatty, chunky:** an interface needing many small exchanges, or a few large ones.

## Go and look

Open your browser's network tools on a page you use every day and count the requests that wait for a previous one before they start. Then try the same page on a throttled connection.
