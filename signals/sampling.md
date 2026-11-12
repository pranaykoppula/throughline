# Sampling and aliasing

Last reviewed: 2026-11-03

A concept page in the signals and control family: how a continuous world is **represented** as numbers in a machine, and why sampling too slowly doesn't just miss things. It invents things that aren't there.

## Problem

Sound, light, temperature, vibration and motion change continuously. A computer can only store numbers, so something has to measure the world at intervals (*sampling*) and round each measurement to one of a fixed set of values (*quantisation*). Both choices are usually made to save money: fewer samples and fewer bits cost less to store and send. Get them wrong and the data isn't just coarse. It can show a pattern that never existed, and look completely trustworthy while doing it.

## The story

In 1994 Henrik Aalto was the instrumentation engineer at a paper mill in Finland. Paper ran through the machines at high speed over dozens of heavy rollers, and a failed roller bearing could tear the paper sheet and stop production for a day. The mill was replacing technicians' monthly rounds with a computer that watched vibration sensors on every bearing, all the time. Disk space was expensive, and there were hundreds of sensors, so Henrik had to decide how often to record each one. The rollers turned a few times a second. He chose two hundred readings a second per sensor, which seemed generous: dozens of readings for every turn of a roller.

For three months the system worked well, and the plots it drew became part of the morning meeting. One roller showed a slow, steady wobble of about ten cycles a second, which everyone agreed was harmless, perhaps a slightly uneven roll. Then that roller's bearing failed, the paper tore, and the mill lost most of a day.

The bearing's manufacturer sent a specialist with a portable analyser, which measured vibration continuously, not two hundred times a second. On a matching roller nearby, whose bearing was starting to fail the same way, it showed a strong vibration at about one hundred and ninety cycles a second, the frequency that a damaged bearing of that size produces. Henrik's system had never shown anything at that speed. Then he worked out why. A vibration of one hundred and ninety cycles a second, measured two hundred times a second, is caught a little earlier in its cycle at each reading. Joined up, the readings trace a slow wave of ten cycles a second. The system hadn't missed the danger. It had recorded it faithfully, and drawn it as something harmless.

*Before reading on: the sensors worked, the readings were accurate, and the plot showed a vibration that didn't exist. What would you have changed?*

Henrik learned the rule he'd never been taught. To record a vibration correctly, you have to sample more than twice as fast as it vibrates. And the rule applies to the fastest thing that's *there*, not the fastest thing you care about, because anything faster folds down and disguises itself as something slower. Since nobody could know everything a machine might do, each sensor got an electronic filter, before the measurement was taken, that removed everything faster than the system could record. A bearing sensor now recorded two thousand readings a second, comfortably more than twice the fastest bearing fault frequency, with the filter making sure nothing faster could sneak in.

That was ten times the data, so he stopped keeping all of it. Each sensor's computer now reduced each minute of readings to a summary: the overall level, the peak, and how much vibration there was at each frequency. The raw readings were kept only when a summary looked unusual. He also found a smaller mistake of the same kind. A sudden hard knock produced readings beyond the largest number the sensor's converter could represent, so it was recorded as the maximum value: large, but no larger than a moderate shock. He gave the converters more range, so the biggest plausible knock fitted, and enough bits that small vibrations still showed.

Looking back, Henrik thought sampling too slowly hadn't quietly lost information, as he'd assumed it would. It had made up new information, and the new information had looked exactly like the truth. The only protection was deciding, before measuring, what could be there.

## Where it shows up

| Page | What was sampled | What the gaps did |
| --- | --- | --- |
| [Sampling and observation](../info/observation.md) | Kofi's fridge, every thirty minutes | A fridge warming and cooling every forty minutes looked cool every time: the same effect, over hours. |
| [Floating-point](../math/floating-point.md) | Real numbers squeezed into a fixed number of bits | Quantisation: the values in between are rounded away. |
| [Compression](../info/compression.md) | Henrik's summaries, kept instead of every reading | Choosing what to keep, before anyone knows what they'll need. |
| [Tokens and context windows](../ai/tokens.md) | Text chopped into tokens | A discrete version of language; what falls inside a token, such as the letters of a word, is hard for the model to see. |
| [Designed for human senses](perception.md) | Sound, for CDs | 44,100 samples a second, just over twice the highest note people can hear. |

It shows up elsewhere too: wagon wheels that seem to turn backwards in films, shimmering patterns when you photograph a screen, jagged edges on diagonal lines in computer graphics, a keyboard reading a switch that bounces, a touchscreen sampling a moving finger, and monitoring systems that record a metric every minute and never see the spike that lasted ten seconds.

