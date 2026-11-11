# Feedback and control

Last reviewed: 2026-11-03

A concept page in the signals and control family: measure, compare, correct, and repeat. Anything that corrects itself can overshoot, and a delay between measuring and acting makes it worse. It's one of the most widely recurring ideas in engineering, well beyond robots.

## Problem

Commands don't come true on their own. A motor told to lift a drone doesn't know about the wind or the weight of the camera; a fleet of servers told to handle the load doesn't know the load will double at nine. So systems measure where they are, compare it with where they should be, and correct. That loop is what makes machines robust. But a loop corrects based on what it *saw*, and what it saw is always a little out of date. Correct too hard, or too late, and the system swings past its target, back again, and sometimes further each time.

## The story

In 2014 Astrid Halvorsen wrote the flight software for a small company in Norway that built drones for inspecting wind turbines. The most important feature was holding a steady height beside a turbine blade while the camera filmed it. The drone measured its height with a pressure sensor, compared it with the target, and set the motors' power in proportion to the difference: a metre too low, a little more power; three metres too low, three times as much. To keep the drone steady in sudden gusts, Astrid made the correction strong. A strong correction meant a fast response, and a fast response seemed like exactly what a drone beside a turbine needed.

The first test flights bobbed. The drone rose past its target, dropped below it, rose past it again, a metre each way, every couple of seconds, and on a calm day the bobbing sometimes grew instead of dying away. The footage was useless. Astrid found two causes working together. The pressure sensor was noisy, so its readings were smoothed, and the smoothing made them about a third of a second late. By the time the controller saw the drone reach its target, the drone was already moving past it, and the strong correction was still pushing. Then, below the target, the same delay and strength sent it too far the other way.

She weakened the correction, and the bobbing stopped. But now, with the heavy camera fitted, the drone settled about a metre *below* its target, and stayed there. A correction proportional to the error only produces extra power while there *is* an error. To hold up the camera's weight, it needed a permanent one.

*Before reading on: a strong correction swung past the target, and a weak one never reached it. What would you have changed?*

Astrid rebuilt the controller from three parts, the combination control engineers had been using for most of a century. The first still corrected in proportion to how far off the drone was. The second added up the error over time, so a small error that persisted slowly built a larger correction, enough to carry the camera with no error left at all. The third responded to how fast the error was changing, so the drone eased off the power as it approached the target, braking before it overshot, not after. She also capped the second part. On the first test, the drone had been held on the ground for a minute before takeoff while the accumulated error grew, and it leapt into the air when released.

The biggest improvement came from the delay itself. She combined the slow, accurate pressure sensor with the drone's accelerometer, which was noisy but instant, so the controller knew its height almost immediately. With less delay in the loop, it could correct more firmly without swinging. She tuned it by commanding sudden one-metre steps and watching how the drone settled, and kept the plots.

A year later a customer asked to fly the drones by hand from a ship, over a radio link that delivered the video half a second late. The pilots overcorrected, steering hard against drift that the drone had already corrected, and it zigzagged. Astrid moved the fast loop onto the drone and gave the pilots a different control: point to where the drone should be, and let it get there itself.

Looking back, Astrid thought every loop that corrected itself was pulling against its own delay. How hard it corrected and how late it learned the truth decided together whether it settled or swung. Most of her best fixes hadn't been to the correction at all. They'd been to how quickly the drone found out where it was.

## Where it shows up

| Page | The loop | What it learned about overshoot and delay |
| --- | --- | --- |
| [5, Machines need to talk](../05-machines-need-to-talk.md) | Lin's backups and TCP, retrying when packets were lost | Retrying harder made congestion worse; Jacobson's fix made loss a signal to slow down, a feedback loop for the whole internet. |
| [Queueing](../latency/queueing.md) | Clients retrying into a full queue | Every retry is a correction based on old news; backoff weakens the correction so the queue can recover. |
| [12, Machines that learn from data](../12-machines-that-learn-from-data.md) | Gradient descent nudging a model's numbers | A learning rate that's too large overshoots and diverges; too small and training never arrives, the same trade as Astrid's. |
| [Round trips](../latency/round-trips.md) | Any loop that crosses a network | The round trip is the delay in the loop, and it limits how quickly any correction can safely act. |
| [State estimation](state-estimation.md) | Astrid's pressure sensor plus accelerometer | Better knowledge of where you are, sooner, is often the best fix for a loop. |

It shows up elsewhere too: autoscalers that add servers after a peak has passed and remove them just as the next one arrives, thermostats, cruise control, central banks setting interest rates, shops whose orders swing wildly because of delays in the supply chain, and teams that overcorrect after an incident with rules that cause the next one.

