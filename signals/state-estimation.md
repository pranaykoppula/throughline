# State estimation

Last reviewed: 2026-11-03

A concept page in the signals and control family: a machine never knows exactly where it is. The best it can do is combine sources that are each wrong in their own way into a best guess, and keep track of how sure it is.

## Problem

Every sensor is wrong somehow. Satellite positioning is accurate on average and jumps about; wheel counters are smooth and drift; cameras can't see in the dark; a gyroscope slowly forgets which way is north. Trust any one of them completely and you inherit its particular failure. And when a sensor goes quiet, the tempting thing is to keep using its last reading, as if nothing could have changed. The motive is to act sensibly in a world you can only glimpse, which means knowing not just what you think is true but how sure you are.

## The story

In 2008 Dorota Wiśniewska led the software team at a Polish company that made automatic steering for tractors. A farmer planting crops needed perfectly straight, evenly spaced rows, hour after hour, and a tractor that steered itself could do it better than a tired driver. The system used satellite positioning with a local correction signal, accurate to a few centimetres most of the time. Dorota's first design steered straight to wherever the satellite receiver said the tractor was. It was the most accurate sensor on the machine, so trusting it seemed obvious.

Farmers liked it in open fields, and complained about it near trees. Along a line of poplars, or beside a barn, satellite signals bounced off the obstacles, and for a second or two the position jumped by half a metre. The tractor jerked towards the false position and back, and left a wave in the row that stayed visible all season. Once, under a long line of trees, the receiver lost its signal completely. The software kept steering to the last position it had received, as if the tractor hadn't moved, and the tractor ran on for fifty metres, drifting, before the driver grabbed the wheel.

Her second design leaned the other way. Between satellite readings, the tractor counted wheel turns and measured its own turning with a gyroscope, and worked out where it must be. That was smooth, with no jumps. But wheels slipped in wet soil and the gyroscope drifted, and the small errors added up. After a minute without satellite corrections, the tractor could be a metre off without any sign that anything was wrong.

*Before reading on: one source was accurate but jumpy, and the other was smooth but drifted. Which would you have trusted?*

Dorota stopped choosing. The new software kept two things at every moment: a best guess of the tractor's position, heading and speed, and a measure of how uncertain that guess was. Each fraction of a second, the wheel counters and gyroscope moved the guess forward, and the uncertainty grew a little, because they drifted. Each satellite reading then pulled the guess towards itself, by an amount that depended on how uncertain each was. When the guess was already confident and the reading was usually noisy, the reading nudged it slightly. When the guess had drifted for a while, the reading pulled it a long way. A reading too far from anything the tractor could physically have reached was treated as a reflection and ignored. The software even estimated how much the wheels were slipping, by comparing the wheel counts with the satellite positions, and corrected for it.

Losing the satellite signal stopped being invisible. The uncertainty simply kept growing, and when it passed what straight rows could tolerate, the tractor slowed down, sounded an alarm and handed the steering back to the driver. Rows near trees came out straight, and nobody was surprised at the end of a long line of poplars any more.

Looking back, Dorota thought the tractor had never known where it was, and never could. What it could know was how sure it was, and that turned out to matter as much as the guess itself. It decided how much to believe each new reading, and when to stop trusting itself and ask a person.

## Where it shows up

| Page | The estimate | What tracking uncertainty changed |
| --- | --- | --- |
| [Sampling and observation](../info/observation.md) | Kofi's fridges, and the sensor that went silent | Silence had to mean "unknown", a grey square, not the last good reading. |
| [Information gain](../info/information-gain.md) | What each new reading is worth | A reading is worth exactly how much it reduces your uncertainty. |
| [Statistical significance](../math/statistics.md) | Is this difference real, or noise? | The same question, asked once about a dataset instead of continuously about a moving tractor. |
| [Feedback and control](feedback.md) | Astrid's height, from a slow sensor and a fast one | Combining them gave the controller fresher knowledge, which let it correct more firmly. |

It shows up elsewhere too: the blue dot on a phone's map, with its circle of uncertainty that grows indoors; aircraft and spacecraft navigation; self-driving cars; weather forecasts, which merge models with millions of observations; robots that build a map of a room while working out where they are in it; robots trained in simulation that fail on a real floor; and project estimates, which ought to carry their uncertainty as visibly as their dates.

What these share is a belief about something you can't see directly: a best guess, plus how sure you are, updated as evidence arrives. Each source is trusted in proportion to how reliable it is, and missing evidence makes you less sure, not more.

