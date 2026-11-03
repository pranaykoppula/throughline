# Sampling and observation

Last reviewed: 2026-11-03

A concept page in the information family: data only contains what something was built to notice, when it happened to look, and silence is not good news.

## Problem

Every record of the world comes from a sensor, a log line, a form or a person, and each one sees only some things, some of the time. Between samples, things happen that nobody recorded. Some things are never recorded at all, because nothing was built to notice them. And when data is missing, it's tempting to read the gap as "nothing happened". The absence of an observation isn't an observation of absence.

## The story

In 2019 Kofi Mensah built the monitoring system for a company that distributed vaccines to two hundred pharmacies and clinics. Vaccines had to stay between 2 and 8 degrees, so every fridge got a small wireless sensor. To make the batteries last a year and keep mobile data costs down, each sensor measured the temperature every thirty minutes and sent its readings once an hour. The dashboard showed every fridge as a green square if its latest reading was in range, and raised an alarm if a reading wasn't. It was simple and cheap, and for six months it showed green almost everywhere.

Then a pharmacist noticed that a tray of vials felt warm, and the fridge was checked by hand. Its door seal had failed. All night, the fridge had been warming to fourteen degrees, then cooling as the compressor fought back, again and again, every forty minutes or so. The sensor had looked twice an hour, and by bad luck its readings had kept landing in the cool part of the cycle. Every one was in range. The fridge had spent hours too warm, and the data said it never had.

A month later, a clinic's fridge failed completely over a long weekend. Its sensor's battery had died on Friday afternoon, and the clinic's area had patchy mobile coverage anyway. The dashboard showed the fridge's last reading, 5 degrees, in green, all weekend. No reading meant no out-of-range reading, so no alarm. The vaccines were found on Tuesday and thrown away. Nobody had been given a spoiled dose, which Kofi knew was luck.

*Before reading on: one fridge went wrong between samples, and another went silent and looked fine. What would you have changed?*

Kofi changed what the sensors recorded and what the dashboard believed. Each sensor still reported every half hour, but it now checked the temperature every minute and kept the lowest and highest values since the last report. A fridge that spent twenty minutes at fourteen degrees reported a maximum of fourteen, wherever the half-hour reading happened to land. Each sensor also sent a short heartbeat, and a fridge whose sensor hadn't been heard from in ninety minutes turned grey on the dashboard, not green, with its own alarm: *no data*. A grey square was treated as seriously as a red one. Batteries were monitored too, with replacements sent before they died. And for the first time, the team wrote down what the sensors couldn't see at all, such as whether the door was open or the power was on, and added door sensors to the fridges that held the most expensive stock.

Looking back, Kofi thought he'd built a system that answered the question "is the latest reading in range?" and treated it as "is the fridge all right?" They were different questions. The first was about what the sensor had seen. The second was about the fridge, and the answer included everything the sensor hadn't.

## Where it shows up

| Page | What was observed | What wasn't |
| --- | --- | --- |
| [11, Software that must not go down](../11-software-that-must-not-go-down.md) | Whether each server was up | Whether anyone could buy a ticket, until Rosa built a robot that tried every minute. |
| [Labels and training data](../data/labels.md) | What raters had ten seconds to judge | The hard cases, and the dialects the raters didn't know. |
| [12, Machines that learn from data](../12-machines-that-learn-from-data.md) | Spam that users reported | Spam nobody bothered to report, and newsletters reported for the wrong reason. |
| [Distributions and percentiles](../math/percentiles.md) | Overall averages | The small group whose experience was completely different. |
| [Statistical significance](../math/statistics.md) | Two days of a button test | Every other day of the week, and the noise that would have shown up given time. |
| [Sampling and aliasing](../signals/sampling.md) | Henrik's bearings, two hundred times a second | A fast, dangerous vibration, which the samples drew as a slow, harmless one. |

It shows up elsewhere too: logs that record errors but not slow successes, analytics that only see users who didn't block tracking, surveys answered only by those who chose to answer, and crash reports that never arrive from devices that crashed too hard to send them.

What these share is a gap between the world and the record of it. The record is shaped by when it looked, what it was built to see, and who or what survived to be counted. Missing data is its own signal, and the most important question about any dataset is what it couldn't have contained.

## It really happened

