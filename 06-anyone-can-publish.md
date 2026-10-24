# 6. Anyone can publish

Last reviewed: 2026-10-24

## Problem

Software used to be shipped to every user's machine, and every copy aged on its own. Putting it on one server and letting a browser fetch it fixed that. But it split the program in two, a client and a server, and two halves can disagree about what's true.

## The story

Hannah Weiss joined a small company in Minneapolis in 1997 that sold appointment software to dental clinics. The software came on a CD. Each clinic installed it on the front-desk computer, and the appointments lived on that computer's disk.

Her first job was a bug fix: the calendar showed the wrong week whenever a month started on a Sunday. She fixed it in two days. Getting the fix to four hundred clinics took four months. CDs had to be burned and mailed, and then someone at each clinic had to install them, which many didn't. A year later the support team was handling calls from clinics on six different versions. Half of them were asking about bugs that had long since been fixed. Hannah came to dread the phrase "which version are you on?"

By 1999 the clinics all had internet connections and web browsers, and Hannah proposed the obvious thing: rebuild it as a website. One server, one copy of the software, one copy of the data. Fix a bug at lunchtime, and every clinic has the fix that afternoon. Nobody installs anything. The browser was already on every computer, and it could show any page a server sent it. It took a year. The day they switched the last clinic over, the support team brought cake.

The receptionists hated it. In the old program, clicking to the next day was instant. On the website, every click sent a request to the server, which built a whole new page and sent it back, and the browser threw away the old one and drew the new one from scratch. On a clinic's connection that took two or three seconds, all day, every click. The software was better in every way that mattered to Hannah, and worse in the one way that mattered to the people using it eight hours a day. A dentist in Duluth told her it was like going back to paper.

She lived with that for five years, because there didn't seem to be another way to build for the web. Then, in 2005, she used Google Maps for the first time and dragged the map, and it simply moved. The page didn't reload. New pieces of map appeared at the edges as she dragged. She opened the page's source to see how.

*Before reading on: the browser was redrawing the whole page for every click, even when only one appointment changed. What would you have wanted it to do instead?*

The trick was a browser feature that had been sitting there for years. A script on the page could quietly ask the server for just the data it needed, then change only the part of the page that had changed. Hannah rebuilt the calendar that way. When a receptionist clicked to the next day, the page asked the server for that day's appointments, a small list, and redrew the calendar itself. It felt instant. The server stopped sending pages and started sending data. Without anyone deciding it, her backend had become an API, because what the receptionists expected from the screen had changed what the server had to do.

To make booking feel instant too, she kept a copy of the day's appointments in the browser. When a receptionist booked a slot, the screen showed it booked straight away and told the server in the background. Every click now felt as fast as the old CD.

Three weeks later a clinic in Rochester called. Two patients had turned up for the same ten o'clock filling. Two receptionists, at two desks, had each booked the slot within a minute of each other. Each screen had shown it free, because each screen's copy was from when the page had loaded that morning. Each screen had shown it booked. The server had saved both. Nobody had done anything wrong. There were now two sources of truth, the server's and each browser's, and they disagreed.

Hannah's first thought was to make the copies in the browsers stay in sync with each other. She spent a week sketching ways to do it before she admitted she was trying to build a second server inside every browser. The real fix was simpler and a little humbling. The server owned the truth, and the browser's copy was only ever a copy. When a booking arrived, the server checked whether the slot was still free. If it wasn't, it refused, and the screen said *that slot was just taken* and refreshed the day. The browser could still assume a booking would succeed, to keep things fast, but it had to be ready to be told it was wrong. The double bookings stopped.

In 2009 the clinics started asking for an iPhone app, because that was where patients looked for things now. Hannah built one that was mostly her website inside a thin native shell. It wasn't because native code was better. It was because the App Store was the only way onto the phone, and Apple decided who got in. One server still beat a million installs. But the companies that owned the path to the user could still make you install something.

Looking back, Hannah thought that every hard problem she'd had since 1999 had come from the same split. The server owns the truth; the client owns what's on the screen and a copy of the state. The copy makes things fast, and it can be wrong. Almost every bug that users could see had been two sources of truth disagreeing.

## It really happened

Hannah is fictional; the web's path wasn't. Tim Berners-Lee proposed the web in 1989, and the Mosaic browser made it popular from 1993. The browser feature Hannah found came from Microsoft's Exchange team, who built it around 1999 for the web version of Outlook. The client side of Gmail later followed roughly the same design ([Alex Hopmann, "The story of XMLHTTP"](https://www.alexhopmann.com/page/the-story-of-xmlhttp)). Microsoft built it first; Google made it famous. In February 2005 Jesse James Garrett gave the pattern a name, Ajax, using Google Maps and Google Suggest as examples ([Garrett, "Ajax: A New Approach to Web Applications"](https://designftw.csail.mit.edu/lectures/apis/ajax_adaptive_path.pdf)).

