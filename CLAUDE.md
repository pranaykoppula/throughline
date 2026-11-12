# Throughline: notes for Claude

A Markdown wiki that teaches the intuition behind engineering decisions through stories. `SPEC.md` is the design and wins any disagreement with this file; update both in the same change if they drift.

## What it is for

The owner wants engineers to *feel* how real problems were met: a person who doesn't know the answer, makes a reasonable decision, hits a problem nobody could see from where they stood, and goes back to the drawing board. Make great engineers feel human; make hard problems feel solvable. Concepts are deeply interconnected, and recognising the recurrence is what builds intuition. Motive always comes first: why anyone needed the thing.

## Layout

- `00`–`13-*.md`: the spine, fourteen problems in historical order. Page 0 is a brief history in several anecdotes; pages 1–13 follow one fictional person each.
- Concept pages in family folders, one concept per page: `dsa/ data/ latency/ cost/ math/ auth/ runtimes/ tooling/ vendors/ writing/ cloud/ ai/ info/ crypto/ signals/`. The five map hubs are Data, DSA, Trust (`auth/`), Latency, Cost.
- `the-model.md` (the cumulative model), `forces.md`, `pushback.md`, `motifs.md` (recurring shapes, with every page each appears on), `README.md`, `SPEC.md`.
- `graph.html` (every page and link), `images/map.svg` (the spine as a transit line), both generated.
- `scripts/check_model.py`, `scripts/make_graph.py` (+ `graph_template.html`), `scripts/make_map.py` (hub dots are a hand-edited list in it), `scripts/make_figures.py` (every figure, as SVG).
- `.github/workflows/checks.yml` runs the model check and fails if `graph.html` or `images/map.svg` differ from what the scripts produce.
- `_config.yml` publishes the site with GitHub Pages (Jekyll, `jekyll-theme-primer`).

## Page shapes

Spine page (SPEC section 7): Builds on (one unheaded paragraph under the title naming the one or two earlier spine pages it climbs from, and why) · Problem · The story · It really happened · What survived · Where it gets misapplied (with the mirror) · Connections · Resources · Names you'll hear · Go and look · The model so far (sentences 0..N, only N in bold).

Concept page (SPEC 7.1): Problem · The story · **Where it shows up** (table: page | the thing | what it taught, then "elsewhere too", then what the rows share) · It really happened · What it is · Where it gets misapplied · Connections · Resources · Names you'll hear · Go and look. No model section. `dsa/hashing.md` is the sample.

## Voice and story rules

- Third person limited, past tense, told in retrospect. Stay inside one head; the narrator may look back from later ("It was months before she learned…").
- Beats: the reasonable decision (say why it was right) → what it caused → one italic *Before reading on: …?* pause → the rethink (what was kept, what replaced, which limit moved) → "Looking back, X thought…".
- Fiction carries the story and is labelled ("X is fictional"). Real people appear only in It really happened, or unnamed inside the story ("a young mathematician at the company"). Don't make the fiction copy a real case's exact numbers.
- A fictional character must not know other pages' fictional characters (Ines can't know Ruth). Reusing a character on purpose (Sam from page 8 in `data/partitioning.md`) is fine.
- Blunt and honest: say when something won by luck; name the money; mark reported reasons as reported; say "we don't know". Don't grade the past by today.
- Plain sentences. British spelling in prose. People are "they" unless the fiction gives a pronoun.
- Pick new names: many are used (Haddad, Okafor, Marsh and Weiss already twice). Search the repo before naming someone.

## Verbs and motifs