What these share is the boundary between a continuous world and a machine that stores numbers. Every digital record made two choices there, how often to look and how finely to measure, and those choices decide not only what's missing but what false patterns might appear.

Motif: [every representation has an edge](../motifs.md#every-representation-has-an-edge).

## It really happened

Henrik is fictional; the rule he learned has several fathers. E. T. Whittaker proved the mathematics in 1915, with no thought of engineering. Harry Nyquist showed a closely related result about telegraph signals in 1928. Vladimir Kotelnikov proved the sampling theorem for communications in 1933 in the Soviet Union, where it is still called Kotelnikov's theorem, but his work was little known outside it for years. Claude Shannon proved and popularised it in 1949. It's usually called the Nyquist–Shannon theorem in the West; the name is more about who was read than who was first.

The compact disc's 44,100 samples a second is just over twice the roughly 20,000 cycles a second that young human ears can hear. The exact number came from an accident of history. In the late 1970s, before computer disks were big enough, studios recorded digital audio onto video tape using *PCM adaptors*, which stored samples in the lines of a television picture. Three samples per line, on the usable lines of each field, at the television's field rate, came to 44,100 a second, and the CD inherited it.

## What it is

Sampling measures a continuous signal at regular intervals; quantisation rounds each measurement to one of a fixed number of levels. A signal containing nothing faster than a certain frequency can be reconstructed exactly from samples taken at more than twice that frequency. Anything faster that reaches the sampler *aliases*: it appears as a false, slower signal that can't be told apart from a real one afterwards, so it has to be filtered out before sampling. Quantisation adds a small rounding error at every sample, and anything beyond the range is *clipped* to the maximum. More samples and more bits cost storage and bandwidth, which is why these choices are always a trade.

## Where it gets misapplied

- **Choosing the sample rate from what you care about, not what's there.** Henrik's two hundred readings a second, and the bearing that vibrated at one hundred and ninety.
- **Thinning data by keeping every tenth point.** Downsampling without filtering first aliases too: smooth or summarise, don't just skip.
- **Clipping.** The biggest events are the ones that hit the ceiling, and they're usually the ones that matter.
- **The mirror:** recording everything at the highest rate, forever. Storage, bandwidth and attention are all finite; decide what question the data answers, and sample for that, with a filter for everything else.

## Connections

- Learning this is also learning [observation](../info/observation.md), because aliasing is the sharpest form of what sampling can't see: not a gap, but a false pattern.
- Learning this is also learning [floating-point](../math/floating-point.md), because quantisation is rounding, and it has the same edges.
- Learning this is also learning [compression](../info/compression.md), because sampling is the first lossy decision anyone makes about a signal, before any compression begins.
- Learning this is also learning [state estimation](state-estimation.md), because every sample is one noisy glimpse, and estimation is how glimpses become a belief.
- Learning this is also learning [feedback and control](feedback.md), because a controller only sees the world at its samples, and acts on what it saw.
- Learning this is also learning [exact or approximate](../dsa/exact-or-approximate.md), because Henrik's per-minute summaries are a small, deliberate approximation of a large stream.

## Resources

1. Monty Montgomery, ["Digital Show & Tell"](https://xiph.org/video/vid2.shtml) (2013) (start here: a video that demonstrates sampling, quantisation and aliasing on real equipment). <!-- verify -->
2. Steven W. Smith, [*The Scientist and Engineer's Guide to Digital Signal Processing*](https://www.dspguide.com/) (go deeper: free online, and written for practical people). <!-- verify -->
3. Hans Dieter Lüke, "The Origins of the Sampling Theorem", *IEEE Communications Magazine* (1999) (reference: who found what, and when).

## Names you'll hear

- **Sample rate:** how many measurements are taken each second.
- **Nyquist rate, Nyquist frequency:** twice the highest frequency present, and half the sample rate.
- **Aliasing:** a fast signal appearing as a false slow one.
- **Anti-aliasing filter:** removes what's too fast to record, before sampling.
- **Quantisation, bit depth:** rounding to fixed levels, and how many levels there are.
- **Clipping:** a value beyond the range, recorded as the maximum.
- **ADC, DAC:** analogue-to-digital and digital-to-analogue converters, the two sides of the boundary.

## Go and look

Film a spinning fan or a car wheel with your phone, and watch for blades that crawl, stop or turn backwards. Then find a metric you monitor, check how often it's recorded, and ask what could happen between two readings that you'd never see.