The two-sources-of-truth problem got harder as screens got more ambitious. Figma lets many people edit one design at once in a browser. Its engineers chose the same answer Hannah reached: changes go to a server, which broadcasts them, and when two people change the same property of the same object, the server picks one ([Figma, "Multiplayer editing in Figma", 2017](https://www.figma.com/blog/multiplayer-editing-in-figma/); [the 2019 follow-up](https://www.figma.com/blog/how-figmas-multiplayer-technology-works/) <!-- verify -->). They wrote that they considered more sophisticated merging techniques and chose the simplest design that worked. Ladder: down, a hand-built engine where nothing on sale could do it.

## What survived

The client and server split the work. The server owns the truth; the client owns presentation and a copy of the state. Most bugs users see are two sources of truth disagreeing. A client can assume an action will succeed, to feel fast, but it has to be ready to be told it didn't. The browser won because shipping one server beats shipping a million installs; native shells survive where platforms control distribution. And what users come to expect on screen keeps reshaping the backend: Ajax turned servers into APIs, and later expectations brought mobile query languages, live collaboration, and streaming.

## Where it gets misapplied

- **A heavy single-page app for a page of text.** Shipping a program to the browser to show what plain HTML would show faster, and that search engines and screen readers handle better.
- **State duplicated in three places.** The server, a browser cache, and a component's local copy, each updated separately. Every extra copy is another chance to disagree.
- **Accessibility left until there's a lawsuit.** Screen readers, keyboards and contrast aren't extras. Courts in several countries have treated inaccessible websites as discrimination ([forces: who pays](forces.md#who-pays-vs-who-benefits)).
- **The mirror:** refusing any client-side state on principle. Users expect the screen to respond instantly, and a page that reloads for every click will lose to one that doesn't.

## Connections

- Learning this is also learning [networking](05-machines-need-to-talk.md), because HTTP is the contract between client and server, and every click is a round trip.
- Learning this is also learning [input validation](auth/input-validation.md), because the client is untrusted by definition: anyone can change what their browser sends.
- Learning this is also learning [cursor pagination](data/pagination.md), because infinite feeds needed a way to page through data that changes underneath you, and page numbers couldn't do it.
- Learning this is also learning [JavaScript](runtimes/javascript.md), because it won by shipping in the only browser that mattered, not by design.
- Learning this is also learning [forces](forces.md#distribution-and-platform-power), because whoever controls the path to users decides what you have to build.

## Resources

1. [MDN Web Docs, "How the web works"](https://developer.mozilla.org/en-US/docs/Learn_web_development/Getting_started/Web_standards/How_the_web_works) (start here). <!-- verify -->
2. Jesse James Garrett, ["Ajax: A New Approach to Web Applications"](https://designftw.csail.mit.edu/lectures/apis/ajax_adaptive_path.pdf) (2005): short, and the moment it got a name.
3. Evan Wallace, ["Multiplayer editing in Figma"](https://www.figma.com/blog/multiplayer-editing-in-figma/) (go deeper: two sources of truth, at their hardest).
4. Ink & Switch, ["Local-first software"](https://www.inkandswitch.com/local-first/) (the argument for putting more truth on the client, and what it costs). <!-- verify -->

## Names you'll hear

- **AJAX:** Garrett's 2005 name for pages that fetch data without reloading.
- **DOM:** the browser's model of the page, which scripts change to redraw parts of it.
- **SPA:** a single-page application, where the browser runs most of the program.
- **Optimistic update:** showing an action as done before the server confirms it, Hannah's fast booking.
- **CRDT:** a data structure whose copies can be edited separately and always merge to the same result. One answer to two sources of truth, at a cost.
- **JavaScript:** designed in about ten days at Netscape in 1995. Its quirks have outlived every decision made in a hurry that week.

## Go and look

Find a piece of state cached on the client in something you've built and ask whether it's a second source of truth by accident or by design, and what happens when it's wrong.

## The model so far

New on this page: sentence 6, in bold. The full model is in [the-model.md](the-model.md).

Engineering is turning what we have into what someone values, within limits, for a reason. Every step is a trade-off, and the engineer's job is to negotiate them.

0. Humans don't operate on the world directly; we build representations of it and operate on those. Every representation is a choice among others that could have been made, and every choice has an edge: decimal gave way to binary; naturals gave way to negatives, irrationals, and complex numbers; bits now have qubits beside them for a narrow class of problems; even formal axioms have an edge, since any consistent system rich enough for arithmetic contains true statements it can't prove (Gödel), and a cousin of that limit shows up in computation as the halting problem (Turing). This wiki hands out representations the same way every textbook does: cleanly, past their edges. Finding the edge is the reader's job.

1. A computer is a little fast memory near a processor and ever larger, slower, cheaper storage further away. Everything fast is small and near; everything big is slow and far. The cost of an operation is set by where the data is.

2. A machine's resources are shared, so something has to divide them: the operating system turns one machine into many processes and threads and decides who runs. Sharing creates waiting, and waiting, not computing, is where most time goes.

3. Programs outgrow a single head, so we build layers of abstraction: languages, libraries, types. Each layer trades control for ease. Building is mostly assembling existing abstractions; optimizing is mostly replacing one with something made for the case at hand, and the skill is knowing when the abstraction's cost has been measured and found to dominate. Data structures and algorithms are the reusable shapes inside those layers, chosen by the access pattern they serve.

4. Data outlives programs, so its shape is the longest-lived decision. A store is chosen by how data is read and written; indexes trade write cost for read speed; transactions define what the store promises.

5. Data is rarely where it's needed, so it moves, and moving it is slow, unreliable, and paid for in round trips. Protocols are contracts between parties that can't see each other. Anything that crosses a network can be lost, delayed, or duplicated, so systems retry and tolerate repeats. Once data moves cheaply, distribution is free, and value shifts from copies to services, relationships, and trust.

6. **Client and server split the work: the server owns the truth, the client owns presentation and a copy of state. Most interface bugs are two sources of truth disagreeing. The browser won because shipping one server beats shipping a million installs; native shells survive where platforms control distribution.**