- Eight verbs (represent, store, move, transform, find, decide, show, protect), bolded once in a spine page's Problem or a concept page's opening line, only where the verb is what the page is about.
- `motifs.md` holds twelve named shapes with every page where each appears. A page that shows one clearly ends Where it shows up (or a spine page's What survived) with `Motif: [name](motifs.md#anchor).` At most two, only where the shape is the point. Keep the names fixed; add a page to the motif's list and the line to the page in the same change. New motifs need more than a couple of pages behind them.

## Figures

- Every figure is ours, drawn by `scripts/make_figures.py` into `images/figures/`. No photographs, archival images or AI-generated images, ever. Only where it shows the problem or the solution better than prose.
- Spine pages: one figure, in the story just before "Looking back" (after the rethink, so it doesn't spoil the pause), with alt text and an italic caption. Concept pages next, folder by folder in the order SPEC lists the families.
- Use the story's numbers; label anything else illustrative. Check light and dark by rendering with Playwright before committing.

## Connections

- One line each: "Learning this is also learning [specific concept](path), because …". Point at one concept, never a whole subject (`dsa/hash-tables.md`, not "DSA").
- When an idea recurs across stories, every page where it appears links to the same concept page, and the concept page's Where it shows up table lists them (the recurrence pass).
- When a new concept page uses an idea from a spine story, add a backlink on that spine page.
- Dangling links are allowed in principle (the frontier), but right now there are none.

## Facts and sources

- Verify every real case before it lands. This environment can't fetch most sites; use web search. A link not confirmed reachable gets `<!-- verify -->` after it (about 29 now; PR #8 checked and cleared most of those on pages that existed before 2026-11-03). Facts confirmed only from memory are said so in the commit message.
- Prefer primary sources; flag legends (Wald, Vail's type cases) and disputed accounts (Storm-0558's crash-dump theory) on the page.

## After any edit

```
python3 scripts/make_graph.py
python3 scripts/make_map.py      # only changes if make_map.py's hub list changed
python3 scripts/make_figures.py  # images/figures/
python3 scripts/check_model.py
```

Commit `graph.html` with the change. A model sentence lives in `the-model.md`, SPEC section 4, its own page and every later page; edit all in one change. Update the map's hub dots by hand if a spine page's Connections change family.

## Git workflow

- Pushing straight to `main` is allowed (the owner's permission, 2026-11-03). Use it for small, self-contained changes; run the checks first, since CI runs on push too.
- For a larger batch the owner may want to review, start a branch from `origin/main`, named for what it does in lowercase kebab-case (`add-time-and-clocks`, `fix-graph-click`, `verify-links`), and open a PR when asked. The owner merges by squash. Don't reuse `claude/project-overview-6pngmr`; that was the first session's branch, and the original of that name was renamed to `main` on GitHub.
- Commit messages end with the attribution lines the session provides.

## Status (2026-11-04)

- Done: all 14 spine pages; 79 concept pages across 15 families (including `dsa/bloom-filters.md`, and `dsa/` growth, amortised-cost, sorting, divide-and-conquer, dynamic-programming, greedy and heaps) plus the guide page `dsa/choosing.md`, including `info/` (information, compression, language, observation, error-correction, information-gain, secrecy; and, from the meaning-making angle, measures-and-targets, encodings, meaning-as-use) and `crypto/` (symmetric-encryption, public-key, key-management, randomness), merged in PR #4; and `signals/` (sampling, perception, feedback, state-estimation) plus `dsa/power-and-predictability.md` (the automata ladder), merged in PR #6.
- Exception from the owner: `dsa/` and system design get depth (SPEC 3.7). Planned: `dsa/` tries, append-only logs, exact-or-approximate, then search (one story through linear scan, binary search, hashing, tries, inverted indexes and ranking, like `sorting.md`); then a `design/` family starting with `approach.md`. Batches of about four, each page with a figure.
- Scope rule from the owner: a new page must carry a mental model that recurs outside its own field. Everything else is a row in an existing table, a line in "elsewhere too", or a link in Resources; depth lives in external sources. Input devices, displays, sound, robotics planning and safety were folded in that way, not given pages.
- The owner's interest: tech as the meeting of meaning-making (semiotics, linguistics, hermeneutics) and mathematics. Stories here are fiction, so don't present patterns across them as findings about the world. Reading-list items (Naur, Weaver, Winograd and Flores, Lakatos, Bender and Koller) are in the relevant Resources sections.
- Candidates for later pages: embeddings (with the search gap), names and identity (check whether a row in `data/modelling.md` is enough).
- Open: the link-verification pass (needs Firecrawl or wider network access); gaps the owner listed: time and clocks, testing, observability, memory management and compilers, search; graphics later (it builds on `signals/sampling.md` and `signals/perception.md`). The spec's later tracks: business acumen, AI engineering, mathematical intuition.
- The owner reviews each spine page before the next; concept pages go in batches.