Kofi is fictional. The most consequential missing data in engineering history may be a chart. The night before the space shuttle Challenger's launch in January 1986, engineers and managers discussed whether cold weather could harm the rubber O-rings sealing the booster joints. The chart they discussed plotted O-ring problems against temperature for the flights that had had problems, and on those flights alone no clear trend appeared. The flights with no O-ring problems, almost all launched in warm weather, were left out. The presidential commission's report later showed both charts, and concluded that a careful analysis of the whole flight history would have revealed the correlation with low temperature ([Rogers Commission report](https://www.nasa.gov/history/rogersrep/v1p146.htm)). Challenger launched at a temperature colder than any previous flight.

During the Second World War, the statistician Abraham Wald wrote a series of memos on estimating aircraft vulnerability from the damage on planes that came back. The planes that didn't come back couldn't be inspected, and their missing damage was the important part. The popular retelling, in which Wald simply told the military to armour the places without bullet holes, is tidier than the record ([AMS, "The Legend of Abraham Wald"](https://www.ams.org/samplings/feature-column/fc-2016-06)). The idea it illustrates, now called survivorship bias, is sound. And Harry Nyquist (1928) and Claude Shannon (1949) showed how often a changing signal must be sampled to capture it: more than twice per cycle of the fastest change. Sample less often and you don't just miss changes; you see a slower pattern that isn't there, like a wagon wheel that seems to turn backwards in a film.

## What it is

Observation is always sampling: of time (how often you look), of space (where the sensors are), of kinds of event (what the instrument can detect), and of population (who or what gets counted). Sampling too slowly misses fast events and can create false patterns. Recording only what passed some filter, such as planes that returned or flights with problems, biases everything inferred from it. Missing data must be distinguished from data that says "nothing happened": a heartbeat, an explicit "no data" state, and summaries like minimum and maximum between samples turn silence into information.

## Where it gets misapplied

- **Last known value shown as current.** Kofi's green square, all weekend.
- **Sampling slower than things change.** Spikes between samples vanish, or turn into patterns that aren't there.
- **Analysing only the cases that reached you.** Planes that came back, flights with problems, users who answered.
- **The mirror:** recording everything, at the highest rate, forever. It costs money and attention, and a flood of data hides gaps as well as an absence of data does. Decide what you need to see, and check that you can.

## Connections

- Learning this is also learning [information](information.md), because a reading only tells you something if it rules out possibilities, and a missing reading rules out nothing.
- Learning this is also learning [compression](compression.md), because sampling is lossy compression of the world, decided before anyone knew what would matter.
- Learning this is also learning [distributions and percentiles](../math/percentiles.md), because averages and slices are only as good as the sample beneath them.
- Learning this is also learning [labels and training data](../data/labels.md), because a model learns only from what someone chose to record.
- Learning this is also learning [statistical significance](../math/statistics.md), because a biased sample produces confident answers to the wrong question.
- Learning this is also learning [sampling and aliasing](../signals/sampling.md), because sampling too slowly doesn't just leave gaps; it can draw a pattern that isn't there.
- Learning this is also learning [state estimation](../signals/state-estimation.md), because when a sensor goes quiet, the honest response is to grow less certain, not to keep its last reading.

## Resources

1. The Rogers Commission report, chapter 6, on the O-ring data (start here: [online at NASA](https://www.nasa.gov/history/rogersrep/v1p146.htm)).
2. Bill Casselman, ["The Legend of Abraham Wald"](https://www.ams.org/samplings/feature-column/fc-2016-06) (go deeper: what Wald actually did, and how the story grew).
3. Any introduction to signal processing, for the sampling theorem and aliasing (reference).

## Names you'll hear

- **Sampling rate, Nyquist rate:** how often you measure, and the minimum rate to capture a signal.
- **Aliasing:** a false pattern created by sampling too slowly.
- **Survivorship bias:** drawing conclusions only from what survived to be observed.
- **Selection bias:** a sample chosen in a way that differs from what it's meant to represent.
- **Heartbeat:** a regular "I'm here" signal, so silence can be noticed.
- **Missing data:** absent values, which are themselves information about the measuring process.

## Go and look

Pick a dashboard you trust and find out what it shows when its data stops arriving. If the answer is "the last value, looking normal", you've found your green square.