What these share is the loop and its two dials: how strongly it corrects, and how old its information is. Strong correction with old information swings. Weak correction never arrives. Most improvements come from making the information fresher, then correcting as firmly as that allows.

## It really happened

Astrid is fictional; the loop is very old. From 1788 James Watt fitted steam engines with a centrifugal governor, spinning weights that closed the steam valve as the engine sped up. Some engines with governors *hunted*, speeding up and slowing down in a rhythm nobody could explain, until James Clerk Maxwell analysed governors mathematically in 1868, in a paper often called the start of control theory. In 1922 Nicolas Minorsky, working on automatic steering for the US Navy, published the first analysis of the three-part controller Astrid used, partly by watching how experienced helmsmen corrected a ship's course. In 1942 John Ziegler and Nathaniel Nichols published rules for tuning such controllers that are still taught.

The internet nearly failed for lack of the right loop. In October 1986, throughput between two Berkeley sites a few hundred metres apart fell from 32 kilobits a second to 40 bits a second, because every computer retried harder as the network got worse. Van Jacobson and Michael Karels fixed it by making TCP slow down when packets were lost ([page 5](../05-machines-need-to-talk.md)). And delay can't always be engineered away. A radio signal takes between about 3 and 22 minutes to reach Mars, depending on where the planets are, so nobody can steer a Mars rover with a joystick. Engineers send goals, and the rover's own navigation software finds a safe path to them, the same move Astrid made with the drone.

## What it is

A feedback controller repeatedly measures a system's output, compares it with a target (the *setpoint*), and adjusts its input to reduce the difference (the *error*). The common PID controller combines three terms: proportional (how far off), integral (how long it's been off, which removes persistent error), and derivative (how fast the error is changing, which damps overshoot). The *gain* of each term sets how strongly it acts. Delay anywhere in the loop, in sensing, computing or acting, reduces how much gain the loop can use before it oscillates or becomes unstable. An *open-loop* system acts without measuring; it's simpler, and blind to anything it didn't expect.

## Where it gets misapplied

- **A strong correction acting on old information.** Astrid's first drone, autoscalers driven by five-minute averages, and clients retrying in step.
- **Integral wind-up.** A correction that accumulates while it can't act, and fires all at once when it can: the drone held on the ground, and the backlog of retries released when a service recovers.
- **A person inside a fast, delayed loop.** Steering by hand over a slow link. Give people goals, and let a local loop do the fast work.
- **The mirror:** so much damping, or so many safety margins, that the system never responds to anything. A loop that never swings and never arrives isn't stable; it's just slow.

## Connections

- Learning this is also learning [queueing](../latency/queueing.md), because retrying is a feedback loop, and backoff is how you keep it from amplifying the overload.
- Learning this is also learning [round trips](../latency/round-trips.md), because a network's delay is the delay in every loop that crosses it.
- Learning this is also learning [state estimation](state-estimation.md), because a controller can only be as good as its knowledge of where it is.
- Learning this is also learning [sampling](sampling.md), because a controller sees the world only at its samples, and anything between them is invisible to it.
- Learning this is also learning [state machines](../dsa/state-machines.md), because robots usually need both, and the word "state" means something different in each: a named stage there, a continuous quantity such as height here.

## Resources

1. Brian Douglas, *Control Systems Lectures* and MATLAB's *Understanding PID Control* videos (start here: short, visual and clear). <!-- verify -->
2. Karl Johan Åström and Richard Murray, *Feedback Systems: An Introduction for Scientists and Engineers* (2nd edition, 2021) (go deeper: the authors have made a version available online). <!-- verify -->
3. Jacobson and Karels, ["Congestion Avoidance and Control"](https://people.eecs.berkeley.edu/~sylvia/cs268/papers/congavoid.pdf) (1988) (reference: feedback control applied to the internet).

## Names you'll hear

- **Setpoint, error:** the target, and how far from it the system is.
- **Gain:** how strongly the controller responds to the error.
- **Overshoot, oscillation, hunting:** going past the target, swinging back and forth, and the old name for it.
- **PID controller:** proportional, integral and derivative corrections combined.
- **Integral wind-up:** accumulated correction that fires all at once.
- **Open loop, closed loop:** acting without measuring, and acting on measurement.
- **Supervisory control:** a person sets goals, and a local loop pursues them.

## Go and look

Find an autoscaler, a retry policy or any rule in something you run that reacts to a measurement. Work out how old the measurement is when the action takes effect, then look at a graph of the system over a busy day for a sawtooth that shouldn't be there.