## It really happened

Dorota is fictional; the method she reinvented is the Kalman filter. Rudolf Kálmán published it in 1960. That same year Stanley Schmidt, at NASA's Ames Research Center, heard Kálmán describe it and saw that it could solve the problem his group was working on: navigating a spacecraft to the Moon with noisy measurements and a small onboard computer. Schmidt's team extended it to the curved paths of real spaceflight, and a version of it flew in the Apollo guidance computer. It became a standard tool in navigation, from aircraft to air traffic control to the phone in your pocket (McGee and Schmidt tell the story in NASA Technical Memorandum 86847, 1985).

In 2005 Stanley, a self-driving car built by Sebastian Thrun's team at Stanford, won the DARPA Grand Challenge, a race across about 200 kilometres of desert. Its approach treated every sensor reading as uncertain and reasoned in probabilities throughout, which Thrun, Wolfram Burgard and Dieter Fox set out in their textbook *Probabilistic Robotics* the same year. The simulation gap is the same problem in another form. In 2017 Josh Tobin and colleagues trained a robot's vision entirely in simulation with deliberately random colours, textures and lighting, so that the real world looked like just one more variation, and it worked on a real robot ([Tobin et al., "Domain Randomization"](https://arxiv.org/abs/1703.06907)).

## What it is

State estimation infers quantities you can't measure directly, such as position, speed or heading, from indirect, noisy measurements over time. Here *state* means those continuous quantities, a different sense from the named stages of a [state machine](../dsa/state-machines.md); real robots usually have both. An estimator keeps a best guess and its uncertainty. It *predicts* how the state changes, which increases uncertainty, and *updates* the guess with each measurement, weighting it by how reliable the measurement is relative to the guess. The Kalman filter does this optimally when errors are well-behaved; particle filters and others handle harder cases. Combining different sensors this way is called sensor fusion.

## Where it gets misapplied

- **Trusting the most accurate sensor absolutely.** Dorota's first tractor: accurate on average, and jerked by every bad reading.
- **Holding the last value when data stops.** The tractor under the poplars, and Kofi's green square.
- **Throwing away the uncertainty.** A single number on a dashboard, an estimate without a range, a model's answer without a measure of confidence.
- **The mirror:** an estimator so elaborate nobody can tune or debug it. A simple weighted average of two sources, with a sanity check, is often enough to start; be precise about what you know before being sophisticated about it.

## Connections

- Learning this is also learning [observation](../info/observation.md), because estimation is what to do with the gaps observation leaves, and silence is a reason to be less sure.
- Learning this is also learning [information gain](../info/information-gain.md), because every measurement is worth the uncertainty it removes, and estimation is that idea running continuously.
- Learning this is also learning [statistical significance](../math/statistics.md), because separating signal from noise is the same problem, asked once instead of every moment.
- Learning this is also learning [feedback and control](feedback.md), because a controller acts on an estimate, and a better estimate allows a firmer correction.
- Learning this is also learning [state machines](../dsa/state-machines.md), because robots need both kinds of state, and the shared word causes real confusion.

## Resources

1. Tim Babb, ["How a Kalman filter works, in pictures"](https://www.bzarg.com/p/how-a-kalman-filter-works-in-pictures/) (2015) (start here: the whole idea, with diagrams and almost no prerequisites). <!-- verify -->
2. Sebastian Thrun, Wolfram Burgard and Dieter Fox, *Probabilistic Robotics* (2005) (go deeper: estimation, mapping and planning, all under uncertainty).
3. Rudolf Kálmán, "A New Approach to Linear Filtering and Prediction Problems" (1960) (reference).

## Names you'll hear

- **State, estimate:** what you want to know, and your best guess of it.
- **Uncertainty, covariance:** how unsure the guess is, and how the uncertainties of different quantities relate.
- **Predict, update:** move the guess forward in time, then correct it with a measurement.
- **Sensor fusion:** combining sensors with different strengths and failures.
- **Dead reckoning:** estimating position from your own motion alone, which drifts.
- **Kalman filter, particle filter:** the classic estimator, and a more flexible one for messier problems.
- **SLAM:** simultaneous localisation and mapping, building a map while working out where you are on it.

## Go and look

Open a map on your phone and watch the circle around your position as you walk indoors and back outside. That circle is the estimate's uncertainty. Then find a number in something you run that's shown without a range, and ask what its circle would look like.
