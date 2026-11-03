# Information gain

Last reviewed: 2026-11-03

A concept page in the information family: how to choose the next question, so each answer rules out as much as possible. It's how good debugging works, how a guessing game is won, and how a decision tree in machine learning picks its splits.

## Problem

Whenever you're looking for something, such as a bug, a cause, a diagnosis or the right category, you narrow it down by asking questions: running a test, checking a log, asking the user. Some questions narrow things down a lot and some barely at all, and the useless ones often feel the most natural. Without a way to tell them apart, an investigation takes ten times longer than it needs to.

## The story

In 2016 Tobias Weber looked after quality for a company's mobile banking app. A new release had gone out on Monday, and by Tuesday the app was crashing for some users when they opened it. Between the last good release and this one there were four hundred changes from twelve developers.

Tobias had a hunch. A big change to the payments screen had gone in late, and it looked risky. He built the app without it, and the crash was still there. He tried the next most suspicious change, then the next. By Wednesday evening he'd checked eleven changes, each one plausible, and ruled out eleven. Three hundred and eighty-nine to go.

*Before reading on: each check ruled out one change out of four hundred. How would you choose a check that rules out more?*

An older colleague watched him for a minute and asked a different question: does the crash happen if you build the app from the change exactly halfway between the good release and the bad one? Tobias built it. It crashed. So the culprit was somewhere in the first two hundred changes, and the other two hundred were ruled out by one test. He built from the middle of those: no crash. The culprit was in a range of a hundred. Then fifty, twenty-five, thirteen, seven, four, two, one. Nine builds after he'd started, he was looking at a single change, a one-line update to a library that read the device's language settings. It had nothing to do with payments, and he'd never have suspected it.

What struck him was the arithmetic. His hunches had each asked "is it this one?", and the answer was almost always no, so each answer taught him almost nothing. The halfway question had two equally likely answers, so whichever came back, half the possibilities were gone. Four hundred changes needed about nine halvings, because two multiplied by itself nine times is more than four hundred.

He saw the same thing in the support team's scripts a week later. To narrow down crash reports, agents started every call by asking "are you on Android or iPhone?" It felt like the obvious first question. But the crash only happened on Android, and nineteen out of twenty callers were on Android, so the answer was nearly always the same and told the agent almost nothing. Tobias rewrote the script to start with "does it crash before or after you see the login screen?". About half said before and half after, so each answer cut the problem roughly in half. Calls got shorter.

The data science team, it turned out, had a name for what he'd stumbled on. Their model for predicting which customers would close their accounts was a decision tree, a chain of yes-or-no questions about each customer. To build it, the computer tried every possible question at every step and kept the one with the greatest *information gain*: the one whose answers, on average, left the least uncertainty behind.

Looking back, Tobias thought the lesson was counter-intuitive and simple. A good question is one where you genuinely don't know which answer you'll get. If you can predict the answer, asking it teaches you almost nothing, however relevant it feels.

## Where it shows up

| Page | The search | The question that earned its keep |
| --- | --- | --- |
| [Information](information.md) | Any message | A message carries information by ruling out possibilities. A question is the same thing, from the other side. |
| [Profiling](../tooling/profiling.md) | Where the time goes | One measurement of the whole program ruled out more than three weeks of hunches about the matrix routine. |
| [B-trees](../dsa/b-trees.md) | A key among millions | Each disk read answers a question with two hundred possible answers, not two, so three reads find one part in eight million. |
| [12, Machines that learn from data](../12-machines-that-learn-from-data.md) | Spam or not | Graham's filter weighed the words that most changed the odds, and ignored the ones that appeared everywhere. |
| [Statistical significance](../math/statistics.md) | Did the change make a difference? | A test whose result you could predict in advance, like Lucas's two-day button test, isn't telling you anything. |

It shows up elsewhere too: `git bisect`, binary search, medical triage, the game of twenty questions, and every good debugging session.

What these share is one idea: the information an answer gives is measured by how much it narrows things down, and a question gives the most when its answers are equally likely. That's why halving beats hunches, and why the most obvious question is often the least useful.

## It really happened

Tobias is fictional; his tools are real. git has a `bisect` command that does exactly what his colleague suggested: give it a good version and a bad one, and it picks the halfway point each time, so finding one bad change among a thousand takes about ten tests. Ross Quinlan's ID3 algorithm (1986) built decision trees by choosing, at each step, the question with the highest information gain, and its descendants are still widely used in machine learning. Claude Shannon measured how predictable English is with a guessing game in 1951: people guessed the next letter of a text, and the number of guesses they needed showed how much information each letter really carried. The game of twenty questions works because twenty well-chosen yes-or-no answers can distinguish about a million possibilities.

## What it is

Uncertainty can be measured as the number of yes-or-no questions needed to pin down the answer. With N equally likely possibilities, that's about log₂ N: ten questions for a thousand possibilities, twenty for a million. A question's information gain is how much it reduces that uncertainty on average. It's largest when the possible answers are equally likely, and close to zero when one answer is nearly certain. A question with a 50/50 answer gives a full bit; one with a 95/5 answer gives less than a third of a bit, even though it can feel more relevant. Decision trees, binary search and bisection all choose their questions this way.

## Where it gets misapplied

- **Checking suspects one at a time.** Each "is it this one?" usually answers "no" and rules out one possibility.
- **The obvious first question.** If nearly everyone gives the same answer, it isn't narrowing anything.
- **Questions that split well but don't matter.** Information gain is about the question you're trying to answer; a split that divides users evenly by birth month tells you nothing about the bug.
- **The mirror:** bisecting when you already know the answer. If the error message names the file and line, read it first.

## Connections

- Learning this is also learning [information](information.md), because information gain is entropy before the question minus entropy after it.
- Learning this is also learning [profiling](../tooling/profiling.md), because a good measurement is a question chosen to rule out the most.
- Learning this is also learning [B-trees](../dsa/b-trees.md), because each wide node answers a many-way question in one read.
- Learning this is also learning [statistical significance](../math/statistics.md), because both are about how much an observation should change what you believe.
- Learning this is also learning [labels and training data](../data/labels.md), because a decision tree can only find the questions its data lets it ask.
- Learning this is also learning [state estimation](../signals/state-estimation.md), because an estimator weighs each new reading by how much it reduces uncertainty, continuously.

## Resources

1. The `git bisect` documentation (start here: the idea, as a tool you can use today).
2. Any introduction to decision trees and entropy, such as the chapter in *An Introduction to Statistical Learning* by James, Witten, Hastie and Tibshirani, which is free online (go deeper).
3. Claude Shannon, "Prediction and Entropy of Printed English" (1951) (reference: the guessing game).

## Names you'll hear

- **Bit:** the information in one answer between two equally likely options.
- **Entropy:** how much uncertainty is left, in bits.
- **Information gain:** how much a question reduces entropy, on average.
- **Binary search, bisection:** halving the possibilities with each question.
- **Decision tree:** a model that classifies by asking a sequence of questions chosen for information gain.
- **Twenty questions:** the game, and the reason 2²⁰, about a million, is a useful number to remember.

## Go and look

Next time you debug something, write down your next check before you run it, and how likely you think each answer is. If you're 90% sure of the answer, find a check you're less sure about.
