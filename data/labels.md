# Labels and training data

Last reviewed: 2026-10-24

A concept page: a learned model is only as good as the examples it learned from, and the people who labelled them.

## Problem

A model learns to imitate the answers in its training data. Those answers, the labels, usually come from people: users clicking buttons, raters paid by the task, experts with limited time. Labels can be wrong, inconsistent, or biased in ways nobody noticed, and the model learns all of it, faithfully, then repeats it with confidence.

## The story

In 2018 Grace Mwangi led the team building a classifier to flag abusive comments on a large discussion site. Training data came from raters, contractors who were shown comments and asked "abusive or not?" Each comment went to three raters and the majority answer became the label. It was the standard approach, and the first model's accuracy, measured against more of the same labels, was ninety-four percent.

In use, the model made two kinds of mistakes that worried her. It flagged a lot of perfectly friendly comments written in certain dialects of English, while missing sarcastic abuse phrased politely. Grace pulled a sample of the training data and labelled it herself, with two colleagues, slowly and carefully. On easy comments they agreed with the raters almost always. On hard ones, they disagreed with the raters' majority about a third of the time. The raters had been paid per comment, had about ten seconds each, and many weren't familiar with the dialects in question. Their quick judgements had become the labels, and the model had learned the raters' shortcuts, not the idea of abuse.

The ninety-four percent hadn't been a lie. It measured how well the model agreed with the raters. It said nothing about how well the raters agreed with the truth.

*Before reading on: the model matched its labels well, and the labels were wrong on exactly the hard cases. How would you have fixed the data?*

Grace changed how labels were made rather than how the model was trained. Raters got clearer guidelines with worked examples of hard cases, more time per comment, and pay by the hour instead of by the item. Comments where raters disagreed weren't settled by majority vote anymore. They went to a smaller group of trained reviewers, including people familiar with the relevant dialects. She built a separate test set labelled with great care by experts, and measured the model against that, sliced by dialect and topic, not against the raters' labels. The headline accuracy went down a few points, because it was now measured honestly. The complaints went down much further.

Looking back, Grace thought she'd learned to ask a question before training anything: who decided these labels, how quickly, and how often would two of them have disagreed?

## Where it shows up

| Page | The labels | What the model learned |
| --- | --- | --- |
| [12, Machines that learn from data](../12-machines-that-learn-from-data.md) | Nadia's users clicking "report spam" on newsletters they were tired of | To block newsletters people had signed up for. Exactly what it was taught. |
| [Statistical significance](../math/statistics.md) | Patterns in noisy data | A model trained on noise learns noise. |
| [Distributions and percentiles](../math/percentiles.md) | Accuracy overall against accuracy by group | A good overall number can hide one group's poor one. |
| [Profiling](../tooling/profiling.md) | Measuring the right thing | Accuracy against bad labels measures agreement with the labellers, not correctness. |

It shows up elsewhere too: medical imaging datasets, recommendation systems trained on clicks, fraud models trained on past decisions, and language models trained on whatever text was collected.

What these share is that every learned model inherits the judgement of whoever produced its examples. Checking that judgement is part of building the model.

## It really happened

Grace is fictional; label errors are well measured. In 2021 Curtis Northcutt and colleagues estimated that the test sets of ten widely used machine-learning benchmarks contained an average of about 3.4% wrongly labelled examples, enough to change which models appeared best ("Pervasive Label Errors in Test Sets Destabilize Machine Learning Benchmarks", 2021). The [Netflix Prize](../12-machines-that-learn-from-data.md) showed the related point that accuracy on a fixed dataset isn't everything.

## What it is

Labels are the target answers a supervised model learns from. Their quality is limited by who produced them, under what instructions, with how much time and context, and how they resolved disagreement. Good practice measures agreement between labellers, sends disputed cases to experts, keeps a carefully labelled evaluation set separate from training data, and evaluates performance by slice, not only overall.

## Where it gets misapplied

- **Majority vote on hard cases.** Three rushed guesses don't make a right answer.
- **Measuring against the same kind of labels you trained on.** It measures consistency, not correctness.
- **Clicks as labels.** What users click isn't always what they want.
- **The mirror:** endlessly perfecting labels before training anything. Some noise is tolerable; find out how much by measuring.

## Connections

- Learning this is also learning [statistical significance](../math/statistics.md), because telling real patterns from noise starts with the data.
- Learning this is also learning [distributions and percentiles](../math/percentiles.md), because evaluating by slice is how hidden failures show up.
- Learning this is also learning [data modelling](modelling.md), because what you decide to record, and how, limits what can be learned from it.
- Learning this is also learning [tokens and context windows](../ai/tokens.md), because for language models, the context you provide is a kind of label for the task.
- Learning this is also learning [consistency](consistency.md), because a trained model is a copy of the world as it was when the labels were made.

## Resources

1. Northcutt, Athalye and Mueller, "Pervasive Label Errors in Test Sets Destabilize Machine Learning Benchmarks" (2021) (start here).
2. Sculley et al., "Hidden Technical Debt in Machine Learning Systems" (2015) (go deeper: data as the long-term cost of ML).
3. Your labelling platform's guidance on agreement metrics (reference).

## Names you'll hear

- **Label, ground truth:** the answer a model is trained to give, and the true answer it's supposed to reflect.
- **Inter-annotator agreement:** how often labellers agree, a ceiling on how good labels can be.
- **Held-out set, evaluation set:** data kept aside to test the model, never trained on.
- **Label noise:** wrong or inconsistent labels.
- **Slice:** a subset of data, such as one language or region, evaluated on its own.

## Go and look

Find a dataset with labels in something you work on, take twenty labelled examples, and label them yourself without looking. Count how often you agree.
